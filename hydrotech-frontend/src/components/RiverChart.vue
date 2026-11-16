<template>
  <div class="rchart" :class="{ 'rchart--compact': compacto }">
    <div v-if="!semCabecalho" class="rchart-head">
      <div class="rchart-now">
        <strong class="rchart-value" :class="'tone--' + risco.nivel">{{ margemTexto }}</strong>
        <span class="rchart-sub">
          Nível do rio: <b>{{ formatarNivel(atual) }}</b>
          <span class="rchart-trend" :class="trendClass">
            <svg v-if="tendencia > 0.04" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5" /><path d="m5 12 7-7 7 7" /></svg>
            <svg v-else-if="tendencia < -0.04" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14" /><path d="m19 12-7 7-7-7" /></svg>
            <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><path d="M5 12h14" /></svg>
            {{ textoTendencia }}
          </span>
        </span>
      </div>
      <RiskPill v-if="!semRisco" :risco="risco" />
    </div>

    <!-- Medidor: onde o rio está entre normal, atenção e perigo -->
    <div v-if="!semCabecalho" class="meter" role="meter" :aria-valuenow="atual" :aria-valuemin="0" :aria-valuemax="escala" :aria-label="`Nível do rio ${formatarNivel(atual)}; perigo a partir de ${formatarNivel(limites.emergencia)}`">
      <div class="meter-track">
        <span class="meter-seg meter-seg--baixo" :style="{ width: pct(limites.alerta) + '%' }"></span>
        <span class="meter-seg meter-seg--medio" :style="{ width: (pct(limites.emergencia) - pct(limites.alerta)) + '%' }"></span>
        <span class="meter-seg meter-seg--alto" :style="{ width: (100 - pct(limites.emergencia)) + '%' }"></span>
        <span class="meter-mark" :style="{ left: pct(atual) + '%' }"></span>
      </div>
      <div v-if="!compacto" class="meter-labels">
        <span>Normal</span>
        <span :style="{ left: pct(limites.alerta) + '%' }">Atenção</span>
        <span :style="{ left: pct(limites.emergencia) + '%' }">Perigo</span>
      </div>
    </div>

    <div class="rchart-canvas" :style="{ height: altura + 'px' }">
      <canvas ref="canvas" role="img" :aria-label="`Gráfico do nível do rio: ${formatarNivel(atual)}, ${risco.titulo}`"></canvas>
    </div>

    <p v-if="!compacto" class="rchart-foot">
      Gráfico dos últimos {{ minutos }}. A faixa vermelha é o nível de perigo, a partir de {{ formatarNivel(limites.emergencia) }}.
    </p>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import Chart from 'chart.js/auto'
import RiskPill from './RiskPill.vue'
import { useNiveis, limitesDe, classificar, formatarNivel, garantirSerie } from '@/composables/useNiveis'

const props = defineProps({
  ponto: { type: Object, required: true },
  altura: { type: Number, default: 220 },
  compacto: { type: Boolean, default: false },
  semCabecalho: { type: Boolean, default: false },
  semRisco: { type: Boolean, default: false },
})

const { series, tendencia: tendenciaDe } = useNiveis()
garantirSerie(props.ponto)

const canvas = ref(null)
let chart = null
let temaObserver = null

const serie = computed(() => series[props.ponto.id] || [])
const limites = computed(() => limitesDe(props.ponto))
const atual = computed(() => serie.value.at(-1)?.v ?? null)
const risco = computed(() => classificar(atual.value, limites.value))
const tendencia = computed(() => { void serie.value.at(-1); return tendenciaDe(props.ponto) })
// Variação nos últimos 3 registros (≈15 s), traduzida em palavras
const textoTendencia = computed(() => {
  const t = tendencia.value
  if (t > 0.3) return 'subindo rápido'
  if (t > 0.04) return 'subindo'
  if (t < -0.04) return 'baixando'
  return 'estável'
})
/** O que importa para quem mora perto: quanto falta para o perigo. */
const margemTexto = computed(() => {
  if (atual.value == null) return 'Sem leitura agora'
  const falta = limites.value.emergencia - atual.value
  if (falta <= 0) return `${formatarNivel(-falta)} acima do perigo`
  return `Faltam ${formatarNivel(falta)} para o perigo`
})
const escala = computed(() => Math.max(limites.value.emergencia * 1.25, (atual.value ?? 0) + 0.3))
const pct = v => Math.max(0, Math.min(100, ((v ?? 0) / escala.value) * 100))
const trendClass = computed(() => tendencia.value > 0.04 ? 'tone--alto' : tendencia.value < -0.04 ? 'tone--baixo' : '')
const minutos = computed(() => {
  const s = serie.value
  if (s.length < 2) return '2 minutos'
  const m = Math.round((s.at(-1).t - s[0].t) / 60000)
  return m <= 1 ? '2 minutos' : `${m} minutos`
})

