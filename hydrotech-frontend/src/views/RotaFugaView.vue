<template>
  <div class="escape" :class="{ 'escape--nav': navegando }">
    <div ref="mapElement" class="escape-map" :class="{ 'escape-map--picking': escolhendo }" aria-label="Mapa com áreas de risco e rota de fuga"></div>

    <router-link v-if="!navegando" to="/monitoramento" class="escape-back" aria-label="Voltar para Seu rio">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m15 18-6-6 6-6" /></svg>
      Seu rio
    </router-link>

    <div v-if="escolhendo" class="escape-hint" role="status">Toque no mapa onde você está</div>

    <!-- ═══ Modo navegação ("Ir agora") ═══ -->
    <template v-if="navegando">
      <section ref="navTopEl" class="nav-top" :class="{ 'nav-top--ok': chegou }" aria-live="assertive">
        <template v-if="chegou">
          <span class="nav-step">Você chegou</span>
          <strong class="nav-instr">Você está em um local mais alto</strong>
          <p class="nav-next">Fique aqui e aguarde as orientações da Defesa Civil (199).</p>
        </template>
        <template v-else>
          <span class="nav-step">Passo {{ passoAtual + 1 }} de {{ passos.length }}</span>
          <strong class="nav-instr">{{ passo.instrucao }}</strong>
          <span v-if="passo.distancia_m" class="nav-dist">{{ formatarDistancia(passo.distancia_m) }}</span>
          <p v-if="proximoPasso" class="nav-next">Depois: {{ proximoPasso.instrucao }}</p>
        </template>
      </section>

      <section ref="navBottomEl" class="nav-bottom">
        <p v-if="!chegou" class="nav-remain">
          Faltam <b>{{ formatarDistancia(restanteM) }}</b> · cerca de <b>{{ formatarDuracao(restanteS) }}</b>
        </p>
        <p v-if="!seguindoGps && !chegou" class="nav-hint">Sem GPS em movimento: toque em “Próximo” a cada passo.</p>
        <div v-if="!chegou" class="nav-btns">
          <button class="btn btn--ghost" type="button" :disabled="passoAtual === 0" @click="passoAnterior">‹ Anterior</button>
          <button class="btn btn--primary" type="button" @click="proximo">{{ passoAtual + 1 >= passos.length ? 'Cheguei' : 'Próximo ›' }}</button>
        </div>
        <button class="btn btn--ghost btn--block" type="button" @click="encerrarNavegacao">{{ chegou ? 'Fechar' : 'Encerrar navegação' }}</button>
      </section>
    </template>

    <!-- Cartão único (vira “gaveta” no celular) -->
    <section v-show="!navegando" ref="sheetEl" class="sheet" :class="{ 'sheet--danger': resultado?.rota?.zonas_cruzadas?.length }" aria-live="polite">
      <!-- Calculando -->
      <div v-if="ocupado || carregandoZonas" class="sheet-state">
        <span class="spinner" aria-hidden="true"></span>
        <div>
          <strong>{{ carregandoZonas ? (zonasDemorando ? 'Conectando ao servidor…' : 'Carregando áreas de risco…') : origem ? 'Calculando a rota mais segura…' : 'Buscando sua localização…' }}</strong>
          <small>{{ zonasDemorando && carregandoZonas ? 'Na primeira visita isso pode levar até 1 minuto. Não precisa recarregar.' : 'Isso leva só alguns segundos.' }}</small>
        </div>
      </div>

      <!-- Erro do serviço -->
      <div v-else-if="erroServico || erro" class="sheet-state sheet-state--col">
        <strong class="tone--alto">{{ erroServico || erro }}</strong>
        <button class="btn btn--primary btn--block" type="button" @click="tentarDeNovo">Tentar de novo</button>
      </div>

      <!-- Rota pronta -->
      <template v-else-if="resultado">
        <div class="sheet-head">
          <span class="sheet-dest-icon" aria-hidden="true">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m8 3 4 8 5-5 5 15H2L8 3z" /></svg>
          </span>
          <div class="sheet-dest">
            <small>Vá para um local mais alto</small>
            <strong>{{ resultado.destino.endereco || 'Ponto mais alto próximo' }}</strong>
          </div>
        </div>

        <div v-if="resultado.rota" class="sheet-metrics">
          <span><b>{{ formatarDuracao(resultado.rota.duracao_s) }}</b> {{ modo === 'pe' ? 'a pé' : 'de carro' }}</span>
          <span class="dot" aria-hidden="true">·</span>
          <span><b>{{ formatarDistancia(resultado.rota.distancia_m) }}</b></span>
        </div>
        <p v-else class="sheet-warn">Sem caminho pelas ruas até este ponto. Use o mapa como referência.</p>

        <button v-if="resultado.rota" class="btn btn--danger btn--lg btn--block" type="button" @click="iniciarNavegacao">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3 11 22 2l-9 19-2-8-8-2z" /></svg>
          Ir agora
        </button>

        <p v-if="resultado.rota?.zonas_cruzadas?.length" class="sheet-warn sheet-warn--danger">
          <RiskIcon nivel="alto" :size="16" /> O caminho passa por uma área de risco. Siga com cuidado.
        </p>

        <div class="seg" role="radiogroup" aria-label="Como você vai se deslocar">
          <button type="button" role="radio" :aria-checked="modo === 'pe'" :class="{ on: modo === 'pe' }" @click="trocarModo('pe')">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="13" cy="4" r="2" /><path d="m10 22 2-7-3-3 1-5 4 3 3 1" /><path d="M7 13l2-5" /></svg>
            A pé
          </button>
          <button type="button" role="radio" :aria-checked="modo === 'carro'" :class="{ on: modo === 'carro' }" @click="trocarModo('carro')">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 17h14v-5l-2-5H7l-2 5v5z" /><circle cx="7.5" cy="17.5" r="1.5" /><circle cx="16.5" cy="17.5" r="1.5" /></svg>
            De carro
          </button>
        </div>

        <details v-if="resultado.rota?.passos?.length" class="more">
          <summary>Passo a passo ({{ resultado.rota.passos.length }})</summary>
          <ol class="steps">
            <li v-for="(passo, i) in resultado.rota.passos" :key="i">{{ passo.instrucao }} <span v-if="passo.distancia_m">· {{ formatarDistancia(passo.distancia_m) }}</span></li>
          </ol>
        </details>

        <details class="more">
          <summary>Mais detalhes</summary>
          <div class="more-body">
            <p v-if="resultado.destino.acima_do_risco_m != null">O destino fica cerca de <b>{{ formatarNumero(resultado.destino.acima_do_risco_m) }} m acima</b> do ponto de risco.</p>
            <p v-if="resultado.rota && !resultado.rota.desvia_zonas && !resultado.rota.zonas_cruzadas?.length">O desvio automático das áreas de risco não está ativo neste servidor.</p>
            <p>Os círculos vermelhos são as áreas de risco (raio de {{ raioZona }} m). Partida: {{ textoOrigem }}.</p>
            <ul v-if="resultado.avisos?.length"><li v-for="(aviso, i) in resultado.avisos" :key="i">{{ aviso }}</li></ul>
            <p v-if="resultado.links?.google_maps" class="more-links">
              <a :href="resultado.links.google_maps" target="_blank" rel="noopener noreferrer">Abrir no Google Maps</a>
              <a v-if="modo === 'carro' && resultado.links.waze" :href="resultado.links.waze" target="_blank" rel="noopener noreferrer">Abrir no Waze</a>
              <small>Google Maps e Waze não conhecem as áreas de risco do HydroTech.</small>
            </p>
            <button class="btn btn--ghost btn--sm" type="button" @click="escolherNoMapa">Mudar ponto de partida</button>
          </div>
        </details>
      </template>

      <!-- Fora da área de risco -->
      <div v-else-if="origem && !origemEmRisco" class="sheet-state sheet-state--col">
        <div class="sheet-ok">
          <RiskIcon nivel="baixo" :size="28" />
          <div>
            <strong>Você está fora das áreas de risco</strong>
            <small>Não é preciso sair agora. Acompanhe os alertas.</small>
          </div>
        </div>
        <button v-if="pontoFoco" class="btn btn--primary btn--block" type="button" @click="partirDoPonto">Ver rota saindo de {{ pontoFoco.descricao }}</button>
        <button class="btn btn--ghost btn--block" type="button" @click="escolherNoMapa">Escolher outro ponto no mapa</button>
      </div>

      <!-- Sem localização -->
      <div v-else class="sheet-state sheet-state--col">
        <strong>Onde você está?</strong>
        <small>Precisamos da sua localização para traçar a rota.</small>
        <button class="btn btn--primary btn--lg btn--block" type="button" @click="usarGps">Usar minha localização</button>
        <button class="btn btn--ghost btn--block" type="button" @click="escolherNoMapa">Marcar no mapa</button>
        <small v-if="gpsNegado" class="tone--medio">Não conseguimos sua localização. Marque no mapa ou escolha o ponto mais perto de você:</small>
        <select v-if="zonas.length" class="pick" aria-label="Escolher ponto de partida" @change="partirDe($event.target.value)">
          <option value="">Estou perto de…</option>
          <option v-for="z in zonas" :key="z.id" :value="z.id">{{ z.descricao }} · {{ z.rio }}</option>
        </select>
      </div>

      <p class="sheet-note">Protótipo acadêmico · em emergência real, siga a Defesa Civil (199)</p>
    </section>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import RiskIcon from '@/components/RiskIcon.vue'
