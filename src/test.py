import json
import re
from typing import Dict, List, Any, Optional, Callable
import asyncio
import threading
import queue
from dataclasses import dataclass
from enum import Enum

# --- 数据模型 ---
@dataclass
class Message:
    role: str  # "user", "assistant", "tool_result"
    content: str
    tool_calls: Optional[List[Dict]] = None
    tool_call_id: Optional[str] = None

@dataclass
class ToolCall:
    id: str
    name: str
    arguments: Dict[str, Any]

@dataclass
class ToolResult:
    call_id: str
    result: Any
    is_error: bool = False

class ExecutionState(Enum):
    IDLE = "idle"
    THINKING = "thinking"
    EXECUTING_TOOL = "executing_tool"
    FINALIZING = "finalizing"

# --- 核心 Agent 类 ---
class ReactAgent:
    """
    简易版 Claude-style ReAct (Reasoning and Acting) Agent
    使用 React 模式进行思考和行动
    """
    def __init__(self, model_client=None, tools: Optional[Dict[str, Callable]] = None):
        self.model_client = model_client or MockModelClient()
        self.tools = tools or {}
        self.messages: List[Message] = []
        self.state: ExecutionState = ExecutionState.IDLE
        self.max_iterations = 10  # 防止无限循环
        self._execution_queue = queue.Queue()

    def add_tool(self, name: str, func: Callable):
        """注册一个工具"""
        self.tools[name] = func

    def _parse_thought_and_action(self, response_text: str) -> tuple[str, Optional[ToolCall]]:
        """
        解析模型响应，提取 Thought 和 Action
        这里简化为正则匹配，实际应用中可能需要更复杂的解析
        """
        thought_match = re.search(r"<thought>(.*?)</thought>", response_text, re.DOTALL)
        action_match = re.search(r"<action>(.*?)</action>", response_text, re.DOTALL)

        thought = thought_match.group(1).strip() if thought_match else ""
        action_json_str = action_match.group(1).strip() if action_match else ""

        tool_call = None
        if action_json_str:
            try:
                action_data = json.loads(action_json_str)
                tool_call = ToolCall(
                    id=action_data.get("id", "unknown"),
                    name=action_data["name"],
                    arguments=action_data["arguments"]
                )
            except (json.JSONDecodeError, KeyError):
                print(f"Failed to parse action: {action_json_str}")

        return thought, tool_call

    def _call_tool(self, tool_call: ToolCall) -> ToolResult:
        """执行工具调用"""
        if tool_call.name not in self.tools:
            return ToolResult(call_id=tool_call.id, result=f"Tool '{tool_call.name}' not found", is_error=True)

        try:
            # 执行工具函数
            result = self.tools[tool_call.name](**tool_call.arguments)
            return ToolResult(call_id=tool_call.id, result=result)
        except Exception as e:
            error_msg = f"Tool '{tool_call.name}' failed: {str(e)}"
            return ToolResult(call_id=tool_call.id, result=error_msg, is_error=True)

    async def run(self, user_input: str) -> str:
        """主执行循环"""
        self.state = ExecutionState.THINKING
        self.messages.append(Message(role="user", content=user_input))

        iteration_count = 0
        while iteration_count < self.max_iterations:
            iteration_count += 1

            # 1. 获取模型思考和下一步行动
            raw_response = await self.model_client.generate_response(self.messages)
            
            # 2. 解析模型的思考和行动
            thought, tool_call = self._parse_thought_and_action(raw_response)

            # 3. 记录思考过程（模拟 Claude 的思考过程可视化）
            if thought:
                print(f"[THOUGHT] {thought}")
                self.messages.append(Message(role="assistant", content=f"<thinking>{thought}</thinking>"))

            # 4. 如果模型决定采取行动（调用工具）
            if tool_call:
                self.state = ExecutionState.EXECUTING_TOOL
                print(f"[ACTION] Calling tool '{tool_call.name}' with args: {tool_call.arguments}")
                
                # 执行工具
                tool_result = self._call_tool(tool_call)
                
                # 将工具结果反馈给模型
                tool_result_msg = Message(
                    role="tool_result",
                    content=str(tool_result.result),
                    tool_call_id=tool_call.id
                )
                self.messages.append(tool_result_msg)
                
                print(f"[TOOL RESULT] {tool_result.result}")
                
                # 继续下一轮循环，让模型基于结果继续思考
                continue
            else:
                # 5. 如果模型没有采取行动，认为它已得出最终答案
                self.state = ExecutionState.FINALIZING
                final_answer = raw_response.split("</action>")[-1].strip() # 简化提取最终答案
                print(f"[FINAL ANSWER] {final_answer}")
                return final_answer

        # 达到最大迭代次数
        fallback_answer = "I couldn't complete the task within the allowed iterations."
        print(f"[FALLBACK ANSWER] {fallback_answer}")
        return fallback_answer

