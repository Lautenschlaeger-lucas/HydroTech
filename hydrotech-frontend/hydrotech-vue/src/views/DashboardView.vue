<template>
  <div class="dashboard">

    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Dashboard</h1>
        <p class="page-subtitle">Visão geral do monitoramento hidrológico</p>
      </div>
      <div class="page-meta" v-if="lastUpdate">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        Atualizado {{ lastUpdate }}
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="stats-grid">

      <!-- Risk Card -->
      <div class="stat-card stat-card--risk" :class="'stat-card--' + riskLevel">
        <div class="stat-card-header">
          <div class="stat-icon stat-icon--risk">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          </div>
          <span class="stat-label">Nível de Risco Atual</span>
        </div>
        <div class="risk-display">
          <span class="risk-dot" :class="'risk-dot--' + riskLevel"></span>
          <span class="risk-text">{{ riskLabel }}</span>
        </div>
      </div>

      <!-- Total Rios -->
      <div class="stat-card">
        <div class="stat-card-header">
          <div class="stat-icon stat-icon--blue">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M2 18c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/></svg>
          </div>
          <span class="stat-label">Total de Rios</span>
        </div>
        <div class="stat-value-wrap">
          <span class="stat-number">{{ rios.length }}</span>
          <span class="stat-desc">rios monitorados</span>
        </div>
        <div class="stat-accent stat-accent--blue"></div>
      </div>

      <!-- Alto Risco -->
      <div class="stat-card">
        <div class="stat-card-header">
          <div class="stat-icon stat-icon--red">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/></svg>
          </div>
          <span class="stat-label">Risco Alto</span>
        </div>
        <div class="stat-value-wrap">
          <span class="stat-number stat-number--red">{{ riosAltoRisco }}</span>
          <span class="stat-desc">requerem atenção</span>
        </div>
        <div class="stat-accent stat-accent--red"></div>
      </div>

      <!-- Medio Risco -->
      <div class="stat-card">
        <div class="stat-card-header">
          <div class="stat-icon stat-icon--yellow">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 9v4"/><path d="M12 17h.01"/><path d="M3.6 15h16.8"/><path d="M12 3v2"/></svg>
          </div>
          <span class="stat-label">Risco Médio</span>
        </div>
        <div class="stat-value-wrap">
          <span class="stat-number stat-number--yellow">{{ riosMedioRisco }}</span>
          <span class="stat-desc">em observação</span>
        </div>
        <div class="stat-accent stat-accent--yellow"></div>
      </div>

    </div>

    <!-- Charts Section (Mock em Tempo Real para cada rio) -->
    <div v-if="rios.length > 0" class="charts-grid">
      <div v-for="rio in rios" :key="'chart-' + rio.id" class="chart-section stat-card">
        <div class="chart-header">
          <h2 class="chart-title">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
            {{ rio.nome }} - {{ rio.cidade }}/{{ rio.estado }}
          </h2>
          <span class="live-indicator">
            <span class="live-dot"></span> AO VIVO
          </span>
        </div>
        <div class="chart-container">
          <canvas :ref="el => setChartRef(el, rio.id)"></canvas>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="table-section">
      <div class="table-header">
        <div>
          <h2 class="table-title">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>
            Monitoramento de Rios
          </h2>
        </div>
        <span class="table-count">{{ rios.length }} registros</span>
      </div>

      <!-- Loading Skeleton -->
      <div v-if="loading" class="skeleton-table">
        <div class="skeleton-row" v-for="i in 4" :key="i">
          <div class="skeleton" style="height:16px; width:30%"></div>
          <div class="skeleton" style="height:16px; width:20%"></div>
          <div class="skeleton" style="height:16px; width:10%"></div>
          <div class="skeleton" style="height:24px; width:15%; border-radius:20px"></div>
        </div>
      </div>

      <!-- Table Content -->
      <div v-else class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Nome do Rio</th>
              <th>Cidade</th>
              <th>Estado</th>
              <th>Risco</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="rios.length === 0">
              <td colspan="4" class="empty-state">
                <div class="empty-content">
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M2 18c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/></svg>
                  <p>Nenhum rio cadastrado ainda</p>
                  <span>Cadastre rios na seção "Rios" para visualizar aqui</span>
                </div>
              </td>
            </tr>
            <tr v-for="(rio, i) in rios" :key="rio.id" :style="{ animationDelay: (i * 0.05) + 's' }" class="table-row-animated">
              <td class="td-name">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>
                {{ rio.nome }}
              </td>
              <td>{{ rio.cidade }}</td>
              <td><span class="state-badge">{{ rio.estado }}</span></td>
              <td>
                <span class="badge" :class="getBadgeClass(rio.risco_inundacao)">
                  <span class="badge-dot"></span>
                  {{ rio.risco_inundacao }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import api from '../services/api'
import Chart from 'chart.js/auto'

const chartCanvases = ref({})
let chartInstances = {}
let chartInterval = null

const setChartRef = (el, id) => {
  if (el) {
    chartCanvases.value[id] = el
  }
}


const rios = ref([])
const loading = ref(true)
const lastUpdate = ref('')

const riosAltoRisco = computed(() =>
  rios.value.filter(r => r.risco_inundacao?.toLowerCase() === 'alto').length
)

const riosMedioRisco = computed(() =>
  rios.value.filter(r => r.risco_inundacao?.toLowerCase() === 'médio').length
)

const riskLabel = computed(() => {
  if (riosAltoRisco.value > 0) return 'ALTO'
  if (riosMedioRisco.value > 0) return 'MÉDIO'
  return 'BAIXO'
})

const riskLevel = computed(() => {
  if (riskLabel.value === 'ALTO') return 'high'
  if (riskLabel.value === 'MÉDIO') return 'medium'
  return 'low'
})

const getBadgeClass = (risco) => {
  const r = risco?.toLowerCase()
  if (r === 'alto') return 'badge--high'
  if (r === 'médio') return 'badge--medium'
  return 'badge--low'
}

const load = async () => {
  loading.value = true
  try {
    const res = await api.getRios()
    rios.value = res.data
  } catch (err) {
    console.error('Erro ao carregar rios:', err)
  } finally {
    loading.value = false
    lastUpdate.value = new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    
    await nextTick()
    if (rios.value.length > 0) {
      initCharts()
    }
  }
}

// Inicializa os gráficos mockados em tempo real - modelo Defesa Civil DC-01
const initCharts = () => {
  // Limpar gráficos anteriores caso a função seja chamada mais de uma vez
  Object.values(chartInstances).forEach(chart => chart.destroy())
  chartInstances = {}

  rios.value.forEach(rio => {
    const canvas = chartCanvases.value[rio.id]
    if (!canvas) return

    const ctx = canvas.getContext('2d')

    // Gradiente suave simulando a onda do rio
    const gradient = ctx.createLinearGradient(0, 0, 0, 300)
    gradient.addColorStop(0, 'rgba(0, 174, 239, 0.3)') // Azul Defesa Civil
    gradient.addColorStop(1, 'rgba(0, 174, 239, 0.0)')

    // Base de nível varia dependendo do rio para parecer diferente
    const baseGeral = Math.random() * 1.5 + 0.5 

    const initialData = Array.from({ length: 15 }, () => (Math.random() * 0.3 + baseGeral).toFixed(2))
    const initialLabels = Array.from({ length: 15 }, (_, i) => {
      const d = new Date()
      d.setSeconds(d.getSeconds() - (15 - i) * 2)
      return d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute:'2-digit', second:'2-digit' })
    })

    // Níveis de limite fixos iguais aos do DC-01 (com valores adaptados à base)
    const atencaoLevel = baseGeral + 0.6
    const alertaLevel = baseGeral + 0.9
    const emergenciaLevel = baseGeral + 1.2

    const emergenciaData = Array.from({ length: 15 }, () => emergenciaLevel.toFixed(2))
    const alertaData = Array.from({ length: 15 }, () => alertaLevel.toFixed(2))
    const atencaoData = Array.from({ length: 15 }, () => atencaoLevel.toFixed(2))

    chartInstances[rio.id] = new Chart(ctx, {
      type: 'line',
      data: {
        labels: initialLabels,
        datasets: [
          {
            label: 'Nível (m)',
            data: initialData,
            borderColor: '#00AEEF',
            backgroundColor: gradient,
            borderWidth: 3,
            pointBackgroundColor: '#00AEEF',
            pointBorderColor: '#fff',
            pointBorderWidth: 1,
            pointRadius: 4,
            pointHoverRadius: 6,
            fill: true,
            tension: 0.4
          },
          {
            label: 'Emergência',
            data: emergenciaData,
            borderColor: '#EF4444',
            borderWidth: 2,
            borderDash: [5, 5],
            pointRadius: 0,
            fill: false,
            tension: 0
          },
          {
            label: 'Alerta',
            data: alertaData,
            borderColor: '#F97316',
            borderWidth: 2,
            borderDash: [5, 5],
            pointRadius: 0,
            fill: false,
            tension: 0
          },
          {
            label: 'Atenção',
            data: atencaoData,
            borderColor: '#EAB308',
            borderWidth: 2,
            borderDash: [5, 5],
            pointRadius: 0,
            fill: false,
            tension: 0
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { 
            display: true,
            position: 'top',
            labels: {
              usePointStyle: true,
              color: '#94A3B8'
            }
          },
          tooltip: {
            backgroundColor: '#0F2847',
            titleColor: '#fff',
            bodyColor: '#38BDF8',
            padding: 10,
            displayColors: true
          }
        },
        scales: {
          y: {
            min: Math.max(0, baseGeral - 0.5),
            max: baseGeral + 1.8,
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#94A3B8' }
          },
          x: {
            grid: { display: false },
            ticks: { color: '#94A3B8', maxTicksLimit: 6 }
          }
        }
      }
    })
  })

  // Simulação de atualização a cada 2 segundos
  if (chartInterval) clearInterval(chartInterval)
  chartInterval = setInterval(() => {
    const now = new Date()
    const newLabel = now.toLocaleTimeString('pt-BR', { hour: '2-digit', minute:'2-digit', second:'2-digit' })

    Object.values(chartInstances).forEach(chart => {
      const mainDataset = chart.data.datasets[0]
      const emergenciaDataset = chart.data.datasets[1]
      const alertaDataset = chart.data.datasets[2]
      const atencaoDataset = chart.data.datasets[3]

      const lastValue = parseFloat(mainDataset.data.slice(-1)[0])
      
      // Variação de -0.15 a +0.20 metros
      let newValue = lastValue + (Math.random() * 0.35 - 0.15)
      if (newValue < 0) newValue = Math.abs(newValue)

      chart.data.labels.push(newLabel)
      mainDataset.data.push(newValue.toFixed(2))
      
      emergenciaDataset.data.push(emergenciaDataset.data[0])
      alertaDataset.data.push(alertaDataset.data[0])
      atencaoDataset.data.push(atencaoDataset.data[0])

      if (chart.data.labels.length > 15) {
        chart.data.labels.shift()
        mainDataset.data.shift()
        emergenciaDataset.data.shift()
        alertaDataset.data.shift()
        atencaoDataset.data.shift()
      }

      chart.update()
    })
    lastUpdate.value = newLabel
  }, 2000)
}

