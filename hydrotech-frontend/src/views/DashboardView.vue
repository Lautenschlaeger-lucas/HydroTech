<template>
  <div class="dashboard">

    <!-- Page Header -->
    <div class="page-header">
      <div>
        <p class="page-label">Painel Operacional</p>
        <h1 class="page-title">Centro de Controle</h1>
        <p class="page-subtitle">Monitoramento em tempo real de todos os pontos de risco hidrológico cadastrados.</p>
      </div>
      <div class="header-right">
        <div class="header-stat">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/></svg>
          <span>Rios</span>
          <strong>{{ rios.length }}</strong>
        </div>
        <div class="header-stat">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z"/><circle cx="12" cy="10" r="3"/></svg>
          <span>Pontos</span>
          <strong>{{ totalPontos }}</strong>
        </div>
        <div class="header-stat header-stat--live">
          <span class="live-dot"></span>
          <span>AO VIVO</span>
          <strong v-if="lastUpdate">{{ lastUpdate }}</strong>
        </div>
      </div>
    </div>

    <!-- Atalho para o simulador (só na área logada, o público não vê) -->
    <section class="sim-card" aria-labelledby="sim-card-titulo">
      <span class="sim-card-ico" aria-hidden="true">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.7c-3.3 4-6 7.5-6 11.3a6 6 0 0 0 12 0c0-3.8-2.7-7.3-6-11.3z"/><path d="M9 15a3 3 0 0 0 3 3"/></svg>
      </span>
      <div class="sim-card-txt">
        <h2 id="sim-card-titulo">Simulador de enchente <span class="sim-card-tag">Treinamento</span></h2>
        <p>Mude o nível dos rios para Normal, Atenção ou Perigo e veja o site do público reagir. Abre numa nova aba deste navegador.</p>
      </div>
      <router-link to="/simulador" target="_blank" rel="noopener" class="btn btn--primary sim-card-btn">
        Abrir simulador
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg>
      </router-link>
    </section>

    <!-- Filter Bar -->
    <div class="filter-bar">
      <div class="filter-row">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
        <select v-model="filtroEstado" class="filter-select">
          <option value="">Todos os estados</option>
          <option v-for="e in estadosList" :key="e" :value="e">{{ e }}</option>
        </select>
      </div>
    </div>

    <!-- Loading Skeletons -->
    <div v-if="loading" class="skeleton-grid">
      <div v-for="i in 4" :key="'skel'+i" class="skeleton-card">
        <div class="skeleton-hdr">
          <div class="skeleton-title skeleton"></div>
          <div class="skeleton-sub skeleton"></div>
        </div>
        <div class="skeleton-body skeleton"></div>
      </div>
    </div>

    <!-- Dashboard Content -->
    <div v-else-if="todosPontos.length === 0" class="empty-state">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
        <path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/>
        <path d="M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/>
      </svg>
      <p>Nenhum ponto de risco cadastrado</p>
      <span>Cadastre rios e pontos de levantamento na seção "Gestão de Rios" para começar o monitoramento.</span>
    </div>

    <div v-else class="dashboard-content">
      <!-- Agrupado por Estado -->
      <div v-for="estado in estadosFiltrados" :key="estado" class="estado-section">
        <div class="estado-header">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          {{ estado }}
          <span class="estado-count">{{ riosPorEstado[estado]?.length || 0 }} rios</span>
        </div>

        <!-- Rios do Estado -->
        <div v-for="rio in riosPorEstado[estado]" :key="rio.id" class="rio-block">
          <div class="rio-hdr">
            <div class="rio-hdr-l">
              <div class="rio-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/></svg>
              </div>
              <div>
                <h2 class="rio-name">{{ rio.nome }}</h2>
                <p class="rio-loc">{{ rio.cidade }} · {{ rio.estado }}</p>
              </div>
            </div>
            <span class="rio-pontos-count">{{ (pontosPorRio[rio.id] || []).length }} pontos</span>
          </div>

          <!-- Gráficos por Ponto de Risco -->
          <div class="charts-wrap">
            <div v-if="!pontosPorRio[rio.id] || pontosPorRio[rio.id].length === 0" class="charts-empty">
              Nenhum ponto de risco cadastrado neste rio.
            </div>
            <div v-else class="charts-grid">
              <div v-for="ponto in pontosPorRio[rio.id]" :key="ponto.id" class="chart-card">
                <div class="chart-card-hdr">
                  <div>
                    <h3 class="chart-card-title">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
                      {{ ponto.descricao.length > 40 ? ponto.descricao.substring(0,40)+'…' : ponto.descricao }}
                    </h3>
                    <p class="chart-card-sub">
                      <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z"/><circle cx="12" cy="10" r="3"/></svg>
                      {{ rio.nome }} · {{ ponto.descricao.length > 45 ? ponto.descricao.substring(0,45)+'…' : ponto.descricao }}
                    </p>
                  </div>
                  <RiskPill :risco="statusDe(ponto)" />
                </div>
                <section class="forecast-card" :class="'forecast--' + (previsoes[ponto.id]?.status || 'carregando')" aria-live="polite">
                  <div class="forecast-heading">
                    <strong>Previsão de risco</strong>
                  </div>
                  <p v-if="!previsoes[ponto.id]">Calculando previsão…</p>
                  <template v-else>
                    <p v-if="previsoes[ponto.id].status === 'sem_risco'" class="forecast-status"><b>Sem risco identificado.</b> {{ previsoes[ponto.id].mensagem }}</p>
                    <p v-else-if="previsoes[ponto.id].status === 'critico'" class="forecast-status"><b>Limite crítico atingido.</b> Nível atual: {{ previsoes[ponto.id].nivel_atual }} m.</p>
                    <p v-else-if="previsoes[ponto.id].status === 'risco' && previsoes[ponto.id].estimativa_minutos !== null" class="forecast-status"><b>Risco identificado:</b> {{ formatarPrazo(previsoes[ponto.id].estimativa_minutos) }} até o limite crítico de {{ previsoes[ponto.id].limite_critico }} m.</p>
                    <p v-else class="forecast-status">{{ previsoes[ponto.id].mensagem }}</p>
                    <small v-if="previsoes[ponto.id].sensor_nome">{{ previsoes[ponto.id].sensor_nome }} · nível registrado {{ previsoes[ponto.id].nivel_atual }} m</small>
                    <p v-if="previsoes[ponto.id].analise_ia" class="forecast-ai">✨ Gemini: {{ previsoes[ponto.id].analise_ia }}</p>
                    <small v-else-if="previsoes[ponto.id].fonte_previsao === 'reserva_local'" class="forecast-fallback">{{ previsoes[ponto.id].mensagem_reserva || 'Estimativa local.' }}</small>
                  </template>
                </section>
                <div class="chart-body"><RiverChart :ponto="ponto" :altura="200" sem-risco /></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import api from '../services/api'