const hora = t => new Date(t).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
const css = nome => getComputedStyle(document.documentElement).getPropertyValue(nome).trim()

function hexA(cor, alfa) {
  const m = cor.match(/^#([0-9a-f]{6})$/i)
  if (!m) return cor
  const n = parseInt(m[1], 16)
  return `rgba(${n >> 16 & 255}, ${n >> 8 & 255}, ${n & 255}, ${alfa})`
}

/** Plugin: faixas de risco no fundo (modelo de hidrograma com cotas de alerta). */
const faixasPlugin = {
  id: 'faixasRisco',
  beforeDatasetsDraw(c, _args, opts) {
    const { ctx, chartArea: a, scales: { y } } = c
    if (!a) return
    ctx.save()
    for (const f of opts.faixas) {
      const topo = y.getPixelForValue(Math.min(f.ate, y.max))
      const base = y.getPixelForValue(Math.max(f.de, y.min))
      if (base <= a.top || topo >= a.bottom) continue
      const t = Math.max(topo, a.top), b = Math.min(base, a.bottom)
      ctx.fillStyle = f.fundo
      ctx.fillRect(a.left, t, a.right - a.left, b - t)
      if (f.linha) {
        ctx.strokeStyle = f.linha
        ctx.lineWidth = 1
        ctx.setLineDash([4, 4])
        ctx.beginPath(); ctx.moveTo(a.left, b + 0.5); ctx.lineTo(a.right, b + 0.5); ctx.stroke()
        ctx.setLineDash([])
      }
      if (f.rotulo && b - t > 16) {
        ctx.fillStyle = f.texto
        ctx.font = '700 11px Inter, system-ui, sans-serif'
        ctx.textAlign = 'left'
        ctx.textBaseline = 'top'
        ctx.fillText(f.rotulo, a.left + 8, t + 6)
      }
    }
    ctx.restore()
  },
}

/** Plugin: destaca o último ponto com um halo. */
const ultimoPontoPlugin = {
  id: 'ultimoPonto',
  afterDatasetsDraw(c, _args, opts) {
    const meta = c.getDatasetMeta(0)
    const p = meta.data.at(-1)
    if (!p) return
    const { ctx } = c
    ctx.save()
    ctx.fillStyle = hexA(opts.cor, 0.25)
    ctx.beginPath(); ctx.arc(p.x, p.y, 10, 0, Math.PI * 2); ctx.fill()
    ctx.fillStyle = opts.cor
    ctx.strokeStyle = opts.borda
    ctx.lineWidth = 2
    ctx.beginPath(); ctx.arc(p.x, p.y, 5, 0, Math.PI * 2); ctx.fill(); ctx.stroke()
    ctx.restore()
  },
}

function maxY() {
  const maior = Math.max(...serie.value.map(p => p.v), limites.value.emergencia)
  return Math.ceil((maior + 0.6) * 2) / 2
}

function construir() {
  if (!canvas.value) return
  chart?.destroy()
  const l = limites.value
  const agua = css('--water') || '#38BDF8'
  const texto = css('--text-muted')
  const verde = css('--risk-low') || '#10B981'
  const ambar = css('--risk-medium-solid') || '#F59E0B'
  const vermelho = css('--risk-high') || '#DC2626'
  const ctx = canvas.value.getContext('2d')
  const grad = ctx.createLinearGradient(0, 0, 0, props.altura)
  grad.addColorStop(0, hexA(agua, 0.35))
  grad.addColorStop(1, hexA(agua, 0.02))

  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: serie.value.map(p => p.t),
      datasets: [{
        label: 'Nível do rio',
        data: serie.value.map(p => p.v),
        borderColor: agua,
        backgroundColor: grad,
        borderWidth: 3,
        pointRadius: 0,
        pointHoverRadius: 5,
        pointHitRadius: 12,
        fill: 'start',
        tension: 0.35,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      interaction: { mode: 'index', intersect: false },
      layout: { padding: { top: 4, right: 4 } },
      plugins: {
        legend: { display: false },
        faixasRisco: {
          faixas: [
            { de: 0, ate: l.alerta, fundo: hexA(verde, 0.07), texto: hexA(verde, 0.9), rotulo: props.compacto ? '' : 'Normal' },
            { de: l.alerta, ate: l.emergencia, fundo: hexA(ambar, 0.13), texto: ambar, linha: hexA(ambar, 0.7), rotulo: 'Atenção' },
            { de: l.emergencia, ate: 999, fundo: hexA(vermelho, 0.16), texto: vermelho, linha: hexA(vermelho, 0.8), rotulo: 'Perigo' },
          ],
        },
        ultimoPonto: { cor: agua, borda: css('--bg-card') || '#fff' },
        tooltip: {
          backgroundColor: css('--bg-elevated'),
          titleColor: css('--text-secondary'),
          bodyColor: css('--text-primary'),
          borderColor: css('--border'),
          borderWidth: 1,
          padding: 10,
          displayColors: false,
          callbacks: {
            title: items => hora(items[0].label * 1),
            label: item => `Nível: ${formatarNivel(item.raw)}`,
          },
        },
      },
      scales: {
        y: {
          min: 0,
          max: maxY(),
          grid: { display: false },
          border: { display: false },
          ticks: { color: texto, font: { size: 11 }, stepSize: 1, callback: v => `${v} m` },
        },
        x: {
          grid: { display: false },
          border: { color: css('--border') },
          ticks: {
            color: texto,
            font: { size: 11 },
            maxRotation: 0,
            autoSkip: true,
            maxTicksLimit: props.compacto ? 3 : 5,
            callback(_v, i) { return new Date(this.getLabelForValue(i) * 1).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }) },
          },
        },
      },
    },
    plugins: [faixasPlugin, ultimoPontoPlugin],
  })
}

