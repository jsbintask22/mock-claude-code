<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useGameLogic } from '../../composables/useGameLogic'
import { useLocalStorage } from '../../composables/useLocalStorage'
import GameCanvas from './GameCanvas.vue'
import ScoreBoard from './ScoreBoard.vue'
import GameOverModal from './GameOverModal.vue'
import GlowingText from '../ui/GlowingText.vue'
import type { GameState, Direction } from '../../types/game'

// 游戏配置
const CONFIG = {
  gridSize: 20,
  tileCount: 20,
  canvasSize: 400,
  initialSpeed: 120,  // 比原游戏慢 1/5 (原 100ms)
  minSpeed: 60,       // 比原游戏慢 1/5 (原 50ms)
  speedIncrement: 2
}

// 游戏状态
const gameState = ref<GameState>('idle')
const gameSpeed = ref(CONFIG.initialSpeed)
let gameLoop: number | null = null

// 使用 composables
const { snake, food, direction, score, initGame, update, updateDirection } = useGameLogic(CONFIG.tileCount)
const highScore = useLocalStorage('snakeHighScore', 0)

// 启动游戏
function startGame() {
  initGame()
  gameState.value = 'running'
  gameSpeed.value = CONFIG.initialSpeed
  gameLoop = setInterval(gameStep, gameSpeed.value)
}

// 暂停/继续游戏
function togglePause() {
  if (gameState.value === 'idle') {
    startGame()
  } else if (gameState.value === 'running') {
    gameState.value = 'paused'
  } else if (gameState.value === 'paused') {
    gameState.value = 'running'
  }
}

// 重新开始游戏
function restartGame() {
  if (gameLoop) clearInterval(gameLoop)
  startGame()
}

// 游戏步骤
function gameStep() {
  if (gameState.value === 'running') {
    const result = update()

    if (result.gameOver) {
      gameOver()
    } else if (result.ateFood) {
      // 吃到食物后增加游戏速度
      if (gameSpeed.value > CONFIG.minSpeed) {
        gameSpeed.value = Math.max(CONFIG.minSpeed, gameSpeed.value - CONFIG.speedIncrement)
        if (gameLoop) {
          clearInterval(gameLoop)
          gameLoop = setInterval(gameStep, gameSpeed.value)
        }
      }
    }
  }
}

// 游戏结束
function gameOver() {
  if (gameLoop) clearInterval(gameLoop)
  gameState.value = 'gameover'

  // 更新最高分
  if (score.value > highScore.value) {
    highScore.value = score.value
  }
}

// 键盘控制
function handleKeyDown(e: KeyboardEvent) {
  // 防止方向键和空格键的默认行为
  if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '].includes(e.key)) {
    e.preventDefault()
  }

  // 空格键
  if (e.key === ' ') {
    if (gameState.value === 'idle' || gameState.value === 'gameover') {
      restartGame()
    } else {
      togglePause()
    }
    return
  }

  // 方向键
  if (gameState.value === 'paused') return

  switch (e.key) {
    case 'ArrowUp':
      updateDirection({ dx: 0, dy: -1 })
      break
    case 'ArrowDown':
      updateDirection({ dx: 0, dy: 1 })
      break
    case 'ArrowLeft':
      updateDirection({ dx: -1, dy: 0 })
      break
    case 'ArrowRight':
      updateDirection({ dx: 1, dy: 0 })
      break
  }
}

// 生命周期
onMounted(() => {
  window.addEventListener('keydown', handleKeyDown)
  initGame()
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
  if (gameLoop) clearInterval(gameLoop)
})
</script>

<template>
  <div class="snake-game">
    <!-- 背景特效 -->
    <div class="bg-grid"></div>
    <div class="scanline"></div>

    <!-- 标题 -->
    <h1 class="neon-title">
      <GlowingText color="cyan" size="xl">CYBER SNAKE</GlowingText>
    </h1>

    <!-- 游戏容器 -->
    <div class="game-container">
      <!-- Canvas -->
      <GameCanvas
        :snake="snake"
        :food="food"
        :game-state="gameState"
      />

      <!-- 计分板 -->
      <ScoreBoard
        :score="score"
        :high-score="highScore"
      />

      <!-- 暂停状态 -->
      <div v-if="gameState === 'paused'" class="paused-overlay">
        PAUSED
      </div>

      <!-- 游戏结束弹窗 -->
      <Transition name="modal">
        <GameOverModal
          v-if="gameState === 'gameover'"
          :final-score="score"
          @restart="restartGame"
        />
      </Transition>
    </div>

    <!-- 控制提示 -->
    <div class="controls-hint">
      使用 ↑ ↓ ← → 方向键控制蛇的移动 | 空格键开始/暂停
    </div>
  </div>
</template>

<style scoped>
.snake-game {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  position: relative;
}

.neon-title {
  margin-bottom: 30px;
  text-align: center;
}

.game-container {
  background: var(--bg-primary);
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8),
              0 0 20px rgba(0, 255, 204, 0.1);
  border: 2px solid var(--neon-cyan);
  position: relative;
}

.paused-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 3rem;
  color: var(--neon-yellow);
  text-shadow: 0 0 20px var(--neon-yellow);
  animation: pulse 1s ease-in-out infinite;
  font-family: var(--font-tech);
  font-weight: bold;
  pointer-events: none;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.controls-hint {
  margin-top: 20px;
  color: #888;
  font-size: 0.9rem;
  text-align: center;
  font-family: var(--font-tech);
}

/* 模态框过渡 */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.8);
}
</style>
