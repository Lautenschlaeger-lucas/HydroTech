<template>
  <div class="landing">

    <!-- Hero + Overlap Section -->
    <section class="hero-overlap-section">
      <div class="hero-bg" style="background-image: url('/images/hero_bg.jpg')">
        <div class="hero-overlay"></div>
      </div>
      
      <div class="hero-content animate-fade-in-up">
        <h1 class="hero-title">HydroTech:<br>Proteção e Resiliência em sua cidade.</h1>
        <p class="hero-subtitle">
          A plataforma HydroTech oferece monitoramento contínuo do nível dos rios e gestão de riscos meteorológicos para garantir a segurança de toda a comunidade.
        </p>
      </div>

      <!-- Overlap Grid -->
      <div class="overlap-grid-container">
        <div class="overlap-card" v-for="(card, i) in overlapCards" :key="i">
          <div class="overlap-icon" v-html="card.icon"></div>
          <div class="overlap-text">
            <h3>{{ card.title }}</h3>
            <p>{{ card.desc }}</p>
          </div>
        </div>
      </div>
    </section>


    <!-- Features (Mantido) -->
    <section class="features">
      <div class="features-container">
        <div class="section-header">
          <span class="section-tag">Funcionalidades</span>
          <h2>Como o sistema protege sua região?</h2>
          <p>Integração entre coleta automática de dados, análise de risco configurável e alertas preventivos</p>
        </div>

        <div class="feature-grid">
          <div class="feature-card" v-for="(feature, i) in features" :key="i" :style="{ animationDelay: (i * 0.1) + 's' }">
            <div class="feature-icon-wrap">
              <div class="feature-icon" v-html="feature.icon"></div>
            </div>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Audience (Mantido) -->
    <section class="audience-section">
      <div class="audience-container">
        <div class="section-header">
          <span class="section-tag">Para quem</span>
          <h2>Quem pode usar o HydroTech?</h2>
          <p>A plataforma atende diferentes perfis de usuário</p>
        </div>

        <div class="audience-grid">
          <div class="audience-card" v-for="(audience, i) in audiences" :key="i">
            <div class="audience-icon" v-html="audience.icon"></div>
            <h3>{{ audience.title }}</h3>
            <p>{{ audience.desc }}</p>
            <ul>
              <li v-for="(item, j) in audience.items" :key="j">{{ item }}</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA (Mantido) -->
    <section class="cta-section">
      <div class="cta-container">
        <div class="cta-card">
          <h2>Pronto para proteger sua região?</h2>
          <p>Cadastre-se e receba alertas de enchente em tempo real. Monitore rios, acompanhe o clima e proteja sua comunidade.</p>
          <router-link to="/registro" class="btn-cta-large">
            Começar Agora
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </router-link>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref } from 'vue'

const overlapCards = ref([
  {
    title: 'Atendimento e Consulta',
    desc: 'Solicite vistorias, consulte processos e tire dúvidas sobre áreas de risco.',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
  },
  {
    title: 'Abrigos',
    desc: 'Localização em tempo real e capacidade dos abrigos públicos disponíveis.',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
  },
  {
    title: 'Histórico',
    desc: 'Acesse o banco de dados histórico de ocorrências e níveis dos rios.',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
  },
  {
    title: 'Plano de Contingência',
    desc: 'Documentação técnica e protocolos de ação para diferentes cenários de risco.',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>'
  }
])



// Features originais mantidos
const features = ref([
  {
    title: 'Sensores',
    desc: 'Sensores acoplados, que medem o nível do rio em tempo real e envia os dados via Wi-Fi diretamente à API do sistema.',
    icon: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6 8-2-2"/><path d="m18 8 2-2"/><path d="m6 16-2 2"/><path d="m18 16 2 2"/><path d="M12 2v2"/><path d="M12 20v2"/><circle cx="12" cy="12" r="4"/></svg>'
  },
  {
    title: 'Dados Meteorológicos',
    desc: 'Integração com APIs externas de precipitação e previsão do tempo, coletando volume de chuva acumulado e previsão para as próximas horas.',
    icon: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>'
  },
  {
    title: 'Análise de Risco',
    desc: 'Classificação automática em 3 níveis — baixo, médio e alto — com base no nível do rio, precipitação acumulada e previsão de chuva. Limites configuráveis pelo administrador.',
    icon: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>'
  },
  {
    title: 'Dashboard Interativo',
    desc: 'Painel com indicador visual do nível do rio, gráficos históricos de evolução da água, indicadores de chuva e painel de alertas ativos e histórico.',
    icon: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>'
  },
  {
    title: 'Alertas no Painel',
    desc: 'Alertas visuais de chuva intensa, elevação do nível do rio e risco de enchente iminente. Onde os risco são exibido no dashboard.',
    icon: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
  }
])