function atualizar() {
  if (!chart) return
  chart.data.labels = serie.value.map(p => p.t)
  chart.data.datasets[0].data = serie.value.map(p => p.v)
  chart.options.scales.y.max = maxY()
  chart.update('none')
}

watch(() => serie.value.at(-1)?.t, atualizar)
watch(() => props.ponto.id, construir)

onMounted(() => {
  construir()
  temaObserver = new MutationObserver(() => construir())
  temaObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] })
})
onUnmounted(() => { chart?.destroy(); temaObserver?.disconnect() })
</script>

<style scoped>
.rchart { display: flex; flex-direction: column; gap: 12px; }
.rchart-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
.rchart-now { display: flex; flex-direction: column; gap: 4px; }
.rchart-value { font-size: var(--fs-lg); font-weight: 800; line-height: 1.2; font-variant-numeric: tabular-nums; }
.rchart-sub { display: flex; flex-wrap: wrap; align-items: center; gap: 4px 10px; font-size: var(--fs-sm); color: var(--text-secondary); }
.rchart-sub b { color: var(--text-primary); font-variant-numeric: tabular-nums; }
.rchart-trend { display: inline-flex; align-items: center; gap: 4px; font-weight: 700; }

.meter { display: flex; flex-direction: column; gap: 6px; }
.meter-track { position: relative; display: flex; height: 12px; border-radius: var(--radius-full); overflow: visible; }
.meter-seg { height: 100%; }
.meter-seg--baixo { background: var(--risk-low); opacity: .55; border-radius: var(--radius-full) 0 0 var(--radius-full); }
.meter-seg--medio { background: var(--risk-medium-solid); opacity: .7; }
.meter-seg--alto  { background: var(--risk-high); opacity: .8; border-radius: 0 var(--radius-full) var(--radius-full) 0; }
.meter-mark {
  position: absolute; top: 50%; width: 22px; height: 22px; border-radius: 50%;
  transform: translate(-50%, -50%); background: var(--water); border: 4px solid var(--bg-card);
  box-shadow: 0 0 0 2px var(--water); transition: left .6s ease;
}
.meter-labels { position: relative; height: 18px; font-size: var(--fs-xs); color: var(--text-muted); font-weight: 600; }
.meter-labels span { position: absolute; white-space: nowrap; }
.meter-labels span:first-child { left: 0; }
.meter-labels span + span { transform: translateX(-2px); }
@media (prefers-reduced-motion: reduce) { .meter-mark { transition: none; } }
.rchart-canvas { position: relative; width: 100%; }
.rchart-foot { font-size: var(--fs-xs); color: var(--text-muted); line-height: 1.5; }
.rchart--compact .rchart-value { font-size: var(--fs-md); }
.tone--baixo { color: var(--risk-low-text); }
.tone--medio { color: var(--risk-medium-text); }
.tone--alto  { color: var(--risk-high-text); }
</style>