import { useNiveis } from '@/composables/useNiveis'
import { useSimulacao } from '@/composables/useSimulacao'

const route = useRoute()
const sim = useSimulacao()
const { carregar: carregarPontos, pontos } = useNiveis()
const serviceUrl = (import.meta.env.VITE_ROTA_API_URL || import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, '')

const alertaId = computed(() => {
  const v = String(route.query.alerta || '')
  return /^\d+(,\d+)*$/.test(v) ? v : ''
})
const pontoFocoId = computed(() => Number(route.query.ponto || route.query.alerta?.split?.(',')[0]) || null)

const mapElement = ref(null)
const sheetEl = ref(null)
const zonas = ref([])
const carregandoZonas = ref(true)
const zonasDemorando = ref(false)
const erroServico = ref('')
const erro = ref('')
const ocupado = ref(false)
const modo = ref(route.query.modo === 'carro' ? 'carro' : 'pe')
const origem = ref(null)
const fonteOrigem = ref('')
const escolhendo = ref(false)
const resultado = ref(null)
const gpsNegado = ref(false)
const raioZona = ref(300)

/* ── Modo navegação ── */
const navegando = ref(false)
const passoAtual = ref(0)
const restanteM = ref(0)
const chegou = ref(false)
const seguindoGps = ref(false)
let idSeguir = null
let travaTela = null
let pontosRotaAtual = []
let camadaPasso = null              // destaque do trecho do passo atual
const navTopEl = ref(null)
const navBottomEl = ref(null)

