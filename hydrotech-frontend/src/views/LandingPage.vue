<template>
  <div class="landing">

    <!-- ═══ HERO ═══ -->
    <section class="hero">
      <div class="hero-inner">
        <span class="hero-badge">MONITORAMENTO DE ENCHENTES</span>
        <h1 class="hero-title">Veja se o rio perto de você <br>está seguro</h1>
        <p class="hero-subtitle">
          O HydroTech acompanha o nível dos rios da sua cidade e avisa quando há risco de enchente.
          Se houver perigo, mostra o caminho mais seguro para sair.
        </p>
        <router-link v-if="pontosEmAlerta.length" :to="{ path: '/rota-de-fuga', query: { ponto: pontosEmAlerta[0].id } }" class="hero-alert" role="alert">
          <RiskIcon nivel="alto" :size="20" />
          <span><strong>Perigo de enchente</strong> · {{ pontosEmAlerta[0].descricao }}</span>
          <b>Rota de fuga →</b>
        </router-link>
        <div class="hero-actions">
          <router-link :to="{ path: '/monitoramento', query: { perto: 1 } }" class="btn btn--primary btn--lg hero-cta">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z" /><circle cx="12" cy="10" r="3" /></svg>
            Ver o rio da minha região
          </router-link>
          <router-link to="/rota-de-fuga" class="btn btn--danger btn--lg hero-cta">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="6" cy="19" r="2.5" /><circle cx="18" cy="5" r="2.5" /><path d="M8.5 19H15a3.5 3.5 0 0 0 0-7H9a3.5 3.5 0 0 1 0-7h6.5" /></svg>
            Rota de fuga
          </router-link>
        </div>
        <a href="#servicos" class="hero-more">Saiba mais sobre o HydroTech ↓</a>
      </div>
    </section>

    <!-- ═══ SERVIÇOS INSTITUCIONAIS ═══ -->
    <section id="servicos" class="services-section">
      <div class="services-inner">
        <div class="services-header">
          <h2>Serviços</h2>
          <p>Atendimento, abrigos e informações da Defesa Civil em um só lugar.</p>
        </div>
        <div class="services-grid">
          <div class="service-card" v-for="(s, i) in services" :key="i">
            <div class="service-icon" v-html="s.icon"></div>
            <h3>{{ s.title }}</h3>
            <p>{{ s.desc }}</p>
            <!-- Só vira link quando houver um destino real; até lá, fica marcado como "Em breve" -->
            <a v-if="s.link && s.link !== '#'" :href="s.link" class="service-link">{{ s.linkText || 'Acessar' }} <span class="arrow">→</span></a>
            <span v-else class="service-soon">Em breve</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══ FEATURES (BENTO GRID) ═══ -->
    <section class="features-section" @pointermove="handleFeaturePointerMove" @pointerleave="resetFeatureParallax">
      <div class="features-inner">
        <div class="features-header">
          <h2>Como o HydroTech protege sua região?</h2>
          <p>Sensores, previsão do tempo e alertas trabalhando juntos.</p>
        </div>
        <div class="bento-grid">
          <div class="bento-card bento-sm" v-for="(f, i) in features.slice(0,2)" :key="'a'+i">
            <div class="bento-icon" v-html="f.icon"></div>
            <h3>{{ f.title }}</h3>
            <p>{{ f.desc }}</p>
          </div>
          <div class="bento-card bento-sm">
            <div class="bento-icon" v-html="features[2].icon"></div>
            <h3>{{ features[2].title }}</h3>
            <p>{{ features[2].desc }}</p>
          </div>
          <div class="bento-card bento-lg">
            <div class="bento-icon" v-html="features[3].icon"></div>
            <h3>{{ features[3].title }}</h3>
            <p>{{ features[3].desc }}</p>
          </div>
          <div class="bento-card bento-full">
            <div class="bento-icon" v-html="features[4].icon"></div>
            <h3>{{ features[4].title }}</h3>
            <p>{{ features[4].desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══ AUDIENCE ═══ -->
    <section id="contingencia" class="audience-section">
      <div class="audience-inner">
        <div class="audience-header">
          <h2>Quem pode usar o HydroTech?</h2>
        </div>
        <div class="audience-grid">
          <div class="audience-card" v-for="(a, i) in audiences" :key="i">
            <div class="audience-icon" v-html="a.icon"></div>
            <h3>{{ a.title }}</h3>
            <ul>
              <li v-for="(item, j) in a.items" :key="j">
                <svg class="check" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                {{ item }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══ CTA ═══ -->
    <section class="cta-section">
      <div class="cta-inner">
        <h2>Receba alertas da sua região</h2>
        <p>Crie sua conta grátis e seja avisado quando o rio perto de você subir.</p>
        <router-link :to="isLoggedIn ? '/minha-conta' : '/registro'" class="btn-cta">{{ isLoggedIn ? 'Minha conta' : 'Criar conta grátis' }}</router-link>
      </div>
    </section>

  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import RiskIcon from '@/components/RiskIcon.vue'
import { useNiveis } from '@/composables/useNiveis'

const { carregar: carregarNiveis, pontosEmAlerta } = useNiveis()

const isLoggedIn = ref(!!localStorage.getItem('user_token'))
const observer = ref(null)
let parallaxFrame = null
let featureElement = null
let pointerX = 0
let pointerY = 0

const paintFeatureParallax = () => {
  featureElement?.style.setProperty('--mouse-x', `${pointerX}px`)
  featureElement?.style.setProperty('--mouse-y', `${pointerY}px`)
  parallaxFrame = null
}

const handleFeaturePointerMove = (event) => {
  if (event.pointerType === 'touch' || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
  featureElement = event.currentTarget
  pointerX = (event.clientX - window.innerWidth / 2) * -0.05
  pointerY = (event.clientY - window.innerHeight / 2) * -0.05
  if (parallaxFrame === null) parallaxFrame = requestAnimationFrame(paintFeatureParallax)
}

const resetFeatureParallax = () => {
  if (parallaxFrame !== null) cancelAnimationFrame(parallaxFrame)
  parallaxFrame = null
  featureElement?.style.setProperty('--mouse-x', '0px')
  featureElement?.style.setProperty('--mouse-y', '0px')
}

onMounted(() => {
  carregarNiveis()
  observer.value = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('bento-in-view')
      } else {
        entry.target.classList.remove('bento-in-view')
      }
    })
  }, { threshold: 0.15 })

  document.querySelectorAll('.bento-card, .audience-card, .cta-inner').forEach(el => {
    observer.value.observe(el)
  })
})

