from openai import OpenAI
from dotenv import load_dotenv
import os

# 1. 加载 .env 环境变量
load_dotenv() 

# 2. 初始化客户端 (阿里云百炼)
client = OpenAI(
    # 确保 .env 文件里写的是 DASHSCOPE_API_KEY=sk-xxx
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 3. 【新增】从命令行获取用户输入
print("🤖 千问助手已就绪 (输入 'quit' 退出)")
while True:
    user_input = input("\n👤 请输入您的问题: ").strip()
    
    # 退出条件
    if user_input.lower() in ['quit', 'exit', 'q']:
        print("👋 再见！")
        break
    
    if not user_input:
        continue

    # 构建消息列表
    messages = [{"role": "user", "content": user_input}]

    try:
        # 4. 发送请求 (开启流式输出 + 思考模式)
        completion = client.chat.completions.create(
            model="qwen3.5-plus", 
            messages=messages,
            extra_body={"enable_thinking": True}, # 启用思考过程
            stream=True
        )

        is_answering = False  # 标记是否已经开始输出正式回答
        
        # 打印分隔线
        print("\n" + "=" * 20 + " 思考过程 " + "=" * 20)
        
        # 5. 处理流式响应
        for chunk in completion:
            if not chunk.choices:
                continue
                
            delta = chunk.choices[0].delta
            
            # 处理思考内容 (reasoning_content)
            if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                # 如果还没开始回答，先打印思考内容
                if not is_answering:
                    print(delta.reasoning_content, end="", flush=True)
            
            # 处理正式回答内容 (content)
            if hasattr(delta, "content") and delta.content:
                # 如果是第一次接收到正式内容，打印分隔线并切换状态
                if not is_answering:
                    print("\n" + "=" * 20 + " 完整回复 " + "=" * 20)
                    is_answering = True
                print(delta.content, end="", flush=True)
        
        # 每次回答结束后换行
        if is_answering:
            print("\n" + "-" * 50)
            
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        # 调试提示：如果是 Key 错误，提示检查 .env
        if "api_key" in str(e).lower():
            print("💡 提示：请检查 .env 文件中的 DASHSCOPE_API_KEY 是否正确配置。")