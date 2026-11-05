<template>
  <div class="sim">
    <header class="sim-top">
      <div>
        <p class="sim-eyebrow">Uso interno · apresentação</p>
        <h1>Simulador de enchente</h1>
        <p class="sim-help">Deixe esta página numa janela fora do projetor. As telas do site abertas <b>neste mesmo navegador</b> reagem na hora.</p>
      </div>
      <div class="sim-top-actions">
        <a class="btn btn--ghost btn--sm" href="/monitoramento" target="_blank" rel="noopener">Abrir monitoramento</a>
        <a class="btn btn--ghost btn--sm" href="/rota-de-fuga" target="_blank" rel="noopener">Abrir rota de fuga</a>
        <button class="btn btn--ghost btn--sm" type="button" @click="resetar">Zerar simulação</button>
      </div>
    </header>

    <section class="sim-card">
      <h2>Onde está o visitante?</h2>
      <p class="sim-help">Na sala de apresentação o GPS real fica longe dos pontos de risco. Escolha um ponto para o site “achar” que o visitante está ali.</p>
      <div class="sim-local">
        <label class="sim-radio" :class="{ on: !estado.local }">
          <input type="radio" name="local" :checked="!estado.local" @change="definirLocal(null)" />
          <span>GPS real do aparelho</span>
        </label>
        <label v-for="p in pontos" :key="'l' + p.id" class="sim-radio" :class="{ on: estado.local?.pontoId === p.id }">
          <input type="radio" name="local" :checked="estado.local?.pontoId === p.id" @change="definirLocal(p)" />
          <span>Perto de <b>{{ p.descricao }}</b> <small>{{ p.rioNome }} · {{ p.cidade }}</small></span>
        </label>
      </div>
    </section>

    <section class="sim-card">
      <h2>Cenário de cada ponto</h2>
      <p class="sim-help">O nível sobe ou desce aos poucos até a faixa escolhida (atualiza a cada 5 segundos).</p>
      <p v-if="carregando" class="sim-help">Carregando pontos…</p>
      <p v-else-if="erro" class="sim-erro">{{ erro }}</p>
      <ul v-else class="sim-list">
        <li v-for="p in pontos" :key="p.id" class="sim-row">
          <div class="sim-row-info">
            <strong>{{ p.descricao }}</strong>
            <small>{{ p.rioNome }} · {{ p.cidade }}</small>
            <span class="sim-row-now">
              <RiskPill :risco="statusDe(p)" />
              <span class="sim-level">{{ formatarNivel(nivelAtual(p)) }}</span>
            </span>
          </div>
          <div class="sim-seg" role="radiogroup" :aria-label="`Cenário de ${p.descricao}`">
            <button v-for="c in opcoes" :key="c.valor" type="button" role="radio"
              :aria-checked="cenarioDe(p.id) === c.valor"
              :class="['sim-seg-btn', 'sim-seg-btn--' + c.valor, { on: cenarioDe(p.id) === c.valor }]"
              @click="definirCenario(p.id, c.valor)">
              {{ c.rotulo }}
            </button>
          </div>
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import RiskPill from '@/components/RiskPill.vue'
import { useSimulacao } from '@/composables/useSimulacao'
import { useNiveis, formatarNivel } from '@/composables/useNiveis'

const sim = useSimulacao()
const { pontos, carregando, erro, carregar, statusDe, nivelAtual } = useNiveis()

const estado = computed(() => sim.estado.value)
const cenarioDe = sim.cenarioDe
const definirCenario = sim.definirCenario
const definirLocal = sim.definirLocal
const resetar = sim.resetar

const opcoes = [
  { valor: 'normal', rotulo: 'Normal' },
  { valor: 'medio', rotulo: 'Atenção' },
  { valor: 'alto', rotulo: 'Perigo' },
]

onMounted(() => {
  document.title = 'Simulador · HydroTech'
  let meta = document.querySelector('meta[name="robots"]')
  if (!meta) { meta = document.createElement('meta'); meta.name = 'robots'; document.head.appendChild(meta) }
  meta.content = 'noindex'
  carregar()
})
</script>

<style scoped>
.sim { max-width: 860px; margin: 0 auto; padding: 24px 16px 48px; display: flex; flex-direction: column; gap: 16px; }
.sim-top { display: flex; flex-direction: column; gap: 14px; }
.sim-top h1 { font-size: var(--fs-xl); }
.sim-eyebrow { font-size: var(--fs-xs); font-weight: 800; letter-spacing: .1em; text-transform: uppercase; color: var(--risk-medium-text); }
.sim-help { font-size: var(--fs-sm); color: var(--text-secondary); }
.sim-erro { color: var(--risk-high-text); font-size: var(--fs-sm); }
.sim-top-actions { display: flex; flex-wrap: wrap; gap: 8px; }
.sim-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-xl); padding: 18px; display: flex; flex-direction: column; gap: 10px; }
.sim-card h2 { font-size: var(--fs-lg); }
.sim-local { display: flex; flex-direction: column; gap: 6px; }
.sim-radio { display: flex; align-items: center; gap: 10px; min-height: var(--tap); padding: 8px 12px; border: 1px solid var(--border); border-radius: var(--radius-lg); cursor: pointer; font-size: var(--fs-sm); }
.sim-radio.on { border-color: var(--accent); background: var(--accent-soft); }
.sim-radio input { width: 18px; height: 18px; flex-shrink: 0; accent-color: var(--accent); }
.sim-radio small { display: block; color: var(--text-muted); }
.sim-list { list-style: none; display: flex; flex-direction: column; gap: 8px; }
.sim-row { display: flex; align-items: center; justify-content: space-between; gap: 14px; padding: 12px; border: 1px solid var(--border); border-radius: var(--radius-lg); flex-wrap: wrap; }
.sim-row-info { display: flex; flex-direction: column; gap: 4px; min-width: 0; }
.sim-row-info small { color: var(--text-muted); font-size: var(--fs-xs); }
.sim-row-now { display: flex; align-items: center; gap: 10px; }
.sim-level { font-variant-numeric: tabular-nums; font-weight: 700; font-size: var(--fs-sm); }
.sim-seg { display: inline-flex; border: 1px solid var(--border); border-radius: var(--radius-lg); overflow: hidden; }
.sim-seg-btn { min-height: 44px; padding: 0 16px; border-radius: 0; background: transparent; color: var(--text-secondary); font-size: var(--fs-sm); }
.sim-seg-btn:hover:not(:disabled) { transform: none; background: var(--bg-elevated); }
.sim-seg-btn + .sim-seg-btn { border-left: 1px solid var(--border); }
.sim-seg-btn.on.sim-seg-btn--normal { background: var(--risk-low-bg); color: var(--risk-low-text); }
.sim-seg-btn.on.sim-seg-btn--medio { background: var(--risk-medium-bg); color: var(--risk-medium-text); }
.sim-seg-btn.on.sim-seg-btn--alto { background: var(--emergency); color: #fff; }
@media (max-width: 560px) { .sim-seg { width: 100%; } .sim-seg-btn { flex: 1; } }
</style>
