<script setup lang="ts">
import GlowingText from '../ui/GlowingText.vue'

interface Props {
  score: number
  highScore: number
}

defineProps<Props>()
</script>

<template>
  <div class="info-panel">
    <div class="score-display">
      得分: <GlowingText color="cyan">{{ score }}</GlowingText>
    </div>
    <div class="score-display">
      最高分: <GlowingText color="green">{{ highScore }}</GlowingText>
    </div>
  </div>
</template>

<style scoped>
.info-panel {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
  color: var(--neon-white);
}

.score-display {
  font-size: 1.2rem;
  font-family: var(--font-tech);
}
</style>