import RiverChart from '@/components/RiverChart.vue'
import RiskPill from '@/components/RiskPill.vue'
import { useNiveis, garantirSerie } from '@/composables/useNiveis'

const { statusDe, ultimaAtualizacao } = useNiveis()

const rios = ref([])
const loading = ref(true)
const lastUpdate = ref('')
const pontosPorRio = ref({})
const todosPontos = ref([])
const previsoes = ref({})
const totalPontos = computed(() => todosPontos.value.length)

const formatarPrazo = minutos => minutos < 60
  ? `cerca de ${minutos} min`
  : minutos < 1440
    ? `cerca de ${Math.floor(minutos / 60)} h ${minutos % 60} min`
    : `cerca de ${Math.floor(minutos / 1440)} dias`
const formatarData = data => data ? new Date(data).toLocaleString('pt-BR') : 'horário indisponível'

const carregarPrevisao = async ponto => {
  try {
    const resposta = await api.getPrevisaoPontoRisco(ponto.id)
    previsoes.value[ponto.id] = resposta.data
  } catch {
    previsoes.value[ponto.id] = {
      status: 'erro',
      mensagem: 'Não foi possível gerar o cenário demonstrativo.',
      estimativa_minutos: null,
    }
  }
}

const filtroEstado = ref('')

