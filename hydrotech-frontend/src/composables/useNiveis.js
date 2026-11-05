/**
 * Fonte única de rios, pontos, nível do rio e localização do visitante.
 *
 * Todas as telas (início, monitoramento, rota de fuga, dashboard) usam este
 * módulo, então o status de um ponto é o mesmo em qualquer lugar do site.
 * Os níveis ainda são simulados no navegador (como antes), mas agora seguem
 * o cenário escolhido no /simulador.
 */
import { ref, reactive, computed } from 'vue'
import api from '@/services/api'
import { useSimulacao } from './useSimulacao'

export const INTERVALO_MS = 5000
const PONTOS_HISTORICO = 24

/* ── Classificação de risco ──
 * Para o público usamos SEMPRE as mesmas três palavras: Normal / Atenção / Perigo.
 * Equivalem ao risco Baixo / Médio / Alto do escopo do projeto.
 */
export const RISCO = {
  baixo: { nivel: 'baixo', rotulo: 'Normal',  escopo: 'Baixo', titulo: 'Rio normal',           frase: 'O nível está dentro do normal. Não é preciso sair.' },
  medio: { nivel: 'medio', rotulo: 'Atenção', escopo: 'Médio', titulo: 'Atenção: rio subindo', frase: 'Fique atento e prepare-se para sair se piorar.' },
  alto:  { nivel: 'alto',  rotulo: 'Perigo',  escopo: 'Alto',  titulo: 'Perigo de enchente',   frase: 'Saia da área de risco agora.' },
}

export function limitesDe(ponto) {
  const n = v => (v === null || v === undefined || v === '' ? null : Number(v))
  const base = n(ponto.nivel_base) ?? 1
  const atencao = n(ponto.limite_atencao) ?? base + 0.5
  const alerta = n(ponto.limite_alerta) ?? base + 1.5
  const emergencia = n(ponto.limite_emergencia) ?? base + 2.5
  return { base, atencao, alerta, emergencia }
}

export function classificar(valor, limites) {
  if (valor == null) return RISCO.baixo
  if (valor >= limites.emergencia) return RISCO.alto
  if (valor >= limites.alerta) return RISCO.medio
  return RISCO.baixo
}

export function distanciaM(aLat, aLng, bLat, bLng) {
  const r = d => d * Math.PI / 180
  const h = Math.sin(r(bLat - aLat) / 2) ** 2 + Math.cos(r(aLat)) * Math.cos(r(bLat)) * Math.sin(r(bLng - aLng) / 2) ** 2
  return 2 * 6371000 * Math.asin(Math.sqrt(h))
}

export const formatarNivel = v => v == null ? '—' : `${Number(v).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} m`
export const formatarDistancia = m => m >= 1000 ? `${(m / 1000).toLocaleString('pt-BR', { maximumFractionDigits: 1 })} km` : `${Math.round(m)} m`

/* ── Estado compartilhado (singleton) ── */
const rios = ref([])
const pontos = ref([])
const carregando = ref(false)
const erro = ref('')
const series = reactive({})            // id → [{ t, v }]
const ultimaAtualizacao = ref(null)
let relogio = null
const registro = new Map()         // id → ponto (para o relógio saber quem atualizar)

const sim = useSimulacao()

function alvo(ponto) {
  const l = limitesDe(ponto)
  const cenario = sim.cenarioDe(ponto.id)
  if (cenario === 'alto') return l.emergencia + 0.6
  if (cenario === 'medio') return (l.alerta + l.emergencia) / 2
  return l.base
}

function proximoValor(ponto, atual) {
  const l = limitesDe(ponto)
  const destino = alvo(ponto)
  const ruido = (Math.random() - 0.5) * 0.16
  const passo = Math.max(-0.45, Math.min(0.45, (destino - atual) * 0.45))
  let v = atual + passo + ruido
  if (sim.cenarioDe(ponto.id) === 'normal') v = Math.min(v, l.alerta - 0.15)
  return Math.max(0, +v.toFixed(2))
}

/** Garante uma série para o ponto (usado também pelo dashboard, que carrega pontos autenticados). */
export function garantirSerie(ponto) {
  if (series[ponto.id]) return series[ponto.id]
  const agora = Date.now()
  const destino = alvo(ponto)
  const l = limitesDe(ponto)
  const lista = []
  let v = l.base
  for (let i = PONTOS_HISTORICO - 1; i >= 0; i--) {
    v = i < 6 ? v + (destino - v) * 0.35 : l.base + (Math.random() - 0.5) * 0.2
    lista.push({ t: agora - i * INTERVALO_MS, v: Math.max(0, +v.toFixed(2)) })
  }
  series[ponto.id] = lista
  registro.set(ponto.id, ponto)
  return lista
}

function tick() {
  const t = Date.now()
  for (const [id, ponto] of registro) {
    const lista = series[id]
    if (!lista) continue
    lista.push({ t, v: proximoValor(ponto, lista.at(-1).v) })
    if (lista.length > PONTOS_HISTORICO) lista.shift()
  }
  ultimaAtualizacao.value = t
}

function ligarRelogio() {
  if (!relogio) relogio = setInterval(tick, INTERVALO_MS)
}

/**
 * Busca rios e pontos no Django. Sempre busca de novo quando chamada (cada tela
 * chama ao abrir) e a cada minuto, para refletir rios cadastrados depois.
 * Enquanto atualiza, os dados anteriores continuam na tela.
 */
