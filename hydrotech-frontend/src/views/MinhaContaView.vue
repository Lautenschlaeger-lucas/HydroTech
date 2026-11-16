<template>
  <div class="conta">
    <header class="conta-head">
      <div class="avatar" aria-hidden="true">{{ initials }}</div>
      <div class="conta-who">
        <h1>Olá, {{ primeiroNome }}</h1>
        <p>{{ userData.is_defesa_civil ? 'Conta da Defesa Civil' : 'Sua conta HydroTech' }}</p>
      </div>
      <router-link v-if="userData.is_defesa_civil" to="/dashboard" class="btn btn--primary btn--sm">Abrir painel</router-link>
    </header>

    <p v-if="avisoSenha" class="aviso" role="status">Este é o seu primeiro acesso. Crie uma senha nova em <b>Meus dados</b> para continuar.</p>

    <div class="tabs" role="tablist" aria-label="Seções da conta">
      <button v-if="!userData.is_defesa_civil" type="button" role="tab" :aria-selected="aba === 'rios'" :class="{ on: aba === 'rios' }" @click="aba = 'rios'">Meus rios</button>
      <button type="button" role="tab" :aria-selected="aba === 'dados'" :class="{ on: aba === 'dados' }" @click="aba = 'dados'">Meus dados</button>
    </div>

    <!-- ═══ MEUS RIOS ═══ -->
    <section v-if="aba === 'rios' && !userData.is_defesa_civil" class="painel" aria-label="Meus rios">
      <p v-if="carregando && !meusPontos.length" class="vazio">Carregando seus rios…</p>

      <div v-else-if="!meusPontos.length" class="vazio">
        <p class="vazio-t">Você ainda não salvou nenhum rio</p>
        <p>Salve os pontos perto da sua casa ou do trabalho para ver tudo aqui e receber alertas.</p>
        <router-link to="/monitoramento?perto=1" class="btn btn--primary btn--lg">Escolher meus rios</router-link>
      </div>

      <ul v-else class="lista">
        <li v-for="p in meusPontos" :key="p.id" class="item" :class="'item--' + statusDe(p).nivel">
          <div class="item-top">
            <RiskIcon :nivel="statusDe(p).nivel" :size="26" :class="'tone--' + statusDe(p).nivel" />
            <div class="item-info">
              <strong>{{ p.descricao }}</strong>
              <small>{{ p.rioNome }} · {{ p.cidade }}</small>
            </div>
            <RiskPill :risco="statusDe(p)" />
          </div>
          <p class="item-nivel">Nível do rio: <b>{{ formatarNivel(nivelAtual(p)) }}</b></p>
          <div class="item-acoes">
            <router-link :to="{ path: '/rota-de-fuga', query: { ponto: p.id } }" class="btn btn--sm" :class="statusDe(p).nivel === 'baixo' ? 'btn--ghost' : 'btn--danger'">Rota de fuga</router-link>
            <router-link :to="{ path: '/monitoramento', query: { ponto: p.id } }" class="btn btn--ghost btn--sm">Ver gráfico</router-link>
            <button type="button" class="btn btn--ghost btn--sm" :class="{ 'is-alert': isAlert(p.id) }" :aria-pressed="isAlert(p.id)" @click="toggleAlert(p.id)">
              {{ isAlert(p.id) ? 'Alertas ligados' : 'Ligar alertas' }}
            </button>
            <button v-if="isFav(p.id)" type="button" class="btn btn--ghost btn--sm remover" @click="toggleFav(p.id)">Remover</button>
          </div>
        </li>
      </ul>
    </section>

    <!-- ═══ MEUS DADOS ═══ -->
    <section v-if="aba === 'dados'" class="painel" aria-label="Meus dados">
      <form class="form" @submit.prevent="handleSave">
        <div class="f"><label for="c-nome">Nome</label><input id="c-nome" v-model="form.nome" type="text" required autocomplete="name" /></div>
        <div class="f"><label for="c-email">E-mail</label><input id="c-email" v-model="form.email" type="email" autocomplete="email" /></div>
        <div class="f"><label for="c-tel">Telefone com DDD</label><input id="c-tel" v-model="form.telefone" type="tel" placeholder="(19) 99999-9999" autocomplete="tel" /></div>
        <div class="f"><label for="c-nasc">Data de nascimento</label><input id="c-nasc" v-model="form.data_nascimento" type="date" required /></div>
        <div class="f">
          <label for="c-senha">Nova senha <small>(deixe em branco para manter a atual)</small></label>
          <input id="c-senha" v-model="form.senha" type="password" autocomplete="new-password" />
        </div>
        <p v-if="errorMsg" class="msg msg--erro" role="alert">{{ errorMsg }}</p>
        <p v-if="successMsg" class="msg msg--ok" role="status">{{ successMsg }}</p>
        <button type="submit" class="btn btn--primary btn--lg" :disabled="loading">{{ loading ? 'Salvando…' : 'Salvar' }}</button>
      </form>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'
