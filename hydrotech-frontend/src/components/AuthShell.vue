<template>
  <div class="auth">
    <aside class="auth-why" aria-label="Por que ter uma conta">
      <h2>Com uma conta você:</h2>
      <ul>
        <li>
          <span class="auth-ico" aria-hidden="true"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" /><path d="M13.73 21a2 2 0 0 1-3.46 0" /></svg></span>
          <span><b>Recebe alertas</b> quando o rio perto de você subir</span>
        </li>
        <li>
          <span class="auth-ico" aria-hidden="true"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" /></svg></span>
          <span><b>Salva os seus rios</b> para ver tudo em um toque</span>
        </li>
        <li>
          <span class="auth-ico" aria-hidden="true"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="19" r="2.5" /><circle cx="18" cy="5" r="2.5" /><path d="M8.5 19H15a3.5 3.5 0 0 0 0-7H9a3.5 3.5 0 0 1 0-7h6.5" /></svg></span>
          <span>A <b>rota de fuga</b> continua aberta para todos, com ou sem conta</span>
        </li>
      </ul>
      <router-link to="/monitoramento" class="auth-skip">Ver os rios sem entrar →</router-link>
    </aside>

    <section class="auth-card">
      <header class="auth-head">
        <h1>{{ titulo }}</h1>
        <p v-if="subtitulo">{{ subtitulo }}</p>
      </header>
      <slot />
      <footer class="auth-foot"><slot name="rodape" /></footer>
    </section>
  </div>
</template>

<script setup>
defineProps({
  titulo: { type: String, required: true },
  subtitulo: { type: String, default: '' },
})
</script>

<style scoped>
.auth {
  min-height: calc(100dvh - var(--landing-header-h));
  display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 440px);
  gap: 48px; align-items: center;
  max-width: 1040px; margin: 0 auto; padding: 40px 24px;
}
.auth-why h2 { font-size: var(--fs-xl); margin-bottom: 20px; }
.auth-why ul { list-style: none; display: flex; flex-direction: column; gap: 16px; }
.auth-why li { display: flex; align-items: center; gap: 14px; font-size: var(--fs-md); color: var(--text-secondary); line-height: 1.4; }
.auth-why b { color: var(--text-primary); }
.auth-ico { width: 44px; height: 44px; flex-shrink: 0; border-radius: var(--radius-lg); display: grid; place-items: center; background: var(--accent-soft); color: var(--accent); }
.auth-skip { display: inline-block; margin-top: 24px; color: var(--accent); font-weight: 700; font-size: var(--fs-sm); }

.auth-card {
  display: flex; flex-direction: column; gap: 20px;
  padding: 28px; border-radius: var(--radius-2xl);
  background: var(--bg-card); border: 1px solid var(--border); box-shadow: var(--shadow-lg);
}
.auth-head h1 { font-size: var(--fs-xl); }
.auth-head p { color: var(--text-secondary); font-size: var(--fs-sm); margin-top: 4px; }
.auth-foot { padding-top: 16px; border-top: 1px solid var(--border-light); font-size: var(--fs-sm); color: var(--text-secondary); text-align: center; }
.auth-foot :deep(a) { color: var(--accent); font-weight: 700; }

/* Campos (usados pelas telas dentro do slot) */
.auth :deep(.f) { display: flex; flex-direction: column; gap: 6px; }
.auth :deep(.f label) { font-size: var(--fs-sm); font-weight: 700; color: var(--text-primary); }
.auth :deep(.f small) { font-size: var(--fs-xs); color: var(--text-muted); }
.auth :deep(.f input) { min-height: var(--tap); font-size: var(--fs-md); }
.auth :deep(.f--erro input) { border-color: var(--risk-high); }
.auth :deep(.f-msg) { font-size: var(--fs-xs); color: var(--risk-high-text); }
.auth :deep(.f-pass) { position: relative; }
.auth :deep(.f-pass input) { padding-right: 52px; }
.auth :deep(.f-eye) {
  position: absolute; right: 4px; top: 50%; transform: translateY(-50%);
  width: 44px; height: 44px; border-radius: var(--radius-md); background: transparent; color: var(--text-muted);
}
.auth :deep(.f-eye:hover:not(:disabled)) { transform: translateY(-50%); color: var(--text-primary); }
.auth :deep(.form) { display: flex; flex-direction: column; gap: 16px; }
.auth :deep(.form-erro) { padding: 12px 14px; border-radius: var(--radius-md); background: var(--risk-high-bg); color: var(--risk-high-text); font-size: var(--fs-sm); font-weight: 600; }
.auth :deep(.form-ok) { padding: 12px 14px; border-radius: var(--radius-md); background: var(--risk-low-bg); color: var(--risk-low-text); font-size: var(--fs-sm); font-weight: 600; }
.auth :deep(.seg2) { display: grid; grid-template-columns: 1fr 1fr; padding: 4px; gap: 4px; border-radius: var(--radius-lg); background: var(--bg-secondary); border: 1px solid var(--border); }
.auth :deep(.seg2 button) { min-height: 42px; border-radius: var(--radius-md); background: transparent; color: var(--text-secondary); font-size: var(--fs-sm); }
.auth :deep(.seg2 button:hover:not(:disabled)) { transform: none; color: var(--text-primary); }
.auth :deep(.seg2 button.on) { background: var(--accent); color: var(--on-accent); }

@media (max-width: 860px) {
  .auth { grid-template-columns: 1fr; gap: 20px; padding: 20px 16px 32px; align-items: start; }
  .auth-card { order: -1; padding: 20px; }
  .auth-why { padding: 0 4px; }
  .auth-why h2 { font-size: var(--fs-lg); margin-bottom: 12px; }
}
</style>