const passos = computed(() => {
  const lista = resultado.value?.rota?.passos || []
  return lista.length ? lista : [{ instrucao: 'Siga a linha verde até o destino', distancia_m: resultado.value?.rota?.distancia_m || 0 }]
})
const passo = computed(() => passos.value[Math.min(passoAtual.value, passos.value.length - 1)])
const proximoPasso = computed(() => passos.value[passoAtual.value + 1] || null)
const restanteS = computed(() => {
  const r = resultado.value?.rota
  if (!r?.distancia_m) return 0
  return r.duracao_s * (restanteM.value / r.distancia_m)
})

let map, camadaBase, camadaZonas, camadaRota, marcadorOrigem, marcadorDestino
let controlador, poller, descartado = false, idGps = 0, idZonas = 0

const valido = (lat, lng) => Number.isFinite(lat) && Number.isFinite(lng) && Math.abs(lat) <= 90 && Math.abs(lng) <= 180
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim()

const pontoFoco = computed(() => {
  const id = pontoFocoId.value
  if (!id) return null
  const z = zonas.value.find(x => x.id === id)
  if (z) return { id, descricao: z.descricao, lat: Number(z.lat), lng: Number(z.lng) }
  const p = pontos.value.find(x => x.id === id)
  return p ? { id, descricao: p.descricao, lat: p.latitude, lng: p.longitude } : null
})

const origemEmRisco = computed(() => origem.value && zonas.value.some(z => {
  const lat = Number(z.lat), lng = Number(z.lng)
  return valido(lat, lng) && L.latLng(origem.value.lat, origem.value.lng).distanceTo([lat, lng]) <= (Number(z.raio_m) || 300)
}))

const textoOrigem = computed(() => ({ gps: 'sua localização (GPS)', simulada: 'localização simulada', mapa: 'ponto marcado no mapa', ponto: 'ponto de monitoramento escolhido', url: 'link recebido' }[fonteOrigem.value] || 'não definida'))

const formatarNumero = v => Number(v).toLocaleString('pt-BR', { maximumFractionDigits: 1 })
const formatarDistancia = m => m >= 1000 ? `${formatarNumero(m / 1000)} km` : `${Math.round(m)} m`
const formatarDuracao = s => s >= 3600 ? `${formatarNumero(s / 3600)} h` : `${Math.max(1, Math.round(s / 60))} min`

/* ── Mapa ── */
function tiles() {
  // OpenStreetMap padrão (sem chave). No tema escuro o CSS escurece os blocos do mapa.
  if (camadaBase) return
  camadaBase = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map)
}

function desenharZonas() {
  if (!map) return
  camadaZonas.clearLayers()
  const vermelho = css('--risk-high') || '#DC2626'
  const limites = []
  for (const z of zonas.value) {
    const lat = Number(z.lat), lng = Number(z.lng)
    if (!valido(lat, lng)) continue
    const foco = z.id === pontoFocoId.value
    L.circle([lat, lng], {
      radius: Number(z.raio_m) || 300, color: vermelho, weight: foco ? 3 : 1.5,
      fillColor: vermelho, fillOpacity: foco ? 0.28 : 0.16, bubblingMouseEvents: false,
    }).bindTooltip(`${z.descricao || 'Área de risco'} · ${z.rio || ''}`, { sticky: true })
      .on('click', e => definirOrigem(e.latlng.lat, e.latlng.lng, 'mapa'))
      .addTo(camadaZonas)
    limites.push([lat, lng])
  }
  if (!origem.value) {
    if (pontoFoco.value) map.setView([pontoFoco.value.lat, pontoFoco.value.lng], 15)
    else if (limites.length) map.fitBounds(limites, { padding: [40, 40], maxZoom: 14 })
  }
}

function limparRota() {
  resultado.value = null
  camadaRota?.clearLayers()
  marcadorDestino?.remove(); marcadorDestino = null
}