# --- 模拟模型客户端 ---
class MockModelClient:
    """
    模拟 LLM 客户端，返回预定义的 ReAct 格式响应
    在真实场景中，这里会是 OpenAI, Anthropic 等 API 调用
    """
    def __init__(self):
        # 定义一些示例响应，模拟 ReAct 逻辑
        self.responses = {
            "what is the weather in tokyo": [
                "<thought>I need to find the weather in Tokyo. I can use the get_weather tool.</thought>\n<action>{\"id\": \"call_123\", \"name\": \"get_weather\", \"arguments\": {\"location\": \"Tokyo\"}}</action>",
                "The current weather in Tokyo is sunny with a temperature of 22°C."
            ],
            "multiply 5 by 6": [
                "<thought>The user wants to multiply 5 by 6. I can use the calculate tool.</thought>\n<action>{\"id\": \"call_456\", \"name\": \"calculate\", \"arguments\": {\"operation\": \"multiply\", \"num1\": 5, \"num2\": 6}}</action>",
                "The result of multiplying 5 by 6 is 30."
            ],
            "default": [
                "<thought>I understand the request. I will formulate a helpful response.</thought>\nThis is a simple response without needing any tools.",
            ]
        }

    async def generate_response(self, messages: List[Message]) -> str:
        # 简化逻辑：根据用户最后一条消息决定响应
        last_user_msg = [m.content for m in messages if m.role == "user"][-1].lower()
        
        # 查找匹配的响应序列
        for key, response_list in self.responses.items():
            if key != "default" and key in last_user_msg:
                # 返回第一个响应（如果是多轮，这里只返回第一步）
                return response_list[0]
        
        # 如果没有匹配，返回默认响应
        return self.responses["default"][0]


# --- 示例工具定义 ---
def get_weather(location: str) -> str:
    """模拟获取天气的工具"""
    import random
    conditions = ["sunny", "cloudy", "rainy", "windy"]
    temp = random.randint(15, 30)
    return f"The current weather in {location} is {random.choice(conditions)} with a temperature of {temp}°C."

def calculate(operation: str, num1: float, num2: float) -> float:
    """模拟计算工具"""
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        return num1 / num2
    else:
        raise ValueError(f"Unknown operation: {operation}")


# --- 主程序入口 ---
async def main():
    agent = ReactAgent()
    
    # 注册工具
    agent.add_tool("get_weather", get_weather)
    agent.add_tool("calculate", calculate)

    print("--- React Agent Demo ---")
    
    # 测试用例 1: 调用工具
    print("\n[USER INPUT] What is the weather in Tokyo?")
    result = await agent.run("What is the weather in Tokyo?")
    print(f"[AGENT OUTPUT] {result}\n")

    # 清空消息历史
    agent.messages = []
    
    # 测试用例 2: 执行计算
    print("[USER INPUT] Multiply 5 by 6")
    result = await agent.run("Multiply 5 by 6")
    print(f"[AGENT OUTPUT] {result}\n")

    # 测试用例 3: 不需要工具的简单问题
    print("[USER INPUT] Hello, how are you?")
    result = await agent.run("Hello, how are you?")
    print(f"[AGENT OUTPUT] {result}\n")


if __name__ == "__main__":
    asyncio.run(main())