onUnmounted(() => {
  resetFeatureParallax()
  if (observer.value) {
    observer.value.disconnect()
  }
})

const services = ref([
  {
    title: 'Atendimento e Consulta',
    desc: 'Peça vistorias e tire dúvidas sobre áreas de risco.',
    link: '#',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="24" height="24"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
  },
  {
    title: 'Abrigos',
    desc: 'Onde ficam os abrigos públicos e quantas vagas têm.',
    link: '#',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="24" height="24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
  },
  {
    title: 'Histórico',
    desc: 'Enchentes e níveis dos rios em anos anteriores.',
    link: '#',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="24" height="24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
  },
  {
    title: 'Plano de Emergência',
    desc: 'O que fazer antes, durante e depois de uma enchente.',
    link: '#',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="24" height="24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>'
  }
])

const features = ref([
  {
    title: 'Sensores',
    desc: 'Medem o nível do rio o tempo todo, com energia solar.',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6 8-2-2"/><path d="m18 8 2-2"/><path d="m6 16-2 2"/><path d="m18 16 2 2"/><path d="M12 2v2"/><path d="M12 20v2"/><circle cx="12" cy="12" r="4"/></svg>'
  },
  {
    title: 'Previsão do tempo',
    desc: 'Acompanha a chuva prevista para antecipar o risco.',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>'
  },
  {
    title: 'Análise de Risco',
    desc: 'Inteligência artificial estima a chance de o rio transbordar e quanto tempo falta.',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>'
  },
  {
    title: 'Painel da Defesa Civil',
    desc: 'Todos os rios e pontos de risco em tempo real para quem coordena a resposta.',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>'
  },
  {
    title: 'Alertas automáticos',
    desc: 'Avisos no site e no WhatsApp quando o risco aumenta.',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
  }
])

const audiences = ref([
  {
    title: 'Gestores Públicos',
    icon: '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    items: [
      'Visão de todos os rios e pontos de risco',
      'Organização das equipes da Defesa Civil',
      'Relatórios para apoiar decisões',
      'Alertas automáticos por WhatsApp'
    ]
  },
  {
    title: 'Cidadãos',
    icon: '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    items: [
      'Ver o nível do rio perto de casa',
      'Receber alertas da sua região',
      'Rota de fuga em poucos toques',
      'Contatos de emergência: 199 e 193'
    ]
  }
])
</script>