function definirOrigem(lat, lng, fonte) {
  if (descartado || !valido(lat, lng)) return
  idGps++
  controlador?.abort(); controlador = null
  ocupado.value = false
  erro.value = ''
  origem.value = { lat, lng }
  fonteOrigem.value = fonte
  escolhendo.value = false
  limparRota()
  const azul = css('--accent') || '#3B82F6'
  if (marcadorOrigem) marcadorOrigem.setLatLng([lat, lng])
  else marcadorOrigem = L.circleMarker([lat, lng], { radius: 9, color: '#fff', weight: 3, fillColor: azul, fillOpacity: 1, interactive: false }).addTo(map)
  map.setView([lat, lng], Math.max(map.getZoom(), 15))
  if (!carregandoZonas.value) calcular()
}

function mostrarRota(dados) {
  limparRota()
  resultado.value = dados
  const pontosRota = [[origem.value.lat, origem.value.lng]]
  const d = dados.destino
  if (d && valido(Number(d.lat), Number(d.lng))) {
    const p = [Number(d.lat), Number(d.lng)]
    marcadorDestino = L.marker(p, {
      interactive: false,
      icon: L.divIcon({ className: 'dest-pin', html: '<span></span>', iconSize: [28, 28], iconAnchor: [14, 14] }),
    }).addTo(map)
    pontosRota.push(p)
  }
  const g = dados.rota?.geometria
  if (g?.type === 'LineString' && g.coordinates?.length > 1) {
    const cor = dados.rota.zonas_cruzadas?.length ? (css('--risk-medium-solid') || '#F59E0B') : (css('--risk-low') || '#10B981')
    L.geoJSON(g, { interactive: false, style: { color: '#000', weight: 10, opacity: 0.25 } }).addTo(camadaRota)
    L.geoJSON(g, { interactive: false, style: { color: cor, weight: 6, opacity: 1 } }).addTo(camadaRota)
    g.coordinates.forEach(c => valido(+c[1], +c[0]) && pontosRota.push([+c[1], +c[0]]))
  }
  pontosRotaAtual = pontosRota
  if (pontosRota.length > 1) {
    nextTick(() => {
      const celular = window.innerWidth < 760
      const gaveta = sheetEl.value?.offsetHeight || 0
      map?.fitBounds(pontosRota, {
        paddingTopLeft: [celular ? 30 : 420, 80],
        paddingBottomRight: [40, celular ? gaveta + 24 : 40],
        maxZoom: 17,
        animate: false,
      })
    })
  }
}

const trecho = (a, b) => L.latLng(a[1], a[0]).distanceTo([b[1], b[0]])

/**
 * Quanto falta, em metros da rota, a partir da posição atual.
 * Usa a PROPORÇÃO do desenho que falta percorrer, porque o comprimento da linha
 * no mapa e a distância informada pelo serviço de rotas nunca batem exatamente.
 */
function distanciaRestante(lat, lng) {
  const coords = resultado.value?.rota?.geometria?.coordinates
  const total = resultado.value?.rota?.distancia_m || 0
  if (!coords?.length || coords.length < 2) return restanteM.value
  let melhor = 0, menor = Infinity
  coords.forEach((c, i) => { const d = L.latLng(lat, lng).distanceTo([c[1], c[0]]); if (d < menor) { menor = d; melhor = i } })
  let comprimento = 0, falta = 0
  for (let i = 0; i < coords.length - 1; i++) {
    const t = trecho(coords[i], coords[i + 1])
    comprimento += t
    if (i >= melhor) falta += t
  }
  if (!comprimento) return restanteM.value
  return Math.min(total, total * (falta / comprimento) + (melhor === coords.length - 1 ? menor : 0))
}

/** Converte "quanto já andei" no passo atual, usando a distância de cada passo. */
function atualizarPassoPorDistancia() {
  const totalRota = resultado.value?.rota?.distancia_m || 0
  const andado = Math.max(0, totalRota - restanteM.value)
  let acumulado = 0
  let indice = passos.value.length - 1
  for (let i = 0; i < passos.value.length; i++) {
    acumulado += passos.value[i].distancia_m || 0
    if (andado < acumulado) { indice = i; break }
  }
  // O GPS só avança; nunca desfaz um passo que a pessoa já marcou como feito
  passoAtual.value = Math.max(passoAtual.value, indice)
}

/* ── Câmera que acompanha o passo ──
 * Os passos só trazem "instrução + distância". Somando as distâncias, sabemos
 * em que fração da rota cada passo começa e termina; com essa fração achamos o
 * trecho correspondente na linha desenhada no mapa.
 */
function linhaDaRota() {
  const coords = resultado.value?.rota?.geometria?.coordinates || []
  const pts = coords.filter(c => valido(+c[1], +c[0])).map(c => L.latLng(+c[1], +c[0]))
  const acumulado = [0]
  for (let i = 1; i < pts.length; i++) acumulado.push(acumulado[i - 1] + pts[i - 1].distanceTo(pts[i]))
  return { pts, acumulado, total: acumulado.at(-1) || 0 }
}

