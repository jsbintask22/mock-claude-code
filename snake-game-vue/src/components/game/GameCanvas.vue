<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import type { SnakeSegment, Position } from '../../types/game'
import { useCanvas } from '../../composables/useCanvas'

interface Props {
  snake: SnakeSegment[]
  food: Position
  gameState: 'idle' | 'running' | 'paused' | 'gameover'
}

const props = defineProps<Props>()

const canvasRef = ref<HTMLCanvasElement | null>(null)
const { draw } = useCanvas(canvasRef)

const CONFIG = {
  gridSize: 20,
  tileCount: 20
}

// 初始化 canvas
onMounted(() => {
  if (canvasRef.value) {
    canvasRef.value.width = 400
    canvasRef.value.height = 400
    draw(props.snake, props.food, CONFIG.gridSize, CONFIG.tileCount)
  }
})

// 监听状态变化，重新绘制
watch([() => props.snake, () => props.food], () => {
  if (canvasRef.value) {
    draw(props.snake, props.food, CONFIG.gridSize, CONFIG.tileCount)
  }
}, { deep: true })
</script>

<template>
  <div class="canvas-wrapper">
    <canvas ref="canvasRef"></canvas>
  </div>
</template>

<style scoped>
.canvas-wrapper {
  position: relative;
}

canvas {
  border: 2px solid var(--neon-blue);
  border-radius: 8px;
  display: block;
  box-shadow: inset 0 0 20px rgba(0, 212, 255, 0.1);
}
</style>