onMounted(() => {
  load()
})

onUnmounted(() => {
  if (chartInterval) clearInterval(chartInterval)
  Object.values(chartInstances).forEach(chart => chart.destroy())
})
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 28px;
  animation: fadeInUp 0.4s ease-out;
}

/* Page Header */
.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-top: 4px;
}

.page-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  color: var(--text-muted);
  font-weight: 500;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}

.stat-card {
  position: relative;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 28px 24px;
  overflow: hidden;
  transition: transform var(--transition-normal), border-color var(--transition-normal), box-shadow var(--transition-normal);
}

.stat-card:hover {
  transform: translateY(-4px);
  border-color: var(--accent);
  box-shadow: var(--shadow-md);
}

.stat-card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  flex-shrink: 0;
}

.stat-icon--blue { background: var(--accent-soft); color: var(--accent); }
.stat-icon--red { background: var(--risk-high-bg); color: var(--risk-high); }
.stat-icon--yellow { background: var(--risk-medium-bg); color: var(--risk-medium); }
.stat-icon--risk { background: var(--accent-soft); color: var(--accent); }

.stat-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.stat-value-wrap {
  display: flex;
  flex-direction: column;
}

.stat-number {
  font-size: 2.2rem;
  font-weight: 800;
  color: var(--accent);
  line-height: 1;
  letter-spacing: -0.03em;
}