function pontoNaFracao(linha, f) {
  const alvo = Math.max(0, Math.min(1, f)) * linha.total
  for (let i = 1; i < linha.pts.length; i++) {
    if (linha.acumulado[i] >= alvo) {
      const t = (alvo - linha.acumulado[i - 1]) / ((linha.acumulado[i] - linha.acumulado[i - 1]) || 1)
      const a = linha.pts[i - 1], b = linha.pts[i]
      return { latlng: L.latLng(a.lat + (b.lat - a.lat) * t, a.lng + (b.lng - a.lng) * t), indice: i }
    }
  }
  return { latlng: linha.pts.at(-1), indice: linha.pts.length - 1 }
}

/** Trecho da linha (lista de pontos) que corresponde ao passo i. */
function trechoDoPasso(i) {
  const linha = linhaDaRota()
  if (linha.pts.length < 2) return []
  const dist = passos.value.map(p => p.distancia_m || 0)
  const soma = dist.reduce((x, y) => x + y, 0) || 1
  const inicio = dist.slice(0, i).reduce((x, y) => x + y, 0) / soma
  const fim = inicio + dist[i] / soma
  const a = pontoNaFracao(linha, inicio), b = pontoNaFracao(linha, fim)
  return [a.latlng, ...linha.pts.slice(a.indice, b.indice), b.latlng]
}

/** Move a câmera e o marcador para o passo atual, entre o cartão do topo e o painel de baixo. */
function focarPasso(animar = true) {
  if (!map || !navegando.value) return
  const trecho = chegou.value ? [] : trechoDoPasso(passoAtual.value)
  camadaPasso?.remove()
  camadaPasso = null
  const topo = (navTopEl.value?.offsetHeight || 0) + 28
  const baixo = (navBottomEl.value?.offsetHeight || 0) + 28
  const opcoes = { paddingTopLeft: [40, topo], paddingBottomRight: [40, baixo], maxZoom: 18, animate: animar, duration: 0.8 }
  if (trecho.length >= 2) {
    // Trecho do passo atual: contorno branco + azul, por cima da linha verde da rota
    camadaPasso = L.layerGroup([
      L.polyline(trecho, { color: '#ffffff', weight: 11, opacity: 0.95, interactive: false }),
      L.polyline(trecho, { color: css('--accent') || '#3B82F6', weight: 6, opacity: 1, interactive: false }),
    ]).addTo(map)
    if (!seguindoGps.value) marcadorOrigem?.setLatLng(trecho[0])
    map.flyToBounds(L.latLngBounds(trecho), opcoes)
  } else if (chegou.value && resultado.value?.destino) {
    const d = [Number(resultado.value.destino.lat), Number(resultado.value.destino.lng)]
    if (!seguindoGps.value) marcadorOrigem?.setLatLng(d)
    map.flyTo(d, 17, { animate: animar, duration: 0.8 })
  }
}

watch([passoAtual, chegou], () => { if (navegando.value) nextTick(() => focarPasso()) })

async function iniciarNavegacao() {
  if (!resultado.value?.rota) return
  navegando.value = true
  chegou.value = false
  passoAtual.value = 0
  restanteM.value = resultado.value.rota.distancia_m
  await nextTick()
  focarPasso(false)
  try { travaTela = await navigator.wakeLock?.request('screen') } catch { /* sem suporte */ }
  // Só segue o GPS quando a partida veio do GPS real (na simulação o visitante não anda)
  if (fonteOrigem.value === 'gps' && navigator.geolocation) {
    seguindoGps.value = true
    idSeguir = navigator.geolocation.watchPosition(pos => {
      if (!navegando.value) return
      const { latitude: lat, longitude: lng } = pos.coords
      marcadorOrigem?.setLatLng([lat, lng])
      if (map && !map.getBounds().pad(-0.2).contains([lat, lng])) map.panTo([lat, lng])
      restanteM.value = Math.min(restanteM.value, distanciaRestante(lat, lng))
      if (restanteM.value < 30) chegou.value = true
      else atualizarPassoPorDistancia()
    }, () => { seguindoGps.value = false }, { enableHighAccuracy: true, maximumAge: 5000 })
  }
}

function proximo() {
  if (passoAtual.value + 1 >= passos.value.length) { chegou.value = true; restanteM.value = 0; return }
  restanteM.value = Math.max(0, restanteM.value - (passo.value.distancia_m || 0))
  passoAtual.value++
}

function passoAnterior() {
  if (passoAtual.value === 0) return
  passoAtual.value--
  restanteM.value = Math.min(resultado.value.rota.distancia_m, restanteM.value + (passo.value.distancia_m || 0))
}

function encerrarNavegacao() {
  camadaPasso?.remove()
  camadaPasso = null
  navegando.value = false
  seguindoGps.value = false
  if (idSeguir != null) navigator.geolocation.clearWatch(idSeguir)
  idSeguir = null
  travaTela?.release?.().catch(() => {})
  travaTela = null
  if (origem.value) marcadorOrigem?.setLatLng([origem.value.lat, origem.value.lng])
  nextTick(() => {
    const celular = window.innerWidth < 760
    const gaveta = sheetEl.value?.offsetHeight || 0
    if (pontosRotaAtual.length > 1) map?.fitBounds(pontosRotaAtual, { paddingTopLeft: [celular ? 30 : 420, 80], paddingBottomRight: [40, celular ? gaveta + 24 : 40], maxZoom: 17, animate: false })
  })
}

