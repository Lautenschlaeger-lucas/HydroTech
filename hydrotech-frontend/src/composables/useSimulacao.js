/**
 * Estado da simulação de enchente (demonstração acadêmica).
 *
 * Quem controla é a página /simulador, que não aparece em nenhum menu.
 * As telas públicas só LEEM este estado.
 *
 * Transporte atual: localStorage + BroadcastChannel → funciona entre abas e
 * janelas do MESMO navegador (ex.: simulador numa janela fora do projetor).
 * Para controlar de outro aparelho (computador → celular), basta trocar
 * `lerRemoto`/`salvarRemoto` por chamadas a um endpoint do backend.
 */
import { ref, readonly } from 'vue'

const CHAVE = 'ht_simulacao'
const CANAL = 'hydrotech-simulacao'

/** Estados possíveis de cada ponto na simulação. */
export const CENARIOS = ['normal', 'medio', 'alto']

const vazio = () => ({ pontos: {}, local: null, atualizadoEm: 0 })

function ler() {
  try {
    const bruto = JSON.parse(localStorage.getItem(CHAVE) || 'null')
    if (bruto && typeof bruto === 'object') return { ...vazio(), ...bruto }
  } catch { /* storage indisponível */ }
  return vazio()
}

const estado = ref(ler())
let canal = null
let iniciado = false

function iniciar() {
  if (iniciado || typeof window === 'undefined') return
  iniciado = true
  window.addEventListener('storage', e => { if (e.key === CHAVE) estado.value = ler() })
  try {
    canal = new BroadcastChannel(CANAL)
    canal.onmessage = () => { estado.value = ler() }
  } catch { /* navegador sem BroadcastChannel: o evento storage cobre */ }
}

function salvar(novo) {
  novo.atualizadoEm = Date.now()
  estado.value = novo
  try { localStorage.setItem(CHAVE, JSON.stringify(novo)) } catch { /* ignora */ }
  try { canal?.postMessage('mudou') } catch { /* ignora */ }
}

export function useSimulacao() {
  iniciar()
  return {
    estado: readonly(estado),
    /** Cenário de um ponto: 'normal' | 'medio' | 'alto'. */
    cenarioDe: id => estado.value.pontos[id] || 'normal',
    definirCenario(id, cenario) {
      const pontos = { ...estado.value.pontos }
      if (cenario === 'normal') delete pontos[id]
      else pontos[id] = cenario
      salvar({ ...estado.value, pontos })
    },
    /** Coloca o "visitante" dentro da área de risco de um ponto (ou null para usar o GPS real). */
    definirLocal(ponto) {
      salvar({ ...estado.value, local: ponto ? { pontoId: ponto.id, lat: ponto.latitude + 0.0008, lng: ponto.longitude + 0.0008 } : null })
    },
    resetar() { salvar(vazio()) },
  }
}
