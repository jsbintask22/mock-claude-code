<script setup lang="ts">
interface Props {
  text?: string
  color?: 'cyan' | 'pink' | 'green' | 'blue' | 'purple'
  size?: 'sm' | 'md' | 'lg' | 'xl'
}

withDefaults(defineProps<Props>(), {
  text: '',
  color: 'cyan',
  size: 'md'
})
</script>

<template>
  <span class="glowing-text" :class="[color, size]">
    <slot>{{ text }}</slot>
  </span>
</template>

<style scoped>
.glowing-text {
  display: inline-block;
  animation: neon-flicker 3s infinite;
}

.glowing-text.cyan {
  color: var(--neon-cyan);
  text-shadow: 0 0 10px var(--neon-cyan), 0 0 20px var(--neon-cyan);
}

.glowing-text.pink {
  color: var(--neon-pink);
  text-shadow: 0 0 10px var(--neon-pink), 0 0 20px var(--neon-pink);
}

.glowing-text.green {
  color: var(--neon-green);
  text-shadow: 0 0 10px var(--neon-green), 0 0 20px var(--neon-green);
}

.glowing-text.blue {
  color: var(--neon-blue);
  text-shadow: 0 0 10px var(--neon-blue), 0 0 20px var(--neon-blue);
}

.glowing-text.purple {
  color: var(--neon-purple);
  text-shadow: 0 0 10px var(--neon-purple), 0 0 20px var(--neon-purple);
}

.glowing-text.sm { font-size: 1rem; }
.glowing-text.md { font-size: 1.5rem; }
.glowing-text.lg { font-size: 2rem; }
.glowing-text.xl { font-size: 3rem; }

@keyframes neon-flicker {
  0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {
    text-shadow: inherit;
  }
  20%, 24%, 55% {
    text-shadow: none;
  }
}
</style>
