<template>
  <div class="dashboard">

    <!-- Page Header -->
    <div class="page-header">
      <div class="page-header-left">
        <p class="page-label">Painel do Sistema</p>
        <h1 class="page-title">Visão geral do monitoramento hidrológico</h1>
      </div>
      <div class="live-badge" v-if="!loading">
        <span class="live-pulse"></span>
        Atualizações ao Vivo Ativas
      </div>
    </div>

    <!-- Stats Row -->
    <div class="stats-row">
      <div class="stat-card">
        <p class="stat-label">Total de Rios</p>
        <p class="stat-number">{{ rios.length }}</p>
        <p class="stat-sub">Estações ativas</p>
      </div>
      <div class="stat-card">
        <p class="stat-label">Pontos Monitorados</p>
        <p class="stat-number">{{ totalPontos }}</p>
        <p class="stat-sub">Sensores ativos</p>
      </div>
      <div class="stat-card">
        <p class="stat-label">Estados Cobertos</p>
        <p class="stat-number">{{ estadosList.length }}</p>
        <p class="stat-sub">Regiões monitoradas</p>
      </div>
      <div class="stat-card">
        <p class="stat-label">Filtrar por Estado</p>
        <select v-model="filtroEstado" class="state-filter">
          <option value="">Todos os estados</option>
          <option v-for="e in estadosList" :key="e" :value="e">{{ e }}</option>
        </select>
      </div>
    </div>

    <!-- Loading Skeletons -->
    <div v-if="loading" class="charts-grid">
      <div v-for="i in 2" :key="'skel'+i" class="skeleton-card">
        <div class="skeleton-hdr">
          <div class="skeleton-title skeleton"></div>
          <div class="skeleton-sub skeleton"></div>
        </div>
        <div class="skeleton-body skeleton"></div>
      </div>
    </div>

    <!-- Empty -->
    <div v-else-if="rios.length === 0" class="empty-block">
      <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
        <path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/>
      </svg>
      <p>Nenhum rio cadastrado</p>
      <span>Vá em <router-link to="/rios">Rios</router-link> para cadastrar rios e pontos de risco.</span>
    </div>

    <!-- Rivers by State -->
    <div v-else class="estados-wrapper">
      <div v-for="estado in estadosFiltrados" :key="estado" class="estado-bloco">
        <div class="estado-header">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
            <circle cx="12" cy="10" r="3"/>
          </svg>
          {{ estado }}
          <span class="estado-count">{{ riosPorEstado[estado].length }} {{ riosPorEstado[estado].length === 1 ? 'rio' : 'rios' }}</span>
        </div>

        <div v-for="rio in riosPorEstado[estado]" :key="rio.id" class="rio-bloco">
          <div class="rio-header">
            <div class="rio-header-left">
              <div class="rio-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                  <path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/>
                </svg>
              </div>
              <div>
                <h2 class="rio-nome">{{ rio.nome }}</h2>
                <p class="rio-loc">{{ rio.cidade }} · {{ rio.estado }}</p>
              </div>
            </div>
            <div class="rio-header-right">
              <span class="station-code">SP-BAS-{{ String(rio.id).padStart(3, '0') }}</span>
            </div>
          </div>

          <!-- Charts grid -->
          <div class="rio-charts">
            <div v-if="!pontosPorRio[rio.id]" class="pontos-loading">
              <svg class="spin" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2.5">
                <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="32">
                  <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="0.8s" repeatCount="indefinite"/>
                </circle>
              </svg>
              Carregando pontos...
            </div>
            <div v-else-if="pontosPorRio[rio.id].length === 0" class="pontos-empty">
              Nenhum ponto de risco. <router-link to="/rios">Adicionar</router-link>
            </div>
            <div v-else class="charts-grid">
              <div v-for="ponto in pontosPorRio[rio.id]" :key="ponto.id" class="chart-card">
                <div class="chart-card-header">
                  <div>
                    <h3 class="chart-title">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round">
                        <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
                      </svg>
                      {{ ponto.descricao.length > 40 ? ponto.descricao.substring(0,40)+'…' : ponto.descricao }}
                    </h3>
                    <p class="chart-sub">
                      <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                        <path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z"/>
                        <circle cx="12" cy="10" r="3"/>
                      </svg>
                      {{ rio.nome }} · {{ ponto.descricao.length > 45 ? ponto.descricao.substring(0,45)+'…' : ponto.descricao }}
                    </p>
                  </div>
                </div>
                <div class="chart-wrap">
                  <div :ref="el => setObserverRef(el, ponto.id)" class="chart-observer">
                    <canvas v-if="visibleCharts.has(ponto.id)" :ref="el => setChartRef(el, ponto.id)"></canvas>
                    <div v-else class="chart-placeholder">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
                      <span>Rolar para carregar</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import api from '../services/api'