const estadosList = computed(() =>
  [...new Set(rios.value.map(r => r.estado))].filter(Boolean).sort()
)
const estadosFiltrados = computed(() => {
  if (filtroEstado.value) return [filtroEstado.value]
  return estadosList.value
})
const riosPorEstado = computed(() => {
  const map = {}
  rios.value.forEach(r => {
    if (!map[r.estado]) map[r.estado] = []
    map[r.estado].push(r)
  })
  return map
})

watch(ultimaAtualizacao, t => {
  if (t) lastUpdate.value = new Date(t).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
})

const load = async () => {
  loading.value = true
  try {
    const res = await api.getRios()
    rios.value = Array.isArray(res.data) ? res.data : res.data.results || []
    const promises = rios.value.map(async (rio) => {
      try {
        const pr = await api.getPontosRisco(rio.id)
        const pontos = Array.isArray(pr.data) ? pr.data : pr.data.results || []
        pontosPorRio.value[rio.id] = pontos
        return pontos.map(ponto => ({ rio, ponto }))
      } catch {
        pontosPorRio.value[rio.id] = []
        return []
      }
    })
    const resultados = await Promise.all(promises)
    todosPontos.value = resultados.flat()
    todosPontos.value.forEach(({ ponto }) => { garantirSerie(ponto); carregarPrevisao(ponto) })
  } catch (err) {
    console.error('Erro ao carregar:', err)
  } finally {
    loading.value = false
    lastUpdate.value = new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  }
}

onMounted(() => load())
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
  animation: fadeInUp 0.35s ease-out;
}

/* Page Header */
.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}

.page-label {
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--text-primary);
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin-top: 4px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.header-stat {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  font-size: 0.78rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.header-stat svg { color: var(--accent); }
.header-stat strong { font-size: 1.1rem; font-weight: 800; color: var(--text-primary); }

.header-stat--live {
  background: var(--risk-high-bg);
  border-color: var(--risk-high);
  color: var(--risk-high);
}
.header-stat--live strong { color: var(--risk-high); font-size: 0.78rem; }

/* Atalho do simulador */
.sim-card {
  display: flex; align-items: center; gap: 16px;
  padding: 16px 20px;
  background: var(--bg-card);
  border: 1px dashed var(--border);
  border-radius: var(--radius-lg);
}
.sim-card-ico {
  width: 44px; height: 44px; flex-shrink: 0;
  display: grid; place-items: center;
  border-radius: var(--radius-md);
  background: var(--accent-soft); color: var(--accent);
}
.sim-card-txt { flex: 1; min-width: 0; }
.sim-card-txt h2 { font-size: var(--fs-md); font-weight: 800; color: var(--text-primary); display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.sim-card-txt p { font-size: var(--fs-sm); color: var(--text-secondary); margin-top: 2px; }
.sim-card-tag {
  font-size: var(--fs-xs); font-weight: 700; text-transform: uppercase; letter-spacing: .04em;
  padding: 2px 8px; border-radius: var(--radius-full);
  background: var(--risk-medium-bg); color: var(--risk-medium-text);
}
.sim-card-btn { flex-shrink: 0; gap: 8px; }
@media (max-width: 640px) {
  .sim-card { flex-wrap: wrap; padding: 16px; }
  .sim-card-ico { display: none; }
  .sim-card-btn { width: 100%; justify-content: center; }
}

/* Filter Bar */
.filter-bar {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
}

.filter-select {
  padding: 8px 14px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  background: var(--bg-card);
  color: var(--text-primary);
  font-size: 0.85rem;
  font-family: inherit;
}

/* Skeleton Loading */
.skeleton-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 80px 24px;
  color: var(--text-muted);
  text-align: center;
}

.empty-state p {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-secondary);
}

.empty-state span {
  font-size: 0.9rem;
  max-width: 400px;
  line-height: 1.6;
}