async function calcular() {
  if (!origem.value || !zonas.value.length) return
  if (!origemEmRisco.value) { limparRota(); return }
  controlador?.abort()
  const c = new AbortController()
  controlador = c
  ocupado.value = true
  erro.value = ''
  limparRota()
  const params = new URLSearchParams({ lat: origem.value.lat, lng: origem.value.lng, modo: modo.value })
  if (alertaId.value) params.set('alerta', alertaId.value)
  try {
    const r = await fetch(`${serviceUrl}/rota-fuga?${params}`, { signal: c.signal })
    let dados
    try { dados = await r.json() } catch { throw new Error('O serviço de rotas respondeu de forma inesperada.') }
    if (c.signal.aborted || descartado) return
    if (!r.ok) throw new Error(typeof dados.detail === 'string' ? dados.detail : 'Não foi possível calcular a rota.')
    if (!dados.destino) throw new Error('Não encontramos um destino seguro por perto.')
    mostrarRota(dados)
  } catch (e) {
    if (!descartado && e.name !== 'AbortError') erro.value = e instanceof TypeError ? 'Sem conexão com o servidor de rotas.' : e.message
  } finally {
    if (controlador === c) { controlador = null; ocupado.value = false }
  }
}

const espera = ms => new Promise(r => setTimeout(r, ms))

/** insistir = continua tentando por ~90 s (servidor gratuito pode estar “acordando”). */
async function carregarZonas(forcar = false, insistir = false, tentativa = 0) {
  const id = ++idZonas
  const avisoLento = setTimeout(() => { if (carregandoZonas.value) zonasDemorando.value = true }, 4000)
  try {
    const r = await fetch(`${serviceUrl}/zonas-risco${forcar ? '?atualizar=1' : ''}`)
    if (!r.ok) throw new Error(`Não foi possível carregar as áreas de risco (erro ${r.status}).`)
    const dados = await r.json()
    if (!Array.isArray(dados)) throw new Error('Resposta inválida do serviço de rotas.')
    if (descartado || id !== idZonas) return
    if (JSON.stringify(dados) !== JSON.stringify(zonas.value)) {
      const tinhaRota = !!resultado.value
      zonas.value = dados
      raioZona.value = Number(dados[0]?.raio_m) || 300
      desenharZonas()
      if (tinhaRota) calcular()
    }
    erroServico.value = ''
  } catch (e) {
    if (descartado || id !== idZonas) return
    if (insistir && !zonas.value.length && tentativa < 17) {
      zonasDemorando.value = true
      clearTimeout(avisoLento)
      await espera(5000)
      if (!descartado) return carregarZonas(forcar, true, tentativa + 1)
      return
    }
    erroServico.value = e instanceof TypeError ? 'Não foi possível conectar ao servidor. Verifique sua internet e tente de novo.' : e.message
  } finally {
    clearTimeout(avisoLento)
  }
  if (!descartado && id === idZonas) { carregandoZonas.value = false; zonasDemorando.value = false }
}

/* ── Ações ── */
function usarGps() {
  if (!navigator.geolocation) { gpsNegado.value = true; return Promise.resolve(false) }
  const id = ++idGps
  ocupado.value = true
  return new Promise(resolve => {
    setTimeout(() => {
      if (descartado || id !== idGps || !ocupado.value || origem.value) return
      idGps++
      ocupado.value = false
      gpsNegado.value = true
      resolve(false)
    }, 15000)
    navigator.geolocation.getCurrentPosition(
      pos => {
        if (descartado || id !== idGps) return resolve(false)
        ocupado.value = false
        definirOrigem(pos.coords.latitude, pos.coords.longitude, 'gps')
        resolve(true)
      },
      () => {
        if (descartado || id !== idGps) return resolve(false)
        ocupado.value = false
        gpsNegado.value = true
        resolve(false)
      },
      { enableHighAccuracy: true, timeout: 12000, maximumAge: 30000 },
    )
  })
}

function partirDe(id) {
  const z = zonas.value.find(x => String(x.id) === String(id))
  if (z) definirOrigem(Number(z.lat) + 0.0008, Number(z.lng) + 0.0008, 'ponto')
}

function partirDoPonto() {
  const p = pontoFoco.value
  if (p) definirOrigem(p.lat + 0.0008, p.lng + 0.0008, 'ponto')
}

function escolherNoMapa() {
  escolhendo.value = true
  limparRota()
}

function trocarModo(m) {
  if (modo.value === m) return
  modo.value = m
  calcular()
}

function tentarDeNovo() {
  erro.value = ''
  if (erroServico.value) { erroServico.value = ''; carregandoZonas.value = true; carregarZonas(true, true).then(() => calcular()) }
  else calcular()
}