// Audiences originais mantidos
const audiences = ref([
  {
    title: 'Gestores Públicos',
    desc: 'Administradores e equipes de Defesa Civil que precisam monitorar riscos e tomar decisões preventivas.',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    items: [
      'Configurar limites de risco (médio e alto)',
      'Visualizar histórico de medições para decisões de evacuação',
      'Gerenciar usuários e acessos da plataforma'
    ]
  },
  {
    title: 'Cidadãos',
    desc: 'Moradores de regiões monitoradas que desejam estar informados sobre o risco de enchentes.',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    items: [
      'Acessar o dashboard e ver o nível atual do rio',
      'Receber alertas de risco alto via WhatsApp ou E-Mail',
      'Acompanhar previsão de chuva e situação da região'
    ]
  }
])
</script>

<style scoped>
.landing {
  width: 100%;
  display: flex;
  flex-direction: column;
}

/* ═══ HERO OVERLAP SECTION ═══ */
.hero-overlap-section {
  position: relative;
  width: 100%;
}

.hero-bg {
  position: relative;
  width: 100%;
  min-height: 80vh;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  flex-direction: column;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, rgba(11, 29, 53, 0.4) 0%, rgba(11, 29, 53, 0.8) 70%, var(--bg-primary) 100%);
  z-index: 1;
}

.hero-content {
  position: absolute;
  top: 15%;
  left: 10%;
  z-index: 2;
  max-width: 800px;
}

.hero-title {
  font-size: 3.8rem;
  font-weight: 800;
  color: #FFFFFF;
  line-height: 1.1;
  letter-spacing: -0.03em;
  margin-bottom: 20px;
}

.hero-subtitle {
  font-size: 1.15rem;
  color: #CBD5E1;
  max-width: 500px;
  line-height: 1.6;
}

/* OVERLAP GRID */
.overlap-grid-container {
  position: absolute;
  bottom: -40px; /* Sobrepõe pra fora do hero */
  left: 0;
  right: 0;
  z-index: 10;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.overlap-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 24px;
  box-shadow: var(--shadow-sm);
  display: flex;
  gap: 16px;
  transition: transform var(--transition-normal), border-color var(--transition-normal);
}

.overlap-card:hover {
  transform: translateY(-4px);
  border-color: var(--accent);
  box-shadow: var(--shadow-md);
}

.overlap-icon {
  background: var(--accent-soft);
  color: var(--accent);
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.overlap-text h3 {
  font-size: 1.05rem;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.overlap-text p {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* ═══ NEWS E ALERTAS ═══ */
.news-alerts-section {
  background: #F8FAFC;
  padding: 140px 24px 80px; /* Padding top enorme devido ao overlap grid */
  width: 100%;
}

.news-alerts-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 40px;
}

.news-col {
  flex: 2;
}

.alerts-col {
  flex: 1;
}

.section-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  border-bottom: 2px solid #E2E8F0;
  padding-bottom: 16px;
}

.section-header-row h2 {
  font-size: 1.8rem;
  color: var(--text-primary);
  font-weight: 800;
  letter-spacing: -0.02em;
}

.view-all {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-secondary);
  text-decoration: none;
}

.view-all:hover {
  color: var(--accent);
}

.news-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.news-card {
  display: flex;
  gap: 24px;
  background: #fff;
  border-radius: var(--radius-lg);
  padding: 20px;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s;
}

.news-card:hover {
  transform: translateX(4px);
  box-shadow: var(--shadow-md);
}

.news-img-wrap {
  width: 200px;
  height: 130px;
  border-radius: var(--radius-md);
  overflow: hidden;
  flex-shrink: 0;
}

.news-img-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.news-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.news-date {
  font-size: 0.75rem;
  font-weight: 700;
  color: #F97316;
  letter-spacing: 0.05em;
  margin-bottom: 8px;
}

.news-content h3 {
  font-size: 1.25rem;
  color: var(--text-primary);
  margin-bottom: 10px;
  line-height: 1.3;
}

.news-content p {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* Alertas Panel */
.alerts-panel {
  background: #F1F5F9;
  border-radius: var(--radius-xl);
  padding: 30px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.alerts-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.1rem;
  color: var(--text-primary);
  margin-bottom: 24px;
}

.alert-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 30px;
  flex-grow: 1;
}

