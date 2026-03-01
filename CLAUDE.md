# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此代码库中工作时提供指导。

## 项目结构

这是一个包含两个独立项目的 monorepo：

1. **Python 项目**（根目录 + `src/`）：Qwen 思维聊天机器人 - 使用阿里云百炼 Qwen3.5 API 的命令行聊天机器人，支持流式输出和思维链显示。
2. **Vue 3 项目**（`snake-game-vue/`）：赛博贪吃蛇 - 使用 Vue 3 + Vite 构建的贪吃蛇游戏，具有科技/赛博朋克风格的霓虹特效 UI。

---

## Python 项目命令

Python 项目使用 `uv` 作为包管理器（而非 pip/npm）。

### 运行 Python 脚本
```bash
# 从 src/ 目录运行 Python 脚本
uv run python src/qwen3.5_test.py
uv run python src/test.py
```

### 环境设置
```bash
# 安装依赖
uv sync

# 项目需要 Python 3.12+
```

### 配置
- API 凭证存储在 `.env` 文件中（DASHSCOPE_API_KEY）

---

## Vue 3 项目命令 (snake-game-vue/)

这是一个独立的 Vite + Vue 3 项目，使用 TypeScript 支持类型定义。

### 开发
```bash
cd snake-game-vue
npm run dev          # 启动开发服务器，地址 http://localhost:5173/
```

### 构建
```bash
cd snake-game-vue
npm run build        # 构建生产版本
npm run preview      # 预览生产构建
```

### 安装依赖
```bash
cd snake-game-vue
npm install
```

---

## Vue 3 项目架构

贪吃蛇游戏采用模块化架构，职责分离清晰：

### Composables（逻辑层）
位于 `snake-game-vue/src/composables/`：
- `useGameLogic.ts` - 核心游戏逻辑：蛇的移动、碰撞检测、食物生成
- `useCanvas.ts` - Canvas 绘图操作：网格、蛇、食物（带脉冲动画）
- `useLocalStorage.ts` - 最高分的持久化存储

### Components（UI 层）
位于 `snake-game-vue/src/components/`：

**游戏组件**（`components/game/`）：
- `SnakeGame.vue` - 主组件，协调游戏状态、循环和键盘事件
- `GameCanvas.vue` - Canvas 包装器，响应式绘图
- `ScoreBoard.vue` - 显示当前分数和最高分
- `GameOverModal.vue` - 游戏结束弹窗，带重新开始按钮

**UI 组件**（`components/ui/`）：
- `NeonButton.vue` - 可复用的霓虹发光按钮
- `GlowingText.vue` - 带闪烁霓虹效果的文字组件

### 状态管理模式
- 游戏状态（`'idle' | 'running' | 'paused' | 'gameover'`）在 `SnakeGame.vue` 中管理
- Composables 返回其内部状态的响应式 refs
- 不使用全局状态管理库（Pinia/Vuex）- 状态在组件内部管理

### 游戏配置
`SnakeGame.vue` 中的速度设置：
- `initialSpeed: 120`（每 tick 毫秒数）
- `minSpeed: 60`（每 tick 毫秒数）
- `speedIncrement: 2`（每吃一个食物减少的毫秒数）

---

## 工作目录说明

使用 bash 命令时，始终使用绝对路径，因为每个命令的工作目录会重置。例如：
```
/Users/jianbin/dev_projects/vs_projects/mock_claude_code/snake-game-vue/node_modules/.bin/vite
```

## 注意事项
请在每次回到的结尾加上：
> happy coding