<template>
  <section class="nf">
    <span class="nf-icon" aria-hidden="true">
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8" /><path d="m21 21-4.3-4.3" /><path d="M8 11h6" /></svg>
    </span>
    <h1>Página não encontrada</h1>
    <p>O endereço que você abriu não existe ou mudou de lugar.</p>
    <div class="nf-actions">
      <router-link to="/" class="btn btn--primary btn--lg">Voltar ao início</router-link>
      <router-link to="/monitoramento" class="btn btn--ghost btn--lg">Ver os rios</router-link>
    </div>
    <p class="nf-help">Em uma emergência, use o botão <b>Rota de fuga</b> ou ligue <b>199</b> (Defesa Civil).</p>
  </section>
</template>

<script setup>
import { onMounted } from 'vue'
onMounted(() => { document.title = 'Página não encontrada · HydroTech' })
</script>

<style scoped>
.nf {
  min-height: calc(100dvh - var(--landing-header-h) - 200px);
  max-width: 560px; margin: 0 auto; padding: 56px 20px;
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 14px; text-align: center;
}
.nf-icon { width: 80px; height: 80px; border-radius: 50%; display: grid; place-items: center; background: var(--accent-soft); color: var(--accent); }
.nf h1 { font-size: var(--fs-xl); }
.nf p { color: var(--text-secondary); }
.nf-actions { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-top: 8px; }
.nf-help { font-size: var(--fs-sm); margin-top: 12px; }
@media (max-width: 480px) { .nf-actions { width: 100%; flex-direction: column; } }
</style>