/** Ordem: link com lat/lng → localização simulada → GPS → ponto escolhido. */
async function definirOrigemInicial() {
  const lat = Number(route.query.lat), lng = Number(route.query.lng)
  if (route.query.lat != null && valido(lat, lng)) return definirOrigem(lat, lng, 'url')
  const local = sim.estado.value.local
  if (local) return definirOrigem(local.lat, local.lng, 'simulada')
  const fLat = Number(route.query.foco_lat), fLng = Number(route.query.foco_lng)
  if (route.query.auto === '1' && valido(fLat, fLng)) return definirOrigem(fLat + 0.0008, fLng + 0.0008, 'ponto')
  const ok = await usarGps()
  if (!ok && pontoFoco.value) partirDoPonto()
}

// O simulador pode mover o “visitante” ao vivo durante a apresentação
watch(() => sim.estado.value.local, local => {
  if (local && !navegando.value) definirOrigem(local.lat, local.lng, 'simulada')
})

onMounted(async () => {
  await nextTick()
  map = L.map(mapElement.value, { zoomControl: false }).setView([-22.357, -47.384], 13)
  L.control.zoom({ position: 'topright' }).addTo(map)
  tiles()
  camadaZonas = L.layerGroup().addTo(map)
  camadaRota = L.layerGroup().addTo(map)
  map.on('click', e => { if (!navegando.value && (escolhendo.value || !resultado.value)) definirOrigem(e.latlng.lat, e.latlng.lng, 'mapa') })

  carregarPontos()
  const zonasProntas = carregarZonas(true, true)
  const origemPronta = definirOrigemInicial()
  await zonasProntas
  await origemPronta
  if (!descartado && origem.value && !resultado.value && !ocupado.value) calcular()
  poller = setInterval(() => carregarZonas(), 60000)
})

onUnmounted(() => {
  if (navegando.value) encerrarNavegacao()
  descartado = true
  controlador?.abort()
  clearInterval(poller)
  map?.remove()
  map = null
})
</script>

<style scoped>
.escape {
  position: relative;
  height: calc(100dvh - var(--landing-header-h));
  min-height: 520px;
  overflow: hidden;
  background: var(--bg-primary);
}
.escape-map { position: absolute; inset: 0; background: var(--bg-tertiary); }
.escape-map--picking { cursor: crosshair; }

.escape-back {
  position: absolute; z-index: 600; top: 14px; left: 14px;
  display: inline-flex; align-items: center; gap: 4px;
  min-height: 44px; padding: 0 14px 0 10px;
  border-radius: var(--radius-full);
  background: var(--bg-card); color: var(--text-primary);
  border: 1px solid var(--border); box-shadow: var(--shadow-md);
  font-weight: 700; font-size: var(--fs-sm); text-decoration: none;
}
.escape-hint {
  position: absolute; z-index: 600; top: 70px; left: 50%; transform: translateX(-50%);
  padding: 10px 16px; border-radius: var(--radius-full);
  background: var(--accent); color: #fff; font-weight: 700; font-size: var(--fs-sm);
  box-shadow: var(--shadow-lg); pointer-events: none; white-space: nowrap;
}

/* Cartão */
.sheet {
  position: absolute; z-index: 700;
  left: 14px; top: 72px; width: 380px; max-height: calc(100% - 86px); overflow-y: auto;
  display: flex; flex-direction: column; gap: 14px;
  padding: 18px; border-radius: var(--radius-2xl);
  background: var(--bg-card); border: 1px solid var(--border); box-shadow: var(--shadow-xl);
}
.sheet--danger { border-color: var(--risk-medium-solid); }
.sheet-state { display: flex; align-items: center; gap: 14px; }
.sheet-state--col { flex-direction: column; align-items: stretch; gap: 10px; text-align: left; }
.sheet-state strong { font-size: var(--fs-md); display: block; }
.sheet-state small { color: var(--text-secondary); font-size: var(--fs-sm); display: block; }
.sheet-ok { display: flex; align-items: center; gap: 12px; padding: 12px; border-radius: var(--radius-lg); background: var(--risk-low-bg); color: var(--risk-low-text); }
.sheet-ok small { color: var(--text-secondary); }

.sheet-head { display: flex; align-items: center; gap: 12px; }
.sheet-dest-icon { width: 44px; height: 44px; border-radius: 50%; flex-shrink: 0; display: grid; place-items: center; background: var(--risk-low-bg); color: var(--risk-low-text); }
.sheet-dest { display: flex; flex-direction: column; min-width: 0; }
.sheet-dest small { font-size: var(--fs-xs); color: var(--text-muted); font-weight: 700; text-transform: uppercase; letter-spacing: .05em; }
.sheet-dest strong { font-size: var(--fs-lg); line-height: 1.25; }
.sheet-metrics { display: flex; align-items: baseline; gap: 8px; font-size: var(--fs-md); color: var(--text-secondary); }
.sheet-metrics b { font-size: var(--fs-xl); color: var(--text-primary); font-weight: 800; margin-right: 2px; }
.sheet-metrics .dot { color: var(--text-dim); }
.sheet-warn { font-size: var(--fs-sm); color: var(--risk-medium-text); display: flex; align-items: center; gap: 6px; }
.sheet-warn--danger { color: var(--risk-high-text); font-weight: 700; }