import RiskIcon from '@/components/RiskIcon.vue'
import RiskPill from '@/components/RiskPill.vue'
import { useFavoritos } from '@/composables/useFavoritos'
import { useNiveis, formatarNivel } from '@/composables/useNiveis'

const { favs, alerts, isFav, isAlert, toggleFav, toggleAlert, sincronizar } = useFavoritos()
const { pontos, carregando, carregar, statusDe, nivelAtual, ultimaAtualizacao } = useNiveis()

const userData = ref(JSON.parse(localStorage.getItem('user_data') || '{}'))
const aba = ref(userData.value.is_defesa_civil ? 'dados' : 'rios')
const loading = ref(false)
const errorMsg = ref('')
const successMsg = ref('')
const avisoSenha = ref(false)

const form = ref({
  nome: userData.value.nome || '',
  email: userData.value.email || '',
  telefone: userData.value.telefone || '',
  data_nascimento: userData.value.data_nascimento || '',
  senha: '',
})

/** Favoritos + pontos com alerta ligado, com o status ao vivo (os de maior risco primeiro). */
const meusPontos = computed(() => {
  void ultimaAtualizacao.value
  const ordem = { alto: 0, medio: 1, baixo: 2 }
  return pontos.value
    .filter(p => favs.value.has(p.id) || alerts.value.has(p.id))
    .sort((a, b) => ordem[statusDe(a).nivel] - ordem[statusDe(b).nivel])
})

const nome = computed(() => userData.value.nome || 'Usuário')
const primeiroNome = computed(() => nome.value.trim().split(' ')[0])
const initials = computed(() => {
  const partes = nome.value.trim().split(' ')
  return (partes.length >= 2 ? partes[0][0] + partes.at(-1)[0] : partes[0][0] || 'U').toUpperCase()
})

onMounted(async () => {
  carregar()
  try {
    const resMe = await api.me()
    userData.value = resMe.data
    form.value.nome = resMe.data.nome
    form.value.email = resMe.data.email
    form.value.telefone = resMe.data.telefone
    form.value.data_nascimento = resMe.data.data_nascimento
    localStorage.setItem('user_data', JSON.stringify(resMe.data))
    await sincronizar()
    if (resMe.data.deve_alterar_senha) { avisoSenha.value = true; aba.value = 'dados' }
    if (resMe.data.is_defesa_civil) aba.value = 'dados'
  } catch (err) {
    console.error('Erro ao carregar dados:', err)
  }
})

const NOMES = { nome: 'Nome', email: 'E-mail', telefone: 'Telefone', senha: 'Senha', data_nascimento: 'Data de nascimento' }