let buscando = null
let atualizador = null
let tentativas = 0
let reintento = null              // nova tentativa já agendada (evita tentativas em paralelo)
const MAX_TENTATIVAS = 18          // ~90 s: tempo para o servidor gratuito (Render) acordar
/** true quando a primeira carga está demorando (servidor “acordando”). */
const demorando = ref(false)

function carregar() {
  if (buscando) return buscando
  if (reintento) return Promise.resolve()
  const primeiraVez = !rios.value.length && !pontos.value.length
  if (primeiraVez) carregando.value = true
  const avisoLento = primeiraVez ? setTimeout(() => { if (carregando.value) demorando.value = true }, 4000) : null
  let tentarDeNovo = false
  buscando = (async () => {
    try {
      const res = await api.getRiosPublico()
      const listaRios = Array.isArray(res.data) ? res.data : res.data.results || []
      const listas = await Promise.all(listaRios.map(async rio => {
        try {
          const pr = await api.getPontosRiscoPublico(rio.id)
          const itens = Array.isArray(pr.data) ? pr.data : pr.data.results || []
          return itens.map(p => ({ ...p, rioId: rio.id, rioNome: rio.nome, cidade: rio.cidade, estado: rio.estado }))
        } catch { return [] }
      }))
      const novos = listas.flat()
      novos.forEach(p => { registro.set(p.id, p); garantirSerie(p) })
      const ids = new Set(novos.map(p => p.id))
      for (const id of [...registro.keys()]) if (!ids.has(id) && pontos.value.some(p => p.id === id)) { registro.delete(id); delete series[id] }
      rios.value = listaRios
      pontos.value = novos
      erro.value = ''
      tentativas = 0
      demorando.value = false
      ultimaAtualizacao.value = Date.now()
      ligarRelogio()
      if (!atualizador) atualizador = setInterval(() => carregar(), 60000)
    } catch (e) {
      console.error('Erro ao carregar rios:', e)
      if (!rios.value.length) {
        // Primeira carga falhou: o servidor pode estar acordando. Tenta de novo sozinho.
        if (++tentativas < MAX_TENTATIVAS) { tentarDeNovo = true; demorando.value = true }
        else { erro.value = 'Não foi possível conectar ao servidor do HydroTech. Verifique sua internet e tente de novo.'; demorando.value = false; tentativas = 0 }
      }
    } finally {
      clearTimeout(avisoLento)
      buscando = null
      if (tentarDeNovo) reintento = setTimeout(() => { reintento = null; carregar() }, 5000)
      else carregando.value = false
    }
  })()
  return buscando
}

/* ── Localização do visitante (simulada pelo /simulador ou GPS real) ── */
const gps = ref(null)                   // { lat, lng }
const gpsStatus = ref('ocioso')         // ocioso | buscando | ok | negado | indisponivel

function pedirGps() {
  if (sim.estado.value.local) return Promise.resolve()
  if (!navigator.geolocation) { gpsStatus.value = 'indisponivel'; return Promise.resolve() }
  if (gpsStatus.value === 'buscando') return Promise.resolve()
  gpsStatus.value = 'buscando'
  return new Promise(resolve => {
    let terminou = false
    const fim = status => { if (terminou) return; terminou = true; clearTimeout(limite); gpsStatus.value = status; resolve() }
    // O Chrome não conta o "timeout" enquanto o pedido de permissão está aberto; este limite cobre isso.
    const limite = setTimeout(() => fim('timeout'), 15000)
    navigator.geolocation.getCurrentPosition(
      pos => { gps.value = { lat: pos.coords.latitude, lng: pos.coords.longitude }; fim('ok') },
      err => fim(err?.code === 1 ? 'negado' : 'timeout'),
      { enableHighAccuracy: true, timeout: 12000, maximumAge: 60000 },
    )
  })
}

export function useNiveis() {
  ligarRelogio()

  const localizacao = computed(() => {
    const local = sim.estado.value.local
    if (local) return { lat: local.lat, lng: local.lng, fonte: 'simulada' }
    return gps.value ? { ...gps.value, fonte: 'gps' } : null
  })

  const statusDe = ponto => {
    const lista = series[ponto.id] || garantirSerie(ponto)
    return classificar(lista.at(-1)?.v, limitesDe(ponto))
  }

  const nivelAtual = ponto => (series[ponto.id] || garantirSerie(ponto)).at(-1)?.v ?? null

  const tendencia = ponto => {
    const lista = series[ponto.id]
    if (!lista || lista.length < 4) return 0
    return +(lista.at(-1).v - lista.at(-4).v).toFixed(2)
  }

  /** Pontos ordenados do mais perto para o mais longe da localização atual. */
  const pontosPorDistancia = computed(() => {
    const loc = localizacao.value
    if (!loc) return []
    return pontos.value
      .map(p => ({ ponto: p, distancia: distanciaM(loc.lat, loc.lng, p.latitude, p.longitude) }))
      .sort((a, b) => a.distancia - b.distancia)
  })

  const pontosEmAlerta = computed(() => {
    void ultimaAtualizacao.value
    return pontos.value.filter(p => statusDe(p).nivel === 'alto')
  })

  return {
    rios, pontos, carregando, erro, demorando, series, ultimaAtualizacao,
    carregar, statusDe, nivelAtual, tendencia,
    localizacao, gpsStatus, pedirGps, pontosPorDistancia, pontosEmAlerta,
  }
}