.stat-number--red { color: var(--risk-high); }
.stat-number--yellow { color: var(--risk-medium); }

.stat-desc {
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-top: 4px;
}

/* Accent stripe */
.stat-accent {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
}

.stat-accent--blue { background: var(--accent-gradient); }
.stat-accent--red { background: linear-gradient(90deg, var(--risk-high), #F97316); }
.stat-accent--yellow { background: linear-gradient(90deg, var(--risk-medium), #EAB308); }

/* Risk card */
.risk-display {
  display: flex;
  align-items: center;
  gap: 10px;
}

.risk-dot {
  width: 12px;
  height: 12px;
  border-radius: var(--radius-full);
}

.risk-dot--high { background: var(--risk-high); animation: pulse 1.5s infinite; }
.risk-dot--medium { background: var(--risk-medium); }
.risk-dot--low { background: var(--risk-low); }

.risk-text {
  font-size: 1.6rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.stat-card--high .risk-text { color: var(--risk-high); }
.stat-card--medium .risk-text { color: var(--risk-medium); }
.stat-card--low .risk-text { color: var(--risk-low); }

.stat-card--high { border-color: var(--risk-high); }

/* Charts Section */
.charts-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}

.chart-section {
  padding: 0; /* Removing default padding from stat-card */
  display: flex;
  flex-direction: column;
}

.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-light);
}

.chart-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-primary);
}