<style scoped>
/* ═══ LANDING BASE ═══ */
.landing {
  width: 100%;
  display: flex;
  flex-direction: column;
  font-family: 'Inter', sans-serif;
}

/* ═══ HERO ═══ */
.hero {
  background: var(--bg-primary);
  padding: 100px 24px 80px;
  position: relative;
  overflow: hidden;
}
.hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: url('/hero_bg.webp') no-repeat center center;
  background-size: cover;
  opacity: 0.7;
  pointer-events: none;
}
[data-theme='dark'] .hero::after {
  background-image:
    linear-gradient(90deg, rgba(2, 8, 18, 0.72), rgba(2, 8, 18, 0.58) 55%, rgba(2, 8, 18, 0.5)),
    url('/hero_bg.webp');
  opacity: 1;
}
[data-theme='light'] .hero::after {
  opacity: 0.15;
}


.hero-inner {
  max-width: 720px;
  position: relative;
  z-index: 1;
  margin-left: 8%;
}

.hero-badge {
  display: inline-block;
  background: rgba(59,130,246,0.15);
  color: var(--accent);
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  padding: 6px 16px;
  border-radius: 4px;
  margin-bottom: 28px;
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.1s forwards;
}

.hero-title {
  font-size: 3.2rem;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1.12;
  letter-spacing: -0.03em;
  margin-bottom: 20px;
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.2s forwards;
}

.hero-subtitle {
  font-size: 1rem;
  color: var(--text-secondary);
  line-height: 1.7;
  max-width: 540px;
  margin-bottom: 0;
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.3s forwards;
}

.hero-actions {
  margin-top: 32px;
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  opacity: 0;
  animation: fadeInUp 0.8s ease-out 0.4s forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-cta { flex: 1 1 260px; max-width: 340px; }
.hero-more { display: inline-block; margin-top: 18px; font-size: var(--fs-sm); color: var(--text-secondary); text-decoration: none; opacity: 0; animation: fadeInUp 0.8s ease-out 0.5s forwards; }
.hero-more:hover { color: var(--text-primary); }
.hero-alert {
  display: flex; align-items: center; gap: 10px; margin-top: 24px; padding: 12px 16px;
  border-radius: var(--radius-lg); background: var(--emergency); color: #fff; text-decoration: none; max-width: 560px;
}
.hero-alert span { flex: 1; font-size: var(--fs-sm); }
.hero-alert b { white-space: nowrap; }
@media (max-width: 768px) {
  .hero-cta { flex: none; width: 100%; max-width: none; }
}


.btn-hero-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  background: var(--accent);
  color: #fff;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  border-radius: 6px;
  text-decoration: none;
  transition: background 0.2s;
}
.btn-hero-primary:hover { background: var(--accent-hover); }

.btn-hero-secondary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  background: transparent;
  color: var(--text-secondary);
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  border-radius: 6px;
  border: 1px solid var(--border);
  text-decoration: none;
  transition: border-color 0.2s, color 0.2s;
}
.btn-hero-secondary:hover { border-color: var(--accent); color: var(--text-primary); }

/* ═══ SERVICES ═══ */
.services-section {
  background: var(--bg-secondary);
  padding: 80px 24px;
}

.services-inner {
  max-width: 1100px;
  margin: 0 auto;
}

.services-header {
  margin-bottom: 48px;
}
.services-header h2 {
  font-size: 2rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  margin-bottom: 10px;
}
.services-header p {
  font-size: 0.95rem;
  color: var(--text-secondary);
  max-width: 620px;
  line-height: 1.6;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.service-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 28px 24px;
  transition: transform 0.2s, box-shadow 0.2s;
}
.service-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}

.service-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 10px;
  background: var(--accent-soft);
  color: var(--accent);
  margin-bottom: 18px;
}

.service-card h3 {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.service-card p {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 18px;
}

.service-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--accent);
  text-decoration: none;
  letter-spacing: 0.05em;
  transition: gap 0.2s;
}
.service-link:hover { gap: 10px; }
.service-soon {
  display: inline-flex; align-self: flex-start; margin-top: 4px;
  padding: 3px 10px; border-radius: var(--radius-full);
  background: var(--bg-elevated); color: var(--text-muted);
  font-size: var(--fs-xs); font-weight: 700; letter-spacing: .03em;
}
.service-link .arrow { transition: transform 0.2s; }

