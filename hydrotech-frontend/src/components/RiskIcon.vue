<template>
  <svg :width="size" :height="size" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <template v-if="nivel === 'alto'">
      <path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z" />
      <path d="M12 9v4" /><path d="M12 17h.01" />
    </template>
    <template v-else-if="nivel === 'medio'">
      <circle cx="12" cy="12" r="10" /><path d="M12 8v4" /><path d="M12 16h.01" />
    </template>
    <template v-else>
      <circle cx="12" cy="12" r="10" /><path d="m8 12 3 3 5-6" />
    </template>
  </svg>
</template>

<script setup>
defineProps({
  nivel: { type: String, default: 'baixo' },
  size: { type: Number, default: 16 },
})
</script>
