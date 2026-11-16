<template>
  <template v-if="!isDefesaCivil">
    <template v-if="isLoggedIn">
      <button class="btn btn--ghost btn--sm" :class="{ 'is-on is-fav': isFav(ponto.id) }" type="button" :aria-pressed="isFav(ponto.id)" @click="toggleFav(ponto.id)">
        <svg width="15" height="15" viewBox="0 0 24 24" :fill="isFav(ponto.id) ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" /></svg>
        {{ isFav(ponto.id) ? 'Favorito' : 'Favoritar' }}
      </button>
      <button class="btn btn--ghost btn--sm" :class="{ 'is-on is-alert': isAlert(ponto.id) }" type="button" :aria-pressed="isAlert(ponto.id)" @click="toggleAlert(ponto.id)">
        <svg width="15" height="15" viewBox="0 0 24 24" :fill="isAlert(ponto.id) ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" /><path d="M13.73 21a2 2 0 0 1-3.46 0" /></svg>
        {{ isAlert(ponto.id) ? 'Alertas ligados' : 'Receber alertas' }}
      </button>
    </template>
    <router-link v-else to="/registro" class="btn btn--ghost btn--sm" title="Crie uma conta para favoritar e receber alertas">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" /><path d="M13.73 21a2 2 0 0 1-3.46 0" /></svg>
      Receber alertas
    </router-link>
  </template>
</template>

<script setup>
import { useFavoritos } from '@/composables/useFavoritos'

defineProps({ ponto: { type: Object, required: true } })
const { isLoggedIn, isDefesaCivil, isFav, isAlert, toggleFav, toggleAlert } = useFavoritos()
</script>

<style scoped>
.is-fav   { color: var(--risk-medium-text); border-color: var(--risk-medium-solid); background: var(--risk-medium-bg); }
.is-alert { color: var(--accent); border-color: var(--accent); background: var(--accent-soft); }
</style>