.alert-card {
  background: #fff;
  border-radius: var(--radius-md);
  padding: 16px;
  border-left: 4px solid #F97316;
  box-shadow: var(--shadow-sm);
}

.alert-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.alert-type {
  font-size: 0.7rem;
  font-weight: 700;
  color: #F97316;
}

.alert-date {
  font-size: 0.7rem;
  color: #94A3B8;
}

.alert-card h4 {
  font-size: 1rem;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.alert-card p {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.4;
}

.btn-block-gray {
  width: 100%;
  padding: 14px;
  background: #E2E8F0;
  border: none;
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-block-gray:hover {
  background: #CBD5E1;
}

/* ═══ MANTIDOS (Features, Audience, CTA) ═══ */
.features {
  padding: 96px 24px;
  background: var(--bg-primary);
}

.features-container {
  max-width: 1100px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 56px;
}

.section-tag {
  display: inline-block;
  padding: 4px 14px;
  border-radius: var(--radius-full);
  background: var(--accent-soft);
  color: var(--accent);
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 16px;
}

.section-header h2 {
  font-size: 2.4rem;
  color: var(--text-primary);
  margin-bottom: 12px;
  letter-spacing: -0.02em;
}

.section-header p {
  font-size: 1.05rem;
  color: var(--text-secondary);
  max-width: 500px;
  margin: 0 auto;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.feature-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 36px 28px;
  transition: transform var(--transition-normal);
}

.feature-card:hover {
  transform: translateY(-6px);
  border-color: var(--accent);
}

.feature-icon-wrap {
  margin-bottom: 20px;
}

.feature-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 52px;
  height: 52px;
  border-radius: var(--radius-lg);
  background: var(--accent-soft);
  color: var(--accent);
}

.feature-card h3 {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 10px;
}

.feature-card p {
  font-size: 0.925rem;
  color: var(--text-secondary);
  line-height: 1.7;
}

.audience-section {
  padding: 96px 24px;
  background: var(--bg-secondary);
}

.audience-container {
  max-width: 900px;
  margin: 0 auto;
}

.audience-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.audience-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 36px 28px;
}

.audience-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  border-radius: var(--radius-lg);
  background: var(--accent-soft);
  color: var(--accent);
  margin-bottom: 18px;
}

.audience-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.audience-card > p {
  font-size: 0.925rem;
  color: var(--text-secondary);
  line-height: 1.65;
  margin-bottom: 16px;
}

.audience-card ul {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.audience-card li {
  font-size: 0.875rem;
  color: var(--text-secondary);
  padding-left: 20px;
  position: relative;
  line-height: 1.5;
}

.audience-card li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 7px;
  width: 8px;
  height: 8px;
  border-radius: var(--radius-full);
  background: var(--accent);
  opacity: 0.6;
}

.cta-section {
  padding: 0 24px 96px;
  background: var(--bg-secondary);
}

.cta-container {
  max-width: 800px;
  margin: 0 auto;
}

.cta-card {
  text-align: center;
  padding: 56px 40px;
  border-radius: var(--radius-xl);
  background: linear-gradient(145deg, var(--accent-dark), #0F2847);
  position: relative;
  overflow: hidden;
}

.cta-card::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -30%;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  background: rgba(41, 171, 226, 0.08);
}

.cta-card h2 {
  font-size: 2rem;
  color: #FFFFFF;
  margin-bottom: 12px;
  position: relative;
}

.cta-card p {
  font-size: 1.05rem;
  color: #94A3B8;
  margin-bottom: 28px;
  position: relative;
}

.btn-cta-large {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 16px 32px;
  border-radius: var(--radius-md);
  background: var(--accent-gradient);
  color: white;
  text-decoration: none;
  font-weight: 700;
  font-size: 1.05rem;
  position: relative;
}

/* ═══ RESPONSIVE COMPLEMENTO ═══ */

@media (max-width: 1024px) {
  .hero-content { left: 5%; }
  
  .overlap-grid-container {
    flex-direction: column;
    position: relative;
    bottom: 0;
    margin-top: -80px;
  }
  
  .news-alerts-container {
    flex-direction: column;
  }
}

@media (max-width: 768px) {
  .hero-title { font-size: 2.5rem; }
  .overlap-left { grid-template-columns: 1fr; }
  .news-card { flex-direction: column; }
  .news-img-wrap { width: 100%; height: 180px; }
  .feature-grid, .audience-grid { grid-template-columns: 1fr; }
}

</style>