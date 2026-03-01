<script setup lang="ts">
interface Props {
  text?: string
  variant?: 'primary' | 'secondary'
}

withDefaults(defineProps<Props>(), {
  text: '按钮',
  variant: 'primary'
})

const emit = defineEmits<{
  click: []
}>()

function handleClick() {
  emit('click')
}
</script>

<template>
  <button class="neon-button" :class="variant" @click="handleClick">
    <slot>{{ text }}</slot>
  </button>
</template>

<style scoped>
.neon-button {
  background: linear-gradient(135deg, var(--neon-green), #00cc6a);
  color: var(--bg-primary);
  border: none;
  padding: 12px 30px;
  font-size: 1rem;
  font-weight: bold;
  font-family: var(--font-tech);
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 0 15px rgba(0, 255, 136, 0.4);
  text-transform: uppercase;
  letter-spacing: 2px;
}

.neon-button:hover {
  transform: scale(1.05);
  box-shadow: 0 0 25px rgba(0, 255, 136, 0.6),
              0 0 40px rgba(0, 255, 136, 0.4);
}

.neon-button:active {
  transform: scale(0.95);
}

.neon-button.secondary {
  background: linear-gradient(135deg, var(--neon-cyan), #00ccaa);
}

.neon-button.secondary:hover {
  box-shadow: 0 0 25px rgba(0, 255, 204, 0.6),
              0 0 40px rgba(0, 255, 204, 0.4);
}
</style>
