<template>
  <AuthShell titulo="Criar conta grátis" subtitulo="Leva menos de 1 minuto. Use e-mail ou telefone, o que for mais fácil.">
    <form class="form" novalidate @submit.prevent="handleRegistro">
      <div class="f">
        <label for="reg-nome">Seu nome</label>
        <input id="reg-nome" v-model="form.nome" type="text" placeholder="Como você se chama?" autocomplete="name" />
      </div>
      <div class="f">
        <label for="reg-email">E-mail</label>
        <input id="reg-email" v-model="form.email" type="email" placeholder="seu@email.com" autocomplete="email" />
      </div>
      <div class="f">
        <label for="reg-telefone">Telefone com DDD <small>(para receber alertas pelo WhatsApp)</small></label>
        <input id="reg-telefone" :value="form.telefone" type="tel" inputmode="numeric" placeholder="(19) 99999-9999" autocomplete="tel" @input="onPhoneInput" />
      </div>
      <div class="f">
        <label for="reg-nascimento">Data de nascimento</label>
        <input id="reg-nascimento" :value="form.data_nascimento_display" type="text" inputmode="numeric" placeholder="dd/mm/aaaa" maxlength="10" autocomplete="bday" @input="onDateInput" />
      </div>
      <div class="f">
        <label for="reg-senha">Crie uma senha</label>
        <div class="f-pass">
          <input id="reg-senha" v-model="form.senha" :type="showSenha ? 'text' : 'password'" autocomplete="new-password" aria-describedby="reg-regras" />
          <button type="button" class="f-eye" :aria-label="showSenha ? 'Esconder senha' : 'Mostrar senha'" @click="showSenha = !showSenha">
            <svg v-if="!showSenha" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" /><circle cx="12" cy="12" r="3" /></svg>
            <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94" /><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19" /><line x1="1" y1="1" x2="23" y2="23" /></svg>
          </button>
        </div>
        <ul id="reg-regras" class="rules">
          <li :class="{ ok: form.senha.length >= 8 }">8 ou mais caracteres</li>
          <li :class="{ ok: /[A-Z]/.test(form.senha) }">1 letra maiúscula</li>
          <li :class="{ ok: /[a-z]/.test(form.senha) }">1 letra minúscula</li>
          <li :class="{ ok: /[0-9]/.test(form.senha) }">1 número</li>
        </ul>
      </div>
      <div class="f">
        <label for="reg-confirmar">Repita a senha</label>
        <div class="f-pass">
          <input id="reg-confirmar" v-model="form.confirmarSenha" :type="showConfirmar ? 'text' : 'password'" autocomplete="new-password" />
          <button type="button" class="f-eye" :aria-label="showConfirmar ? 'Esconder senha' : 'Mostrar senha'" @click="showConfirmar = !showConfirmar">
            <svg v-if="!showConfirmar" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" /><circle cx="12" cy="12" r="3" /></svg>
            <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94" /><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19" /><line x1="1" y1="1" x2="23" y2="23" /></svg>
          </button>
        </div>
        <p v-if="form.confirmarSenha && form.confirmarSenha !== form.senha" class="f-msg">As senhas ainda estão diferentes</p>
      </div>

      <p v-if="error" class="form-erro" role="alert">{{ error }}</p>
      <p v-if="success" class="form-ok" role="status">{{ success }}</p>

      <button class="btn btn--primary btn--lg btn--block" type="submit" :disabled="loading">
        {{ loading ? 'Criando sua conta…' : 'Criar conta' }}
      </button>
    </form>

    <template #rodape>
      Já tem conta? <router-link to="/login">Entrar</router-link>
    </template>
  </AuthShell>
</template>

<script setup>
import { ref, computed } from 'vue'
import AuthShell from '@/components/AuthShell.vue'
import { useRouter } from 'vue-router'

import api from '../services/api'

const router = useRouter()
const loading = ref(false)
const error = ref('')
const success = ref('')
const showSenha = ref(false)
const showConfirmar = ref(false)

const form = ref({
  nome: '',
  email: '',
  telefone: '',
  data_nascimento: '',
  data_nascimento_display: '',
  senha: '',
  confirmarSenha: ''
})