import Chart from 'chart.js/auto'

const chartCanvases = ref({})
let chartInstances = {}
let chartLevels = {}
let chartInterval = null

const setChartRef = (el, id) => { 
  if (el) chartCanvases.value[id] = el 
  else delete chartCanvases.value[id]
}

const visibleCharts = ref(new Set())
let chartObserver = null

const setObserverRef = (el, pontoId) => {
  if (!el) return
  if (!chartObserver) {
    chartObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = Number(entry.target.dataset.pontoId)
          visibleCharts.value = new Set([...visibleCharts.value, id])
          chartObserver.unobserve(entry.target)
          const todo = todosPontos.value.find(({ponto}) => ponto.id === id)
          if (todo) buildChart(todo.ponto)
        }
      })
    }, { rootMargin: '100px' })
  }
  el.dataset.pontoId = pontoId
  chartObserver.observe(el)
}

const buildChart = (ponto) => {
  const canvas = chartCanvases.value[ponto.id]
  if (!canvas || chartInstances[ponto.id]) return
  const ctx = canvas.getContext('2d')
  const nivelColor = '#38bdf8'
  const gradient = ctx.createLinearGradient(0, 0, 0, 220)
  gradient.addColorStop(0, nivelColor + '40')
  gradient.addColorStop(1, nivelColor + '05')
  const baseMap = { 1: 0.8, 2: 1.4, 3: 2.0 }
  const base = (ponto.nivel_base !== null && ponto.nivel_base !== undefined) ? parseFloat(ponto.nivel_base) : (baseMap[ponto.nivel_risco] || 1.0)
  const variance = 0.25
  const data = Array.from({ length: 15 }, () => (base + (Math.random() * variance * 2 - variance)).toFixed(2))
  const labels = Array.from({ length: 15 }, (_, i) => {
    const d = new Date(); d.setSeconds(d.getSeconds() - (15 - i) * 10)
    return d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  })
  const atencao = (ponto.limite_atencao !== null && ponto.limite_atencao !== undefined) ? parseFloat(ponto.limite_atencao) : +(base + 0.5).toFixed(2)
  const alerta = (ponto.limite_alerta !== null && ponto.limite_alerta !== undefined) ? parseFloat(ponto.limite_alerta) : +(base + 0.85).toFixed(2)
  const emergencia = (ponto.limite_emergencia !== null && ponto.limite_emergencia !== undefined) ? parseFloat(ponto.limite_emergencia) : +(base + 1.2).toFixed(2)
  chartLevels[ponto.id] = { base, variance, emergenciaLevel: parseFloat(emergencia) }

  chartInstances[ponto.id] = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        { label: 'Altura do Rio', data, borderColor: nivelColor, backgroundColor: gradient, borderWidth: 2, pointRadius: 3, pointHoverRadius: 5, pointBackgroundColor: nivelColor, pointBorderColor: 'transparent', fill: true, tension: 0.4 },
        { label: 'Alto', data: Array(15).fill(emergencia), borderColor: '#ef4444', borderWidth: 1, borderDash: [5, 4], pointRadius: 0, fill: false },
        { label: 'Médio', data: Array(15).fill(alerta), borderColor: '#f59e0b', borderWidth: 1, borderDash: [5, 4], pointRadius: 0, fill: false },
        { label: 'Baixo', data: Array(15).fill(atencao), borderColor: '#4ade80', borderWidth: 1, borderDash: [5, 4], pointRadius: 0, fill: false }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false, animation: false,
      plugins: {
        legend: { display: true, position: 'top', labels: { usePointStyle: true, color: getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim(), font: { size: 10 }, boxWidth: 8 } },
        tooltip: { backgroundColor: getComputedStyle(document.documentElement).getPropertyValue('--bg-elevated').trim() || '#0D1B2E', titleColor: getComputedStyle(document.documentElement).getPropertyValue('--text-primary').trim(), bodyColor: getComputedStyle(document.documentElement).getPropertyValue('--accent').trim(), borderColor: 'rgba(0,0,0,0.08)', borderWidth: 1, padding: 10 }
      },
      scales: {
        y: { suggestedMin: 0, grid: { color: 'rgba(100,116,139,0.1)' }, ticks: { color: getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim(), font: { size: 10 } } },
        x: { grid: { display: false }, ticks: { color: getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim(), maxTicksLimit: 15, font: { size: 10 } } }
      }
    }
  })
}