/* ═══ FEATURES (BENTO) ═══ */
.features-section {
  background: var(--bg-primary);
  padding: 80px 24px;
  position: relative;
  overflow: hidden;
}
.features-section::after {
  content: '';
  position: absolute;
  width: 110%;
  height: 110%;
  top: -5%;
  left: -5%;
  background: url('/features_bg.webp') no-repeat center center;
  background-size: cover;
  opacity: 0.3;
  mix-blend-mode: overlay;
  pointer-events: none;
  z-index: 0;
  transform: translate3d(var(--mouse-x, 0px), var(--mouse-y, 0px), 0);
  transition: transform 0.15s ease-out;
  will-change: transform;
}
[data-theme='light'] .features-section::after {
  opacity: 0.1;
}
.features-inner {
  position: relative;
  z-index: 1;
  max-width: 1100px;
  margin: 0 auto;
}

.features-header {
  text-align: center;
  margin-bottom: 48px;
}
.features-header h2 {
  font-size: 2rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  margin-bottom: 10px;
}
.features-header p {
  font-size: 0.95rem;
  color: var(--text-muted);
  max-width: 500px;
  margin: 0 auto;
  line-height: 1.6;
}

.bento-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.bento-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 32px 28px;
  opacity: 0;
  transform: translateY(40px) scale(0.95);
  transition: border-color 0.2s, transform 0.6s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.bento-card.bento-in-view {
  opacity: 1;
  transform: translateY(0) scale(1);
}
.bento-card:hover { border-color: rgba(59,130,246,0.3); }

.bento-sm { /* default 1 col */ }

.bento-lg {
  /* takes 1 col but visually bigger */
}

.bento-full {
  grid-column: 1 / -1;
}

.bento-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 10px;
  background: var(--accent-soft);
  color: var(--accent);
  margin-bottom: 18px;
}

.bento-card h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.bento-card p {
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.6;
}

/* ═══ AUDIENCE ═══ */
.audience-section {
  background: var(--bg-secondary);
  padding: 80px 24px;
}

.audience-inner {
  max-width: 900px;
  margin: 0 auto;
}

.audience-header {
  text-align: center;
  margin-bottom: 48px;
}
.audience-header h2 {
  font-size: 2rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.audience-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px;
}

.audience-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 32px 28px;
  opacity: 0;
  transform: translateY(40px) scale(0.95);
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.audience-card.bento-in-view {
  opacity: 1;
  transform: translateY(0) scale(1);
}

.audience-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 52px;
  height: 52px;
  border-radius: 12px;
  background: var(--accent-soft);
  color: var(--accent);
  margin-bottom: 18px;
}

.audience-card h3 {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 16px;
}

.audience-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.audience-card li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

.audience-card li .check {
  color: var(--accent);
  flex-shrink: 0;
  margin-top: 1px;
}

/* ═══ CTA ═══ */
.cta-section {
  background: var(--bg-primary);
  padding: 80px 24px;
}

.cta-inner {
  max-width: 680px;
  margin: 0 auto;
  text-align: center;
  opacity: 0;
  transform: translateY(40px) scale(0.95);
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.cta-inner.bento-in-view {
  opacity: 1;
  transform: translateY(0) scale(1);
}

.cta-inner h2 {
  font-size: 2.2rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  margin-bottom: 14px;
}

.cta-inner p {
  font-size: 1rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 32px;
}

.btn-cta {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 16px 40px;
  border-radius: 8px;
  background: var(--emergency);
  color: #fff;
  text-decoration: none;
  font-weight: 700;
  font-size: 1rem;
  letter-spacing: 0.02em;
  transition: background 0.2s, transform 0.15s;
}
.btn-cta:hover { background: var(--emergency-hover); transform: translateY(-2px); }

/* ═══ RESPONSIVE ═══ */
@media (max-width: 1024px) {
  .services-grid { grid-template-columns: repeat(2, 1fr); }
  .hero-inner { margin-left: 5%; }
}

@media (max-width: 768px) {
  .hero { padding: 36px 20px 40px; }
  .hero-inner { margin-left: 0; }
  .hero-title { font-size: 1.9rem; }
  .hero-title br { display: none; }
  .hero-subtitle { font-size: var(--fs-sm); }
  .hero-badge { font-size: 0.62rem; letter-spacing: .08em; }
  .hero-actions { flex-direction: column; }
  .services-grid { grid-template-columns: 1fr; }
  .bento-grid { grid-template-columns: 1fr; }
  .audience-grid { grid-template-columns: 1fr; }
  .cta-inner h2 { font-size: 1.6rem; }
}
</style>
