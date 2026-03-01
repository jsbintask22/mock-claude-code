import { ref } from 'vue'
import type { SnakeSegment, Position, Direction, UpdateResult } from '../types/game'

export function useGameLogic(tileCount: number = 20) {
  const snake = ref<SnakeSegment[]>([])
  const food = ref<Position>({ x: 0, y: 0 })
  const direction = ref<Direction>({ dx: 1, dy: 0 })
  const nextDirection = ref<Direction>({ dx: 1, dy: 0 })
  const score = ref(0)

  // 初始化游戏
  function initGame() {
    snake.value = [
      { x: 10, y: 10 },
      { x: 9, y: 10 },
      { x: 8, y: 10 }
    ]
    direction.value = { dx: 1, dy: 0 }
    nextDirection.value = { dx: 1, dy: 0 }
    score.value = 0
    spawnFood()
  }

  // 生成食物
  function spawnFood() {
    do {
      food.value = {
        x: Math.floor(Math.random() * tileCount),
        y: Math.floor(Math.random() * tileCount)
      }
    } while (snake.value.some(segment =>
      segment.x === food.value.x && segment.y === food.value.y
    ))
  }

  // 更新方向
  function updateDirection(newDir: Direction) {
    // 防止反向移动
    if (direction.value.dx !== 0 && newDir.dx !== 0) return
    if (direction.value.dy !== 0 && newDir.dy !== 0) return
    nextDirection.value = newDir
  }

  // 更新游戏状态
  function update(): UpdateResult {
    direction.value = { ...nextDirection.value }

    // 计算新蛇头位置
    const head = {
      x: snake.value[0].x + direction.value.dx,
      y: snake.value[0].y + direction.value.dy
    }

    // 检查墙壁碰撞
    if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
      return { gameOver: true, ateFood: false }
    }

    // 检查自身碰撞
    if (snake.value.some(segment => segment.x === head.x && segment.y === head.y)) {
      return { gameOver: true, ateFood: false }
    }

    // 添加新蛇头
    snake.value.unshift(head)

    // 检查是否吃到食物
    if (head.x === food.value.x && head.y === food.value.y) {
      score.value += 10
      spawnFood()
      return { gameOver: false, ateFood: true }
    } else {
      snake.value.pop()
    }

    return { gameOver: false, ateFood: false }
  }

  return {
    snake,
    food,
    direction,
    score,
    initGame,
    spawnFood,
    updateDirection,
    update
  }
}