const tick = () => {
      })
    }, { rootMargin: '100px' })
  }
  el.dataset.pontoId = pontoId
  chartObserver.observe(el)
}

const rios = ref([])
const loading = ref(true)
const lastUpdate = ref('')
const pontosPorRio = ref({})
const todosPontos = ref([])
const totalPontos = computed(() => todosPontos.value.length)

const normalizeRisk = (risco) => {
  if (typeof risco === 'number') return risco
  if (typeof risco === 'string') {
    const lower = risco.toLowerCase().trim()
    if (lower === 'baixo') return 1
    if (lower === 'médio' || lower === 'medio') return 2
    if (lower === 'alto') return 3
    if (lower === 'muito alto') return 4
    const parsed = parseInt(lower, 10)
    return Number.isNaN(parsed) ? null : parsed
  }
  return null
}

const filtroEstado = ref('')
watch(filtroEstado, () => {
  Object.values(chartInstances).forEach(c => c.destroy())
  chartInstances = {}
  chartLevels = {}
  visibleCharts.value = new Set()
})
const estadosList = computed(() => [...new Set(rios.value.map(r => r.estado))].filter(Boolean).sort())
const estadosFiltrados = computed(() => {
  if (filtroEstado.value) return [filtroEstado.value]
  return estadosList.value
})
const riosPorEstado = computed(() => {
  const map = {}
  rios.value.forEach(r => { if (!map[r.estado]) map[r.estado] = []; map[r.estado].push(r) })
  return map
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
      } catch { pontosPorRio.value[rio.id] = []; return [] }
    })
    const resultados = await Promise.all(promises)
    todosPontos.value = resultados.flat()
  } catch (err) {
    console.error('Erro ao carregar:', err)
  } finally {
    loading.value = false
    lastUpdate.value = new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    await nextTick()
    if (todosPontos.value.length > 0) {
      chartInterval = setInterval(tick, 10000)
    }
  }
}

const tick = () => {
  const newLabel = new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  Object.entries(chartInstances).forEach(([pontoId, chart]) => {
    const levels = chartLevels[pontoId]; if (!levels) return
    const ds = chart.data.datasets[0]
    let v = parseFloat(ds.data.slice(-1)[0]) + (Math.random() * levels.variance * 2 - levels.variance)
    v = Math.max(Math.max(0, levels.base - 0.6), Math.min(levels.emergenciaLevel + 0.2, v))
    chart.data.labels.push(newLabel); ds.data.push(v.toFixed(2))
    chart.data.datasets[1].data.push(chart.data.datasets[1].data[0])
      chart.data.datasets[2].data.push(chart.data.datasets[2].data[0])
      chart.data.datasets[3].data.push(chart.data.datasets[3].data[0])
      if (chart.data.labels.length > 15) { chart.data.labels.shift(); chart.data.datasets.forEach(d => d.data.shift()) }
      chart.update('none')
    })
    lastUpdate.value = newLabel
  }, 10000)
}

onMounted(() => load())
onUnmounted(() => {
  if (chartInterval) clearInterval(chartInterval)
  if (chartObserver) chartObserver.disconnect()
  Object.values(chartInstances).forEach(c => c.destroy())
  chartLevels = {}
})
</script>

<style scoped>
.dashboard { display: flex; flex-direction: column; gap: 24px; animation: fadeInUp 0.35s ease-out; }

/* Header */
.page-header { display: flex; align-items: flex-end; justify-content: space-between; flex-wrap: wrap; gap: 12px; }
.page-label { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: 4px; }
.page-title { font-size: 1.5rem; font-weight: 800; letter-spacing: -0.02em; }

.live-badge {
  display: flex; align-items: center; gap: 8px;
  font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em;
  color: var(--status-active);
  padding: 5px 12px;
  border-radius: var(--radius-full);
  background: var(--status-active-bg);
  border: 1px solid rgba(16,185,129,0.2);
}

.live-pulse {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--status-active); animation: pulse 2s infinite;
}

