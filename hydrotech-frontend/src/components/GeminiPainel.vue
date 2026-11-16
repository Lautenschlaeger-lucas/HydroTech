<template>
  <div class="gp" aria-live="polite">
    <div v-if="carregando" class="gp-loading">
      <div class="skeleton" style="height: 14px; width: 40%"></div>
      <div class="skeleton" style="height: 12px; width: 100%"></div>
      <div class="skeleton" style="height: 12px; width: 85%"></div>
    </div>
    <template v-else-if="dados">
      <dl class="gp-facts">
        <div><dt>Comprimento</dt><dd>{{ dados.comprimento }}</dd></div>
        <div><dt>Áreas de maior risco</dt><dd>{{ dados.areas_risco }}</dd></div>
        <div><dt>Foz</dt><dd>{{ dados.foz }}</dd></div>
        <div><dt>Período crítico</dt><dd>{{ dados.periodo_critico }}</dd></div>
      </dl>
      <p class="gp-desc">{{ dados.descricao_historico_enchentes }}</p>
      <p class="gp-src">{{ dados.using_fallback ? 'Texto de demonstração' : 'Gerado por IA (Gemini)' }} · pode conter imprecisões</p>
    </template>
    <p v-else class="gp-desc">Não foi possível carregar as informações deste rio.</p>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import api from '@/services/api'

const props = defineProps({ rioId: { type: Number, required: true } })
const dados = ref(null)
const carregando = ref(false)
const cache = new Map()

async function buscar() {
  if (cache.has(props.rioId)) { dados.value = cache.get(props.rioId); return }
  carregando.value = true
  try {
    const res = await api.getRioDescricaoGemini(props.rioId)
    dados.value = res.data
    cache.set(props.rioId, res.data)
  } catch (e) {
    console.error('Erro ao carregar dados do Gemini:', e)
    dados.value = null
  } finally { carregando.value = false }
}

watch(() => props.rioId, buscar)
onMounted(buscar)
</script>

<style scoped>
.gp { display: flex; flex-direction: column; gap: 12px; padding: 16px; border-radius: var(--radius-lg); background: var(--bg-secondary); border: 1px solid var(--border); }
.gp-loading { display: flex; flex-direction: column; gap: 8px; }
.gp-facts { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; }
.gp-facts dt { font-size: var(--fs-xs); color: var(--text-muted); font-weight: 600; }
.gp-facts dd { font-size: var(--fs-sm); font-weight: 600; }
.gp-desc { font-size: var(--fs-sm); color: var(--text-secondary); line-height: 1.6; }
.gp-src { font-size: var(--fs-xs); color: var(--text-muted); }
</style>