.live-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
  font-weight: 800;
  color: #EF4444;
  letter-spacing: 0.5px;
  background: rgba(239, 68, 68, 0.1);
  padding: 4px 10px;
  border-radius: var(--radius-sm);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.live-dot {
  width: 8px;
  height: 8px;
  background-color: #EF4444;
  border-radius: 50%;
  animation: pulse 1.5s infinite;
}

.chart-container {
  height: 300px;
  padding: 20px 24px;
  width: 100%;
}

/* Table Section */
.table-section {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  transition: transform var(--transition-normal), border-color var(--transition-normal), box-shadow var(--transition-normal);
}
.table-section:hover {
  transform: translateY(-2px);
  border-color: var(--accent);
  box-shadow: var(--shadow-md);
}

.table-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-light);
}

.table-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-primary);
}

.table-title svg {
  color: var(--accent);
}

.table-count {
  font-size: 0.8rem;
  color: var(--text-muted);
  font-weight: 500;
  background: var(--bg-secondary);
  padding: 4px 12px;
  border-radius: var(--radius-full);
}

.table-wrapper {
  overflow-x: auto;
}

.td-name {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.state-badge {
  display: inline-block;
  padding: 2px 10px;
  background: var(--bg-secondary);
  border-radius: var(--radius-full);
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-secondary);
}

/* Badges */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: capitalize;
}

.badge-dot {
  width: 7px;
  height: 7px;
  border-radius: var(--radius-full);
}

.badge--high { background: var(--risk-high-bg); color: var(--risk-high); }
.badge--high .badge-dot { background: var(--risk-high); }

.badge--medium { background: var(--risk-medium-bg); color: var(--risk-medium); }
.badge--medium .badge-dot { background: var(--risk-medium); }

.badge--low { background: var(--risk-low-bg); color: var(--risk-low); }
.badge--low .badge-dot { background: var(--risk-low); }

/* Empty State */
.empty-state {
  text-align: center;
  padding: 48px 24px !important;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: var(--text-muted);
}

.empty-content p {
  font-weight: 600;
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.empty-content span {
  font-size: 0.85rem;
}

/* Skeleton */
.skeleton-table {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.skeleton-row {
  display: flex;
  gap: 24px;
  align-items: center;
}

.skeleton-row > * {
  height: 16px;
}

/* Row Animation */
.table-row-animated {
  animation: fadeInUp 0.3s ease-out both;
}

/* Responsive */
@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .stat-number {
    font-size: 1.8rem;
  }
}
</style>