/* Stats */
.stats-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }
.stat-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-xl); padding: 20px 24px; display: flex; flex-direction: column; justify-content: center; box-shadow: var(--shadow-sm); }
.stat-label { font-size: 0.72rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; }
.stat-number { font-size: 1.8rem; font-weight: 800; color: var(--text-primary); line-height: 1; margin-bottom: 6px; }
.stat-number--accent { color: var(--accent); }
.stat-sub { font-size: 0.8rem; color: var(--text-secondary); }

.state-filter { width: 100%; padding: 10px 14px; margin-top: 4px; border-radius: var(--radius-md); border: 1px solid var(--border); background: var(--bg-tertiary); color: var(--text-primary); font-size: 0.95rem; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.state-filter:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }

/* Loading / Empty */
.dash-loading { display: flex; align-items: center; justify-content: center; gap: 12px; padding: 60px; color: var(--text-muted); font-size: 0.875rem; }
.empty-block { display: flex; flex-direction: column; align-items: center; gap: 10px; padding: 56px 24px; text-align: center; color: var(--text-muted); background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-xl); }
.empty-block p { font-size: 0.95rem; font-weight: 600; color: var(--text-secondary); }
.empty-block a { color: var(--accent); font-weight: 600; }

/* States */
.estados-wrapper { display: flex; flex-direction: column; gap: 32px; }
.estado-bloco { display: flex; flex-direction: column; gap: 16px; }
.estado-header { display: flex; align-items: center; gap: 8px; font-size: 0.78rem; font-weight: 800; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.06em; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
.estado-count { font-size: 0.65rem; background: var(--accent-soft); color: var(--accent); padding: 2px 8px; border-radius: var(--radius-full); margin-left: 4px; }

/* River Block */
.rio-bloco { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-xl); overflow: hidden; }

.rio-header { display: flex; align-items: center; justify-content: space-between; padding: 14px 20px; border-bottom: 1px solid var(--border-light); flex-wrap: wrap; gap: 10px; border-left: 3px solid var(--accent); }
.rio-header-left { display: flex; align-items: center; gap: 12px; }
.rio-icon { width: 38px; height: 38px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; background: rgba(56, 189, 248, 0.1); color: var(--accent); }
.rio-nome { font-size: 1rem; font-weight: 700; }
.rio-loc { font-size: 0.72rem; color: var(--text-muted); margin-top: 2px; }
.rio-header-right { display: flex; align-items: center; gap: 10px; }
.station-code { font-size: 0.7rem; font-family: var(--font-mono); color: var(--text-muted); }

/* Charts */
.rio-charts { padding: 18px 20px; }
.pontos-loading { display: flex; align-items: center; gap: 8px; color: var(--text-muted); font-size: 0.8rem; padding: 8px 0; }
.pontos-empty { color: var(--text-muted); font-size: 0.82rem; padding: 8px 0; }
.pontos-empty a { color: var(--accent); font-weight: 600; }

.charts-grid { display: grid; grid-template-columns: 1fr; gap: 20px; }

.chart-card { background: var(--bg-secondary); border: 1px solid var(--border); border-radius: var(--radius-lg); overflow: hidden; }

.chart-card-header { display: flex; align-items: flex-start; justify-content: space-between; padding: 16px 20px; border-bottom: 1px solid var(--border-light); gap: 12px; }

.chart-title { display: flex; align-items: center; gap: 8px; font-size: 0.95rem; font-weight: 700; }

.chart-sub { display: flex; align-items: center; flex-wrap: wrap; gap: 4px; font-size: 0.75rem; color: var(--text-muted); margin-top: 4px; }

.nivel--alto { color: var(--risk-high); font-weight: 700; }
.nivel--medio { color: var(--risk-medium); font-weight: 700; }
.nivel--baixo { color: var(--risk-low); font-weight: 700; }

.live-tag { display: flex; align-items: center; gap: 5px; font-size: 0.65rem; font-weight: 800; color: var(--risk-high); background: var(--risk-high-bg); padding: 4px 8px; border-radius: var(--radius-sm); text-transform: uppercase; letter-spacing: 0.04em; white-space: nowrap; border: 1px solid rgba(220,38,38,0.2); flex-shrink: 0; }

.live-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--risk-high); animation: pulse 1.5s infinite; }

.chart-wrap { height: 260px; padding: 16px 20px; }

.chart-observer { width: 100%; height: 100%; }
.chart-placeholder { width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; color: var(--text-muted); font-size: 0.82rem; opacity: 0.5; }

@media (max-width: 1024px) { .stats-row { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px) { .stats-row { grid-template-columns: 1fr; } .charts-grid { grid-template-columns: 1fr; } }
</style>