.seg { display: grid; grid-template-columns: 1fr 1fr; border: 1px solid var(--border); border-radius: var(--radius-lg); overflow: hidden; }
.seg button { min-height: var(--tap); border-radius: 0; background: transparent; color: var(--text-secondary); font-size: var(--fs-sm); }
.seg button:hover:not(:disabled) { transform: none; background: var(--bg-elevated); }
.seg button + button { border-left: 1px solid var(--border); }
.seg button.on { background: var(--accent-soft); color: var(--accent); }

.more { border-top: 1px solid var(--border-light); padding-top: 10px; font-size: var(--fs-sm); }
.more summary { cursor: pointer; font-weight: 700; min-height: 32px; display: flex; align-items: center; color: var(--text-secondary); }
.more[open] summary { color: var(--text-primary); }
.more-body { display: flex; flex-direction: column; gap: 8px; padding-top: 6px; color: var(--text-secondary); line-height: 1.5; }
.more-body ul { padding-left: 18px; }
.more-links { display: flex; flex-wrap: wrap; gap: 6px 14px; }
.more-links a { color: var(--accent); font-weight: 600; }
.more-links small { width: 100%; color: var(--text-muted); }
.steps { padding: 6px 0 0 20px; display: flex; flex-direction: column; gap: 6px; color: var(--text-primary); }
.steps span { color: var(--text-muted); }

.sheet-note { font-size: var(--fs-xs); color: var(--text-muted); }

/* Navegação */
.nav-top, .nav-bottom {
  position: absolute; z-index: 800; left: 14px; right: 14px;
  display: flex; flex-direction: column; gap: 6px;
  padding: 18px; border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-xl);
}
.nav-top { top: 14px; background: var(--accent); color: #fff; }
/* No modo navegação o cartão do passo ocupa o topo: esconde o zoom e as dicas do mapa */
.escape--nav :deep(.leaflet-control-zoom), .escape--nav :deep(.leaflet-tooltip) { display: none; }
.nav-top--ok { background: var(--risk-low); }
.nav-step { font-size: var(--fs-sm); font-weight: 700; opacity: .85; text-transform: uppercase; letter-spacing: .05em; }
.nav-instr { font-size: var(--fs-xl); line-height: 1.2; font-weight: 800; }
.nav-dist { font-size: var(--fs-lg); font-weight: 700; }
.nav-next { font-size: var(--fs-sm); opacity: .9; }
.nav-bottom { bottom: calc(14px + env(safe-area-inset-bottom)); background: var(--bg-card); border: 1px solid var(--border); gap: 10px; }
.nav-remain { font-size: var(--fs-md); color: var(--text-secondary); }
.nav-remain b { color: var(--text-primary); }
.nav-hint { font-size: var(--fs-xs); color: var(--text-muted); }
.nav-btns { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.nav-btns .btn { min-height: 56px; font-size: var(--fs-lg); }
@media (min-width: 760px) {
  .nav-top, .nav-bottom { left: 50%; right: auto; width: 460px; transform: translateX(-50%); }
}
.tone--alto { color: var(--risk-high-text); }
.tone--medio { color: var(--risk-medium-text); }
.spinner { width: 26px; height: 26px; flex-shrink: 0; border: 3px solid var(--border-accent); border-top-color: var(--accent); border-radius: 50%; animation: spin .8s linear infinite; }

:deep(.dest-pin span) {
  display: block; width: 28px; height: 28px; border-radius: 50%;
  background: var(--risk-low); border: 4px solid #fff; box-shadow: 0 2px 10px rgba(0,0,0,.4);
}
:deep(.leaflet-control-attribution) { font-size: 10px; }
.pick { min-height: var(--tap); }
/* Mapa escuro sem chave de API: inverte as cores dos blocos do OpenStreetMap */
:global([data-theme='dark'] .escape .leaflet-tile-pane) { filter: invert(1) hue-rotate(180deg) brightness(.9) contrast(.9) saturate(.6); }

/* Celular: cartão vira gaveta inferior */
@media (max-width: 759px) {
  .escape { height: calc(100dvh - var(--landing-header-h)); }
  .sheet {
    left: 0; right: 0; top: auto; bottom: 0; width: auto;
    max-height: 55%;
    gap: 10px;
    border-radius: var(--radius-2xl) var(--radius-2xl) 0 0;
    border-bottom: 0;
    padding: 12px 16px calc(16px + env(safe-area-inset-bottom));
  }
  .sheet-dest-icon { width: 36px; height: 36px; }
  .sheet-dest strong { font-size: var(--fs-md); }
  .sheet-metrics b { font-size: var(--fs-lg); }
  .more { padding-top: 4px; }
  .sheet::before { content: ''; align-self: center; width: 40px; height: 4px; border-radius: 4px; background: var(--border); flex-shrink: 0; }
}
@media (prefers-reduced-motion: reduce) { .spinner { animation: none; } }
</style>
