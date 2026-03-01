export interface SnakeSegment {
  x: number
  y: number
}

export interface Position {
  x: number
  y: number
}

export interface Direction {
  dx: number
  dy: number
}

export type GameState = 'idle' | 'running' | 'paused' | 'gameover'

export interface GameConfig {
  gridSize: number
  tileCount: number
  canvasSize: number
  initialSpeed: number
  minSpeed: number
  speedIncrement: number
}

export interface UpdateResult {
  gameOver: boolean
  ateFood: boolean
}
