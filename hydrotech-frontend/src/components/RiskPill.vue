<template>
  <span class="risk-pill" :class="'risk-pill--' + risco.nivel">
    <RiskIcon :nivel="risco.nivel" :size="size" />
    <span>{{ texto ?? risco.rotulo }}</span>
  </span>
</template>

<script setup>
import RiskIcon from './RiskIcon.vue'

defineProps({
  risco: { type: Object, required: true },
  texto: { type: String, default: null },
  size: { type: Number, default: 14 },
})
</script>