/* Dashboard Content */
.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

/* Estado Section */
.estado-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.estado-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
  font-weight: 800;
  color: var(--text-primary);
  padding-bottom: 8px;
  border-bottom: 2px solid var(--border-accent);
}

.estado-count {
  font-size: 0.75rem;
  font-weight: 600;
  background: var(--water-soft);
  color: var(--accent);
  padding: 2px 8px;
  border-radius: 20px;
  margin-left: 4px;
  border: 1px solid var(--border-accent);
}

/* Rio Block */
.rio-block {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.rio-hdr {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 22px;
  border-bottom: 1px solid var(--border-light);
  border-left: 4px solid var(--accent);
  flex-wrap: wrap;
  gap: 12px;
}

.rio-hdr-l {
  display: flex;
  align-items: center;
  gap: 12px;
}

.rio-icon {
  width: 42px;
  height: 42px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent-soft);
  color: var(--accent);
}

.rio-name {
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--text-primary);
}

.rio-loc {
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-top: 2px;
}

.rio-pontos-count {
  font-size: 0.72rem;
  font-weight: 700;
  background: var(--bg-elevated);
  color: var(--text-secondary);
  padding: 4px 12px;
  border-radius: var(--radius-full);
  border: 1px solid var(--border);
}

/* Charts */
.charts-wrap {
  padding: 20px 22px;
}

.charts-empty {
  color: var(--text-muted);
  font-size: 0.85rem;
  text-align: center;
  padding: 20px;
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

/* Chart Card */
.chart-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
}

.forecast-card { margin: 14px 22px 0; padding: 13px 16px; border: 1px solid var(--border); border-left: 4px solid var(--text-muted); border-radius: 10px; background: var(--bg-tertiary); color: var(--text-primary); font-size: .84rem; line-height: 1.5; }
.forecast--estimavel { border-left-color: var(--water); }
.forecast--critico { border-left-color: var(--risk-high); background: var(--risk-high-bg); }
.forecast-heading { display:flex; justify-content:space-between; gap:12px; margin-bottom:5px; }
.forecast-heading span, .forecast-card small { color:var(--text-secondary); font-size:.73rem; }
.forecast-card p { margin:4px 0; }
.forecast-ai { color:var(--accent); }
.forecast--risco { border-left-color: var(--risk-medium-solid); background: var(--risk-medium-bg); }
.forecast--sem_risco { border-left-color: var(--risk-low); }
.forecast-status b { color: var(--text-primary); }
.forecast-fallback { display:block; margin-top:6px; color: var(--risk-medium-text); }

.chart-card-hdr {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 18px 22px;
  border-bottom: 1px solid var(--border-light);
  gap: 10px;
}

.chart-card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
}

.chart-card-sub {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px;
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-top: 5px;
}

.live-badge {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.7rem;
  font-weight: 800;
  color: var(--risk-high);
  background: var(--risk-high-bg);
  padding: 4px 9px;
  border-radius: 8px;
  border: 1px solid var(--risk-high);
  flex-shrink: 0;
}

.live-dot {
  width: 7px;
  height: 7px;
  background: var(--risk-high);
  border-radius: 50%;
  animation: pulse 1.4s infinite;
}

.chart-canvas-wrap {
  height: 280px;
  padding: 18px 20px;
}

.chart-observer {
  width: 100%;
  height: 100%;
}

.chart-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: var(--text-muted);
  font-size: 0.82rem;
  opacity: 0.5;
}

/* Animations */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(1.4); }
}

/* Responsive */
.chart-body { padding: 16px 22px 20px; }
@media (min-width: 1200px) { .charts-grid { grid-template-columns: 1fr 1fr; } }
@media (max-width: 768px) {
  .page-header { flex-direction: column; align-items: flex-start; }
  .header-right { flex-wrap: wrap; }
  .page-title { font-size: var(--fs-xl); }
  .chart-card-hdr { padding: 14px 16px; }
  .forecast-card { margin: 12px 16px 0; }
  .chart-body { padding: 12px 16px 16px; }
}
</style>