const handleSave = async () => {
  errorMsg.value = ''
  successMsg.value = ''
  loading.value = true
  try {
    const payload = {
      nome: form.value.nome,
      email: form.value.email,
      telefone: form.value.telefone,
      data_nascimento: form.value.data_nascimento,
    }
    if (form.value.senha) payload.senha = form.value.senha
    const res = await api.updateMe(payload)
    userData.value = res.data
    localStorage.setItem('user_data', JSON.stringify(res.data))
    localStorage.setItem('user_name', res.data.nome)
    window.dispatchEvent(new Event('storage-update'))
    successMsg.value = 'Pronto, seus dados foram salvos.'
    if (form.value.senha) {
      successMsg.value = 'Senha trocada! Entre de novo com a senha nova.'
      setTimeout(() => {
        localStorage.removeItem('user_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
      }, 2000)
    }
  } catch (err) {
    const dados = err.response?.data
    errorMsg.value = dados && typeof dados === 'object'
      ? Object.entries(dados).map(([c, m]) => `${NOMES[c] ? NOMES[c] + ': ' : ''}${Array.isArray(m) ? m.join(' ') : m}`).join(' · ')
      : 'Não foi possível salvar agora. Tente de novo.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.conta { max-width: 720px; margin: 0 auto; padding: 28px 16px 40px; display: flex; flex-direction: column; gap: 20px; }
.conta-head { display: flex; align-items: center; gap: 14px; }
.avatar { width: 56px; height: 56px; flex-shrink: 0; border-radius: 50%; display: grid; place-items: center; background: var(--accent); color: var(--on-accent); font-weight: 800; font-size: var(--fs-lg); }
.conta-who { flex: 1; min-width: 0; }
.conta-who h1 { font-size: var(--fs-xl); }
.conta-who p { color: var(--text-secondary); font-size: var(--fs-sm); }
.aviso { padding: 12px 14px; border-radius: var(--radius-lg); background: var(--risk-medium-bg); color: var(--risk-medium-text); font-size: var(--fs-sm); }

.tabs { display: flex; padding: 4px; gap: 4px; border-radius: var(--radius-lg); background: var(--bg-card); border: 1px solid var(--border); }
.tabs button { flex: 1; min-height: 44px; border-radius: var(--radius-md); background: transparent; color: var(--text-secondary); }
.tabs button:hover:not(:disabled) { transform: none; color: var(--text-primary); }
.tabs button.on { background: var(--accent); color: var(--on-accent); }

.painel { display: flex; flex-direction: column; gap: 12px; }
.vazio { display: flex; flex-direction: column; align-items: center; gap: 10px; padding: 32px 20px; text-align: center; color: var(--text-secondary); border: 1px dashed var(--border); border-radius: var(--radius-xl); }
.vazio-t { font-size: var(--fs-lg); font-weight: 800; color: var(--text-primary); }

.lista { list-style: none; display: flex; flex-direction: column; gap: 10px; }
.item { padding: 16px; border-radius: var(--radius-xl); background: var(--bg-card); border: 1px solid var(--border); display: flex; flex-direction: column; gap: 10px; }
.item--alto { border-color: var(--risk-high); }
.item--medio { border-color: var(--risk-medium-solid); }
.item-top { display: flex; align-items: center; gap: 12px; }
.item-info { flex: 1; min-width: 0; display: flex; flex-direction: column; }
.item-info strong { font-size: var(--fs-md); }
.item-info small { font-size: var(--fs-xs); color: var(--text-muted); }
.item-nivel { font-size: var(--fs-sm); color: var(--text-secondary); }
.item-nivel b { color: var(--text-primary); font-variant-numeric: tabular-nums; }
.item-acoes { display: flex; flex-wrap: wrap; gap: 8px; }
.is-alert { color: var(--accent); border-color: var(--accent); background: var(--accent-soft); }
.remover { color: var(--text-muted); }

.form { display: flex; flex-direction: column; gap: 16px; padding: 20px; border-radius: var(--radius-xl); background: var(--bg-card); border: 1px solid var(--border); }
.f { display: flex; flex-direction: column; gap: 6px; }
.f label { font-size: var(--fs-sm); font-weight: 700; }
.f small { font-weight: 400; color: var(--text-muted); }
.f input { min-height: var(--tap); font-size: var(--fs-md); }
.msg { padding: 12px 14px; border-radius: var(--radius-md); font-size: var(--fs-sm); font-weight: 600; }
.msg--erro { background: var(--risk-high-bg); color: var(--risk-high-text); }
.msg--ok { background: var(--risk-low-bg); color: var(--risk-low-text); }
.tone--baixo { color: var(--risk-low-text); }
.tone--medio { color: var(--risk-medium-text); }
.tone--alto { color: var(--risk-high-text); }
@media (max-width: 480px) { .item-top :deep(.risk-pill) { display: none; } }
</style>
