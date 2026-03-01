import { computed, type Ref } from 'vue'
import type { SnakeSegment, Position } from '../types/game'

export function useCanvas(canvasRef: Ref<HTMLCanvasElement | null>) {
  const ctx = computed(() => canvasRef.value?.getContext('2d'))

  let pulsePhase = 0

  // 绘制网格
  function drawGrid(gridSize: number, tileCount: number) {
    if (!ctx.value) return

    ctx.value.strokeStyle = 'rgba(0, 212, 255, 0.1)'
    ctx.value.lineWidth = 0.5

    for (let i = 0; i <= tileCount; i++) {
      ctx.value.beginPath()
      ctx.value.moveTo(i * gridSize, 0)
      ctx.value.lineTo(i * gridSize, 400)
      ctx.value.stroke()

      ctx.value.beginPath()
      ctx.value.moveTo(0, i * gridSize)
      ctx.value.lineTo(400, i * gridSize)
      ctx.value.stroke()
    }
  }

  // 绘制蛇
  function drawSnake(snake: SnakeSegment[], gridSize: number) {
    if (!ctx.value) return

    snake.forEach((segment, index) => {
      if (index === 0) {
        // 蛇头 - 霓虹青色发光效果
        ctx.value.fillStyle = '#00ffcc'
        ctx.value.shadowColor = '#00ffcc'
        ctx.value.shadowBlur = 15
      } else {
        // 蛇身 - 渐变效果
        const brightness = Math.max(50, 100 - index * 3)
        ctx.value.fillStyle = `rgba(${brightness}, ${brightness + 20}, ${brightness + 50}, 0.9)`
        ctx.value.shadowBlur = 0
      }

      ctx.value.fillRect(
        segment.x * gridSize + 1,
        segment.y * gridSize + 1,
        gridSize - 2,
        gridSize - 2
      )

      ctx.value.shadowBlur = 0
    })
  }

  // 绘制食物（带脉冲效果）
  function drawFood(food: Position, gridSize: number) {
    if (!ctx.value) return

    pulsePhase += 0.1
    const pulse = 1 + Math.sin(pulsePhase) * 0.1
    const radius = (gridSize / 2 - 2) * pulse

    ctx.value.fillStyle = '#ff3366'
    ctx.value.shadowColor = '#ff3366'
    ctx.value.shadowBlur = 15 + pulse * 10

    ctx.value.beginPath()
    ctx.value.arc(
      food.x * gridSize + gridSize / 2,
      food.y * gridSize + gridSize / 2,
      radius,
      0,
      Math.PI * 2
    )
    ctx.value.fill()
    ctx.value.shadowBlur = 0
  }

  // 清空画布
  function clearCanvas(width: number, height: number) {
    if (!ctx.value) return
    ctx.value.fillStyle = '#0a0a1a'
    ctx.value.fillRect(0, 0, width, height)
  }

  // 主绘制函数
  function draw(snake: SnakeSegment[], food: Position, gridSize: number, tileCount: number) {
    clearCanvas(400, 400)
    drawGrid(gridSize, tileCount)
    drawSnake(snake, gridSize)
    drawFood(food, gridSize)
  }

  return { draw, clearCanvas, drawGrid, drawSnake, drawFood }
}
