<script setup lang="ts">
import NeonButton from '../ui/NeonButton.vue'
import GlowingText from '../ui/GlowingText.vue'

interface Props {
  finalScore: number
}

defineProps<Props>()

const emit = defineEmits<{
  restart: []
}>()
</script>

<template>
  <div class="game-over-modal">
    <GlowingText color="pink" size="xl">游戏结束!</GlowingText>
    <p>你的得分: <GlowingText color="cyan" size="md">{{ finalScore }}</GlowingText></p>
    <NeonButton @click="emit('restart')">重新开始</NeonButton>
  </div>
</template>

<style scoped>
.game-over-modal {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(10, 10, 26, 0.95);
  border: 2px solid var(--neon-pink);
  border-radius: 15px;
  padding: 40px;
  text-align: center;
  box-shadow: 0 0 30px rgba(255, 51, 102, 0.3);
  backdrop-filter: blur(10px);
  z-index: 100;
  min-width: 250px;
}

.game-over-modal h2 {
  margin-bottom: 15px;
}

.game-over-modal p {
  color: var(--neon-white);
  margin: 20px 0;
  font-size: 1.2rem;
  font-family: var(--font-tech);
}
</style>
