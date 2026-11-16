<template>
  <router-link
    v-if="visivel"
    :to="destino"
    class="fab"
    :class="{ 'fab--alerta': emAlerta }"
    :aria-label="emAlerta ? 'Perigo de enchente: abrir rota de fuga' : 'Abrir rota de fuga'"
  >
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="6" cy="19" r="2.5" /><circle cx="18" cy="5" r="2.5" /><path d="M8.5 19H15a3.5 3.5 0 0 0 0-7H9a3.5 3.5 0 0 1 0-7h6.5" /></svg>
    <span>{{ emAlerta ? 'Perigo · Rota de fuga' : 'Rota de fuga' }}</span>
  </router-link>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useNiveis } from '@/composables/useNiveis'

/** Atalho fixo para a rota de fuga em todas as telas públicas (só no celular). */
const route = useRoute()
const { carregar, pontosEmAlerta } = useNiveis()

const OCULTO_EM = ['/rota-de-fuga', '/simulador', '/login', '/registro', '/minha-conta']
const visivel = computed(() => !OCULTO_EM.includes(route.path))
const emAlerta = computed(() => pontosEmAlerta.value.length > 0)
const destino = computed(() => emAlerta.value
  ? { path: '/rota-de-fuga', query: { ponto: pontosEmAlerta.value[0].id } }
  : { path: '/rota-de-fuga' })

onMounted(() => carregar())
</script>

<style scoped>
.fab {
  display: none;
  position: fixed; z-index: 950;
  right: 16px; bottom: calc(16px + env(safe-area-inset-bottom));
  align-items: center; gap: 8px;
  min-height: 56px; padding: 0 20px 0 16px;
  border-radius: var(--radius-full);
  background: var(--emergency); color: #fff;
  font-weight: 800; font-size: var(--fs-md); text-decoration: none;
  box-shadow: 0 6px 20px rgba(0, 0, 0, .45);
}
.fab--alerta { animation: fabPulse 1.6s ease-out infinite; }
@keyframes fabPulse {
  0% { box-shadow: 0 6px 20px rgba(0,0,0,.45), 0 0 0 0 rgba(220, 38, 38, .6); }
  100% { box-shadow: 0 6px 20px rgba(0,0,0,.45), 0 0 0 16px rgba(220, 38, 38, 0); }
}
@media (max-width: 768px) { .fab { display: inline-flex; } }
@media (prefers-reduced-motion: reduce) { .fab--alerta { animation: none; } }
</style>