const onDateInput = (e) => {
  let digits = e.target.value.replace(/\D/g, '').slice(0, 8)
  let formatted = ''
  if (digits.length > 0) formatted += digits.slice(0, 2)
  if (digits.length > 2) formatted += '/' + digits.slice(2, 4)
  if (digits.length > 4) formatted += '/' + digits.slice(4, 8)
  form.value.data_nascimento_display = formatted
  e.target.value = formatted
  // Convert dd/mm/yyyy to yyyy-mm-dd for API
  if (digits.length === 8) {
    const dd = digits.slice(0, 2)
    const mm = digits.slice(2, 4)
    const yyyy = digits.slice(4, 8)
    form.value.data_nascimento = `${yyyy}-${mm}-${dd}`
  } else {
    form.value.data_nascimento = ''
  }
}

const onPhoneInput = (e) => {
  let digits = e.target.value.replace(/\D/g, '').slice(0, 11)
  let formatted = ''
  if (digits.length > 0) formatted += '(' + digits.slice(0, 2)
  if (digits.length >= 2) formatted += ') '
  if (digits.length > 2) formatted += digits.slice(2, 7)
  if (digits.length > 7) formatted += '-' + digits.slice(7, 11)
  form.value.telefone = formatted
  e.target.value = formatted
}

const pwStrength = computed(() => {
  const s = form.value.senha
  if (!s) return 0
  let score = 0
  if (s.length >= 6) score++
  if (s.length >= 10) score++
  if (/[A-Z]/.test(s)) score++
  if (/[0-9]/.test(s)) score++
  if (/[^A-Za-z0-9]/.test(s)) score++
  return score
})

const pwStrengthPercent = computed(() => (pwStrength.value / 5) * 100)

const pwStrengthClass = computed(() => {
  if (pwStrength.value <= 1) return 'pw-weak'
  if (pwStrength.value <= 3) return 'pw-medium'
  return 'pw-strong'
})

const pwStrengthLabel = computed(() => {
  if (pwStrength.value <= 1) return 'Fraca'
  if (pwStrength.value <= 3) return 'Média'
  return 'Forte'
})

const handleRegistro = async () => {
  error.value = ''
  success.value = ''

  if (!form.value.nome || (!form.value.email && !form.value.telefone) || !form.value.data_nascimento || !form.value.senha) {
    error.value = 'Preencha seu nome, um e-mail ou telefone, a data de nascimento e a senha.'
    return
  }

  if (form.value.senha !== form.value.confirmarSenha) {
    error.value = 'As duas senhas estão diferentes. Digite a mesma senha nos dois campos.'
    return
  }

  loading.value = true

  try {
    const data = {
      nome: form.value.nome,
      senha: form.value.senha,
      data_nascimento: form.value.data_nascimento,
    }
    if (form.value.email) data.email = form.value.email
    if (form.value.telefone) data.telefone = form.value.telefone
    const response = await api.register(data)
    const { access, refresh, usuario } = response.data

    localStorage.setItem('user_token', access)
    localStorage.setItem('refresh_token', refresh)
    localStorage.setItem('user_name', usuario.nome)
    localStorage.setItem('user_data', JSON.stringify(usuario))
    if (usuario.favoritos) localStorage.setItem('ht_favs', JSON.stringify(usuario.favoritos))
    if (usuario.alertas) localStorage.setItem('ht_alerts', JSON.stringify(usuario.alertas))
    localStorage.setItem('ht_show_onboarding', 'true')
    window.dispatchEvent(new Event('storage-update'))
    success.value = 'Conta criada! Entrando…'

    setTimeout(() => {
      router.push('/')
    }, 1500)
  } catch (err) {
    // Traduz os erros do servidor para frases que qualquer pessoa entende
    const NOMES = { nome: 'Nome', email: 'E-mail', telefone: 'Telefone', senha: 'Senha', data_nascimento: 'Data de nascimento' }
    const dados = err.response?.data
    if (dados && typeof dados === 'object') {
      error.value = Object.entries(dados)
        .map(([campo, msg]) => `${NOMES[campo] || (campo === 'non_field_errors' || campo === 'detail' ? '' : campo)}${NOMES[campo] ? ': ' : ''}${Array.isArray(msg) ? msg.join(' ') : msg}`)
        .join(' · ')
    } else {
      error.value = 'Não foi possível criar a conta agora. Verifique a internet e tente de novo.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.rules { list-style: none; display: grid; grid-template-columns: 1fr 1fr; gap: 4px 12px; margin-top: 4px; font-size: var(--fs-xs); color: var(--text-muted); }
.rules li::before { content: '○'; margin-right: 6px; }
.rules li.ok { color: var(--risk-low-text); font-weight: 700; }
.rules li.ok::before { content: '✓'; }
</style>
