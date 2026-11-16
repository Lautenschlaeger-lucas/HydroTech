<template>
  <div class="mon">
    <!-- Alerta ativo: sempre no topo, com atalho direto para a rota -->
    <router-link v-if="alerta" :to="rotaPara(alerta)" class="mon-alert" role="alert">
      <RiskIcon nivel="alto" :size="22" />
      <span class="mon-alert-txt">
        <strong>Perigo de enchente</strong>
        <span>{{ alerta.descricao }} · {{ alerta.rioNome }}</span>
      </span>
      <span class="mon-alert-cta">Rota de fuga →</span>
    </router-link>

    <div class="mon-wrap">
      <div class="mon-head">
        <h1>Rios monitorados</h1>
        <div class="tabs" role="tablist" aria-label="Como mostrar os rios">
          <button type="button" role="tab" :aria-selected="modo === 'todos'" :class="{ on: modo === 'todos' }" @click="mudarModo('todos')">Todos os rios</button>
          <button type="button" role="tab" :aria-selected="modo === 'perto'" :class="{ on: modo === 'perto' }" @click="mudarModo('perto')">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z" /><circle cx="12" cy="10" r="3" /></svg>
            Perto de mim
          </button>
        </div>
      </div>

      <div v-if="carregando" class="mine-card mine-card--loading" aria-busy="true" aria-live="polite">
        <span class="spinner" aria-hidden="true"></span>
        <template v-if="demorando">
          <p class="mine-empty-title">Conectando ao servidor…</p>
          <p>Na primeira visita isso pode levar até 1 minuto. Já estamos tentando de novo, não precisa recarregar.</p>
        </template>
        <p v-else>Carregando rios…</p>
      </div>

      <div v-else-if="erro" class="mine-card mine-card--empty">
        <p>{{ erro }}</p>
        <button class="btn btn--primary" type="button" @click="recarregar">Tentar de novo</button>
      </div>

      <template v-else>
        <!-- ═══ PERTO DE MIM: aguardando / bloqueado ═══ -->
        <div v-if="modo === 'perto' && !localizacao" class="mine-card mine-card--empty">
          <template v-if="gpsStatus === 'buscando'">
            <span class="spinner" aria-hidden="true"></span>
            <p class="mine-empty-title">Aguardando sua localização…</p>
            <p>Se o navegador perguntar, toque em <b>Permitir</b>.</p>
          </template>
          <template v-else>
            <p class="mine-empty-title">{{ gpsStatus === 'negado' || gpsStatus === 'timeout' ? 'Não conseguimos sua localização' : 'Encontre o rio mais perto de você' }}</p>
            <p v-if="gpsStatus === 'negado'">A localização está bloqueada no navegador. Libere no ícone ao lado do endereço do site ou escolha seu rio na lista abaixo.</p>
            <p v-else-if="gpsStatus === 'timeout'">O GPS demorou para responder. Tente de novo ou escolha seu rio na lista abaixo.</p>
            <button class="btn btn--primary btn--lg btn--block" type="button" @click="pedirGps">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="3" /><path d="M12 2v3M12 19v3M2 12h3M19 12h3" /><circle cx="12" cy="12" r="8" /></svg>
              Usar minha localização
            </button>
          </template>
        </div>

        <!-- ═══ SEU RIO (mais perto, escolhido ou favorito) ═══ -->
        <section v-if="meuPonto" class="mine" aria-labelledby="mine-title">
          <div class="mine-head">
            <h2 id="mine-title">Seu rio</h2>
            <p class="mine-where">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z" /><circle cx="12" cy="10" r="3" /></svg>
              {{ textoOrigem }}
            </p>
          </div>

          <article class="mine-card" :class="'mine-card--' + meuRisco.nivel">
            <div class="mine-status">
              <span class="mine-status-icon"><RiskIcon :nivel="meuRisco.nivel" :size="30" /></span>
              <div>
                <p class="mine-status-title">{{ meuRisco.titulo }}</p>
                <p class="mine-status-text">{{ meuRisco.frase }}</p>
              </div>
            </div>

            <div class="mine-place">
              <h3>{{ meuPonto.descricao }}</h3>
              <p>{{ meuPonto.rioNome }} · {{ meuPonto.cidade }}/{{ meuPonto.estado }}</p>
            </div>

            <RiverChart :ponto="meuPonto" :altura="200" sem-risco />

            <router-link :to="rotaPara(meuPonto)" class="btn btn--lg btn--block" :class="meuRisco.nivel === 'baixo' ? 'btn--primary' : 'btn--danger'">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="6" cy="19" r="2.5" /><circle cx="18" cy="5" r="2.5" /><path d="M8.5 19H15a3.5 3.5 0 0 0 0-7H9a3.5 3.5 0 0 1 0-7h6.5" /></svg>
              Ver rota de fuga
            </router-link>

            <div class="mine-actions">
              <PontoAcoes :ponto="meuPonto" />
              <button class="btn btn--ghost btn--sm" type="button" :aria-expanded="geminiAberto === meuPonto.rioId" @click="alternarGemini(meuPonto.rioId)">Sobre o rio</button>
              <button v-if="escolhidoId === meuPonto.id" class="btn btn--ghost btn--sm" type="button" @click="limparEscolha">Trocar</button>
            </div>
            <GeminiPainel v-if="geminiAberto === meuPonto.rioId" :rio-id="meuPonto.rioId" />
          </article>
        </section>

        <!-- ═══ TODOS OS RIOS ═══ -->
        <section class="all" aria-labelledby="all-title">
          <div class="all-head">
            <h2 id="all-title">{{ modo === 'perto' && localizacao ? 'Rios por distância' : 'Todos os rios' }} <span class="all-count">{{ grupos.length }}</span></h2>
            <select v-if="cidades.length > 1" v-model="filtroCidade" class="all-filter" aria-label="Filtrar por cidade">
              <option value="">Todas as cidades</option>
              <option v-for="c in cidades" :key="c" :value="c">{{ c }}</option>
            </select>
          </div>

          <p v-if="!grupos.length" class="mine-card mine-card--empty">Nenhum rio cadastrado ainda.</p>

          <ul class="rivers">
            <li v-for="g in grupos" :key="g.rio.id" class="river" :class="'river--' + g.pior.nivel">
              <div class="river-head">
                <span class="river-icon" :class="'tone--' + g.pior.nivel">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1" /><path d="M2 18c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1" /></svg>
                </span>
                <div class="river-info">
                  <h3>{{ g.rio.nome }}</h3>
                  <small>{{ g.rio.cidade }}/{{ g.rio.estado }}<template v-if="g.distancia != null"> · {{ formatarDistancia(g.distancia) }}</template></small>
                </div>
                <RiskPill v-if="g.pontos.length" :risco="g.pior" />
              </div>

              <p v-if="!g.pontos.length" class="river-empty">Nenhum ponto de monitoramento cadastrado neste rio.</p>
              <ul v-else class="all-list">
                <li v-for="p in g.pontos" :key="p.id" class="row" :class="{ 'row--open': aberto === p.id }" :id="'ponto-' + p.id">
                  <button class="row-btn" type="button" :aria-expanded="aberto === p.id" @click="aberto = aberto === p.id ? null : p.id">
                    <span class="row-icon" :class="'tone--' + statusDe(p).nivel"><RiskIcon :nivel="statusDe(p).nivel" :size="22" /></span>
                    <span class="row-info">
                      <strong>{{ p.descricao }}</strong>
                      <small v-if="distanciaDe(p) != null">{{ formatarDistancia(distanciaDe(p)) }} de você</small>
                    </span>
                    <span class="row-level">
                      <b :class="'tone--' + statusDe(p).nivel">{{ statusDe(p).rotulo }}</b>
                      <small>{{ formatarNivel(nivelAtual(p)) }}</small>
                    </span>
                    <svg class="row-chev" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="m6 9 6 6 6-6" /></svg>
                  </button>
                  <div v-if="aberto === p.id" class="row-body">
                    <RiverChart :ponto="p" :altura="170" compacto />
                    <div class="row-actions">
                      <router-link :to="rotaPara(p)" class="btn btn--primary btn--sm">Rota de fuga</router-link>
                      <button class="btn btn--ghost btn--sm" type="button" @click="escolher(p)">Este é o meu rio</button>
                      <PontoAcoes :ponto="p" />
                    </div>
                  </div>
                </li>
              </ul>
            </li>
          </ul>
        </section>
      </template>

      <p class="mon-note">Protótipo acadêmico · níveis e alertas desta página são simulados · atualiza a cada 5 s{{ horaAtualizacao ? ` · ${horaAtualizacao}` : '' }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import RiverChart from '@/components/RiverChart.vue'
import RiskIcon from '@/components/RiskIcon.vue'
import RiskPill from '@/components/RiskPill.vue'
import PontoAcoes from '@/components/PontoAcoes.vue'
import GeminiPainel from '@/components/GeminiPainel.vue'
import { useNiveis, formatarNivel, formatarDistancia, distanciaM, RISCO } from '@/composables/useNiveis'
import { useFavoritos } from '@/composables/useFavoritos'

const route = useRoute()
const router = useRouter()
const {
  rios, pontos, carregando, erro, demorando, carregar, statusDe, nivelAtual,
  localizacao, gpsStatus, pedirGps, pontosPorDistancia, pontosEmAlerta, ultimaAtualizacao,
} = useNiveis()
const { favs, sincronizar } = useFavoritos()

const CHAVE_ESCOLHIDO = 'ht_meu_ponto'
const escolhidoId = ref(Number(sessionStorage.getItem(CHAVE_ESCOLHIDO)) || null)
const aberto = ref(null)
const filtroCidade = ref('')
const geminiAberto = ref(null)
const modo = ref(route.query.perto === '1' || localizacao.value?.fonte === 'simulada' ? 'perto' : 'todos')

function mudarModo(novo) {
  modo.value = novo
  router.replace({ query: { ...route.query, perto: novo === 'perto' ? '1' : undefined } })
  if (novo === 'perto' && !localizacao.value) pedirGps()
}

function limparEscolha() {
  escolhidoId.value = null
  sessionStorage.removeItem(CHAVE_ESCOLHIDO)
}

/* Prioridade: escolha manual → mais perto (no modo "Perto de mim") → primeiro favorito */
const meuPonto = computed(() => {
  if (escolhidoId.value) {
    const p = pontos.value.find(x => x.id === escolhidoId.value)
    if (p) return p
  }
  if (modo.value === 'perto' && pontosPorDistancia.value.length) return pontosPorDistancia.value[0].ponto
  return pontos.value.find(p => favs.value.has(p.id)) || null
})

const meuRisco = computed(() => { void ultimaAtualizacao.value; return meuPonto.value ? statusDe(meuPonto.value) : null })

const textoOrigem = computed(() => {
  if (!meuPonto.value) return ''
  if (escolhidoId.value === meuPonto.value.id) return 'Escolhido por você'
  if (modo.value === 'perto' && localizacao.value) {
    const d = distanciaDe(meuPonto.value)
    const fonte = localizacao.value.fonte === 'simulada' ? 'Localização simulada' : 'Mais perto de você'
    return d != null ? `${fonte} · ${formatarDistancia(d)}` : fonte
  }
  return 'Seu favorito'
})

const alerta = computed(() => {
  const lista = pontosEmAlerta.value
  if (!lista.length) return null
  return lista.find(p => p.id === meuPonto.value?.id) || lista[0]
})

const cidades = computed(() => [...new Set(rios.value.map(r => r.cidade))].filter(Boolean).sort())

const ORDEM = { alto: 0, medio: 1, baixo: 2 }

/** Todos os rios cadastrados (mesmo sem pontos), cada um com seus pontos e o pior status. */
const grupos = computed(() => {
  void ultimaAtualizacao.value
  const perto = modo.value === 'perto' && !!localizacao.value
  return rios.value
    .filter(r => !filtroCidade.value || r.cidade === filtroCidade.value)
    .map(rio => {
      const lista = pontos.value.filter(p => p.rioId === rio.id)
        .sort((a, b) => perto
          ? (distanciaDe(a) - distanciaDe(b))
          : (ORDEM[statusDe(a).nivel] - ORDEM[statusDe(b).nivel]))
      const pior = lista.reduce((acc, p) => ORDEM[statusDe(p).nivel] < ORDEM[acc.nivel] ? statusDe(p) : acc, RISCO.baixo)
      const distancia = perto && lista.length ? Math.min(...lista.map(distanciaDe)) : null
      return { rio, pontos: lista, pior, distancia }
    })
    .sort((a, b) => perto
      ? ((a.distancia ?? 1e12) - (b.distancia ?? 1e12))
      : (ORDEM[a.pior.nivel] - ORDEM[b.pior.nivel]) || (b.pontos.length > 0) - (a.pontos.length > 0) || a.rio.nome.localeCompare(b.rio.nome, 'pt-BR'))
})

function distanciaDe(p) {
  const loc = localizacao.value
  return loc ? distanciaM(loc.lat, loc.lng, p.latitude, p.longitude) : null
}

const horaAtualizacao = computed(() => ultimaAtualizacao.value
  ? new Date(ultimaAtualizacao.value).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  : '')

const rotaPara = p => ({ path: '/rota-de-fuga', query: { ponto: p.id } })

function escolher(p) {
  geminiAberto.value = null
  escolhidoId.value = p.id
  sessionStorage.setItem(CHAVE_ESCOLHIDO, String(p.id))
  aberto.value = null
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function alternarGemini(rioId) {
  geminiAberto.value = geminiAberto.value === rioId ? null : rioId
}

function recarregar() { carregar() }

// Se a localização mudar (GPS chegou ou simulador moveu o visitante), volta para o ponto mais próximo
watch(() => localizacao.value && `${localizacao.value.lat},${localizacao.value.lng}`, (novo, antigo) => {
  if (novo && antigo !== undefined && modo.value === 'perto') limparEscolha()
  if (novo && localizacao.value.fonte === 'simulada') modo.value = 'perto'
})

onMounted(async () => {
  await carregar()
  sincronizar()
  if (modo.value === 'perto' && !localizacao.value) pedirGps()
  if (route.query.ponto) {
    aberto.value = Number(route.query.ponto)
    await nextTick()
    document.getElementById(`ponto-${route.query.ponto}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }
})
</script>

<style scoped>
.mon { min-height: 100%; background: var(--bg-primary); }
.mon-wrap { max-width: 760px; margin: 0 auto; padding: 20px 16px 40px; display: flex; flex-direction: column; gap: 28px; }

/* Alerta */
.mon-alert {
  position: sticky; top: var(--landing-header-h); z-index: 20;
  display: flex; align-items: center; gap: 12px;
  padding: 12px 16px; background: var(--emergency); color: #fff; text-decoration: none;
  animation: alertIn .3s ease-out;
}
.mon-alert-txt { display: flex; flex-direction: column; flex: 1; min-width: 0; line-height: 1.3; }
.mon-alert-txt strong { font-size: var(--fs-md); }
.mon-alert-txt span { font-size: var(--fs-sm); opacity: .92; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.mon-alert-cta { font-weight: 800; white-space: nowrap; padding: 8px 12px; border-radius: var(--radius-md); background: rgba(255,255,255,.18); }
@keyframes alertIn { from { transform: translateY(-100%); } to { transform: none; } }

/* Cabeçalho + abas */
.mon-head { display: flex; align-items: center; justify-content: space-between; gap: 12px 16px; flex-wrap: wrap; }
.mon-head h1 { font-size: var(--fs-xl); }
.tabs { display: inline-flex; padding: 4px; gap: 4px; border-radius: var(--radius-lg); background: var(--bg-card); border: 1px solid var(--border); }
.tabs button { min-height: 42px; padding: 0 16px; border-radius: var(--radius-md); background: transparent; color: var(--text-secondary); font-size: var(--fs-sm); }
.tabs button:hover:not(:disabled) { transform: none; color: var(--text-primary); }
.tabs button.on { background: var(--accent); color: var(--on-accent); }
@media (max-width: 520px) { .tabs { width: 100%; } .tabs button { flex: 1; } }

/* Rios */
.all-count { font-size: var(--fs-sm); font-weight: 700; color: var(--text-muted); margin-left: 4px; }
.rivers { list-style: none; display: flex; flex-direction: column; gap: 14px; }
.river { border: 1px solid var(--border); border-radius: var(--radius-xl); background: var(--bg-secondary); padding: 14px; display: flex; flex-direction: column; gap: 10px; }
.river--alto { border-color: var(--risk-high); }
.river--medio { border-color: var(--risk-medium-solid); }
.river-head { display: flex; align-items: center; gap: 12px; }
.river-icon { width: 44px; height: 44px; flex-shrink: 0; border-radius: var(--radius-lg); display: grid; place-items: center; background: var(--bg-card); }
.river-info { flex: 1; min-width: 0; }
.river-info h3 { font-size: var(--fs-lg); line-height: 1.25; }
.river-info small { font-size: var(--fs-sm); color: var(--text-muted); }
.river-empty { font-size: var(--fs-sm); color: var(--text-muted); padding: 4px 2px; }

/* Seu rio */
.mine { display: flex; flex-direction: column; gap: 12px; }
.mine-head { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
.mine-head h2 { font-size: var(--fs-lg); }
.mine-where { display: inline-flex; align-items: center; gap: 6px; font-size: var(--fs-sm); color: var(--text-secondary); }
.mine-card {
  display: flex; flex-direction: column; gap: 18px;
  padding: 20px; border-radius: var(--radius-2xl);
  background: var(--bg-card); border: 1px solid var(--border);
}
.mine-card--alto  { border-color: var(--risk-high); box-shadow: 0 0 0 3px var(--risk-high-bg); }
.mine-card--medio { border-color: var(--risk-medium-solid); }
.mine-card--loading, .mine-card--empty { align-items: center; text-align: center; color: var(--text-secondary); padding: 32px 20px; gap: 12px; }
.mine-empty-title { font-size: var(--fs-lg); font-weight: 800; color: var(--text-primary); }
.mine-hint { font-size: var(--fs-sm); color: var(--risk-medium-text); }

.mine-status { display: flex; align-items: center; gap: 14px; padding: 14px; border-radius: var(--radius-xl); }
.mine-card--baixo .mine-status { background: var(--risk-low-bg); color: var(--risk-low-text); }
.mine-card--medio .mine-status { background: var(--risk-medium-bg); color: var(--risk-medium-text); }
.mine-card--alto  .mine-status { background: var(--risk-high-bg); color: var(--risk-high-text); }
.mine-status-icon { width: 54px; height: 54px; flex-shrink: 0; border-radius: 50%; display: grid; place-items: center; background: var(--bg-card); }
.mine-card--alto .mine-status-icon { animation: pulseRing 1.6s ease-out infinite; }
.mine-status-title { font-size: var(--fs-lg); font-weight: 800; line-height: 1.2; }
.mine-status-tag { font-size: var(--fs-xs); font-weight: 700; text-transform: uppercase; letter-spacing: .05em; opacity: .8; white-space: nowrap; }
.mine-status-text { font-size: var(--fs-md); color: var(--text-primary); opacity: .9; line-height: 1.4; }
@keyframes pulseRing { 0% { box-shadow: 0 0 0 0 var(--risk-high-bg); } 100% { box-shadow: 0 0 0 14px transparent; } }

.mine-place h3 { font-size: var(--fs-lg); }
.mine-place p { font-size: var(--fs-sm); color: var(--text-secondary); }
.mine-actions { display: flex; flex-wrap: wrap; gap: 8px; }

/* Lista */
.all { display: flex; flex-direction: column; gap: 12px; }
.all-head { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.all-head h2 { font-size: var(--fs-lg); }
.all-filter { width: auto; min-height: 40px; font-size: var(--fs-sm); }
.all-list { list-style: none; display: flex; flex-direction: column; gap: 8px; }
.row { border: 1px solid var(--border); border-radius: var(--radius-xl); background: var(--bg-card); overflow: hidden; }
.row--open { border-color: var(--border-accent); }
.row-btn {
  width: 100%; min-height: 68px; padding: 12px 14px; border-radius: 0;
  display: flex; align-items: center; gap: 12px; text-align: left;
  background: transparent; color: var(--text-primary); font-weight: 400;
}
.row-btn:hover:not(:disabled) { transform: none; background: var(--bg-card-hover); }
.row-icon { flex-shrink: 0; }
.row-info { display: flex; flex-direction: column; flex: 1; min-width: 0; gap: 2px; }
.row-info strong { font-size: var(--fs-md); font-weight: 700; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.row-info small { font-size: var(--fs-xs); color: var(--text-muted); }
.row-level { display: flex; flex-direction: column; align-items: flex-end; gap: 2px; font-variant-numeric: tabular-nums; }
.row-level b { font-size: var(--fs-md); }
.row-level small { font-size: var(--fs-xs); color: var(--text-muted); }
.row-chev { color: var(--text-muted); transition: transform var(--transition-fast); flex-shrink: 0; }
.row--open .row-chev { transform: rotate(180deg); }
.row-body { padding: 4px 14px 16px; display: flex; flex-direction: column; gap: 14px; border-top: 1px solid var(--border-light); padding-top: 14px; }
.row-actions { display: flex; flex-wrap: wrap; gap: 8px; }

.tone--baixo { color: var(--risk-low-text); }
.tone--medio { color: var(--risk-medium-text); }
.tone--alto  { color: var(--risk-high-text); }

.mon-note { font-size: var(--fs-xs); color: var(--text-muted); text-align: center; }

.spinner { width: 28px; height: 28px; border: 3px solid var(--border-accent); border-top-color: var(--accent); border-radius: 50%; animation: spin .8s linear infinite; }

@media (min-width: 900px) {
  .mon-wrap { padding-top: 32px; }
}
@media (prefers-reduced-motion: reduce) {
  .mon-alert, .mine-card--alto .mine-status-icon, .spinner { animation: none; }
}
</style>
