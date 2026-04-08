<template>
  <footer class="footer">
    <div class="footer-container">

      <div class="footer-grid">
        <!-- About -->
        <div class="footer-col">
          <div class="footer-brand">
            <div class="footer-logo">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>
              </svg>
            </div>
            <span>Hydro<span class="accent">Tech</span></span>
          </div>
          <p class="footer-desc">
            Plataforma web de monitoramento de riscos de enchentes em municípios brasileiros.
            Coleta dados de sensores ESP32 e APIs meteorológicas, classifica riscos e gera
            alertas preventivos via dashboard e WhatsApp.
          </p>
        </div>

        <!-- Links -->
        <div class="footer-col">
          <h4>Navegação</h4>
          <nav class="footer-nav">
            <router-link to="/">Início</router-link>
            <router-link to="/dashboard">Dashboard</router-link>
            <router-link to="/rios">Rios</router-link>
            <router-link to="/usuarios">Usuários</router-link>
          </nav>
        </div>


        <!-- Project -->
        <div class="footer-col">
          <h4>Projeto</h4>
          <div class="footer-info">
            <p>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>
              Projeto Interdisciplinar
            </p>
          </div>
        </div>
      </div>

      <div class="footer-divider"></div>

      <div class="footer-bottom">
        <p>&copy; {{ currentYear }} HydroTech — Sistema de Monitoramento de Riscos de Enchentes.</p>
      </div>

    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
const currentYear = computed(() => new Date().getFullYear())
</script>

<style scoped>
.footer {
  margin-top: auto;
  background: var(--bg-secondary);
  border-top: 1px solid var(--border);
}

.footer-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 48px 24px 24px;
}

.footer-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr 1fr;
  gap: 40px;
}

.footer-col h4 {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  margin-bottom: 16px;
}

/* Brand */
.footer-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.2rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.footer-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  background: var(--accent-gradient);
  color: white;
}

.accent {
  color: var(--accent);
}

.footer-desc {
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.7;
  max-width: 300px;
}

/* Nav */
.footer-nav {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.footer-nav a {
  text-decoration: none;
  color: var(--text-secondary);
  font-size: 0.875rem;
  font-weight: 500;
  transition: color var(--transition-fast);
}

.footer-nav a:hover {
  color: var(--accent);
}

/* Info */
.footer-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.footer-info p {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.footer-info svg {
  flex-shrink: 0;
  color: var(--text-muted);
}

/* Divider */
.footer-divider {
  height: 1px;
  margin: 32px 0 20px;
  background: linear-gradient(to right, transparent, var(--border), transparent);
}

/* Bottom */
.footer-bottom {
  text-align: center;
}

.footer-bottom p {
  font-size: 0.8rem;
  color: var(--text-muted);
}

/* Responsive */
@media (max-width: 768px) {
  .footer-grid {
    grid-template-columns: 1fr;
    gap: 32px;
  }
}
</style>