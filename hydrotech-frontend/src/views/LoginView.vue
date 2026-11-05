<template>
  <AuthShell titulo="Entrar" subtitulo="Use o e-mail ou o telefone que você cadastrou.">
    <div class="seg2" role="tablist" aria-label="Entrar com">
      <button type="button" role="tab" :aria-selected="loginMode === 'email'" :class="{ on: loginMode === 'email' }" @click="loginMode = 'email'">E-mail</button>
      <button type="button" role="tab" :aria-selected="loginMode === 'telefone'" :class="{ on: loginMode === 'telefone' }" @click="loginMode = 'telefone'">Telefone</button>
    </div>

    <form class="form" novalidate @submit.prevent="login">
      <div v-if="loginMode === 'email'" class="f" :class="{ 'f--erro': errors.email }">
        <label for="login-email">E-mail</label>
        <input id="login-email" v-model="form.email" type="email" placeholder="seu@email.com" autocomplete="email" :aria-invalid="errors.email" @input="clearError('email')" @blur="validateField('email')" />
        <p v-if="errors.email" class="f-msg">Digite um e-mail válido, por exemplo nome@gmail.com</p>
      </div>
      <div v-else class="f" :class="{ 'f--erro': errors.telefone }">
        <label for="login-phone">Telefone com DDD</label>
        <input id="login-phone" :value="form.telefone" type="tel" inputmode="numeric" placeholder="(19) 99999-9999" autocomplete="tel" :aria-invalid="errors.telefone" @input="onPhoneInput($event, 'telefone')" @focus="clearError('telefone')" @blur="validateField('telefone')" />
        <p v-if="errors.telefone" class="f-msg">Digite o telefone com DDD</p>
      </div>

      <div class="f" :class="{ 'f--erro': errors.senha }">
        <label for="login-password">Senha</label>
        <div class="f-pass">
          <input id="login-password" v-model="form.senha" :type="showSenha ? 'text' : 'password'" autocomplete="current-password" :aria-invalid="errors.senha" @input="clearError('senha')" @blur="validateField('senha')" />
          <button type="button" class="f-eye" :aria-label="showSenha ? 'Esconder senha' : 'Mostrar senha'" @click="showSenha = !showSenha">
            <svg v-if="!showSenha" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" /><circle cx="12" cy="12" r="3" /></svg>
            <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94" /><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19" /><line x1="1" y1="1" x2="23" y2="23" /></svg>
          </button>
        </div>
        <p v-if="errors.senha" class="f-msg">Digite sua senha</p>
      </div>

      <p v-if="error" class="form-erro" role="alert">{{ error }}</p>

      <button class="btn btn--primary btn--lg btn--block" type="submit" :disabled="loading">
        {{ loading ? 'Entrando…' : 'Entrar' }}
      </button>
    </form>

    <template #rodape>
      Ainda não tem conta? <router-link to="/registro">Criar conta grátis</router-link>
    </template>
  </AuthShell>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AuthShell from '@/components/AuthShell.vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const loginMode = ref('email')
const form = ref({ email: '', telefone: '', senha: '' })
const errors = ref({ email: false, telefone: false, senha: false })
const loading = ref(false)
const error = ref('')
const showSenha = ref(false)
const remember = ref(true)

const clearError = (field) => {
  errors.value[field] = false
  if (error.value) error.value = ''
}

const validateField = (field) => {
  if (field === 'email') {
    if (!form.value.email) errors.value.email = true
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) errors.value.email = true
  } else if (field === 'telefone') {
    if (!form.value.telefone) errors.value.telefone = true
    else if (form.value.telefone.replace(/\D/g, '').length < 10) errors.value.telefone = true
  } else if (field === 'senha') {
    if (!form.value.senha) errors.value.senha = true
  }
}

const onPhoneInput = (e, field) => {
  let digits = e.target.value.replace(/\D/g, '').slice(0, 11)
  let formatted = ''
  if (digits.length > 0) formatted += '(' + digits.slice(0, 2)
  if (digits.length >= 2) formatted += ') '
  if (digits.length > 2) formatted += digits.slice(2, 7)
  if (digits.length > 7) formatted += '-' + digits.slice(7, 11)
  form.value[field] = formatted
  e.target.value = formatted
}

const validate = () => {
  let valid = true
  const field = loginMode.value === 'email' ? 'email' : 'telefone'
  validateField(field)
  validateField('senha')
  if (errors.value[field]) valid = false
  if (errors.value.senha) valid = false
  return valid
}

const focusFirstInvalid = () => {
  const field = loginMode.value === 'email' ? 'email' : 'telefone'
  const id = errors.value[field] ? field : errors.value.senha ? 'senha' : null
  if (id) {
    const map = { email: 'email', telefone: 'phone', senha: 'password' }
    const el = document.getElementById(`login-${map[id]}`)
    if (el) setTimeout(() => el.focus(), 100)
  }
}

const login = async () => {
  if (!validate()) { focusFirstInvalid(); return }
  loading.value = true; error.value = ''
  try {
    const payload = { senha: form.value.senha }
    if (loginMode.value === 'email') {
      payload.email = form.value.email
    } else {
      payload.telefone = form.value.telefone
    }
    const response = await api.login(payload)
    const { access, refresh, usuario } = response.data
    localStorage.setItem('user_token', access)
    localStorage.setItem('refresh_token', refresh)
    localStorage.setItem('user_name', usuario.nome)
    localStorage.setItem('user_data', JSON.stringify(usuario))
    if (usuario.favoritos) localStorage.setItem('ht_favs', JSON.stringify(usuario.favoritos))
    if (usuario.alertas) localStorage.setItem('ht_alerts', JSON.stringify(usuario.alertas))
    window.dispatchEvent(new Event('storage-update'))
    router.push(usuario.deve_alterar_senha ? '/minha-conta' : '/')
  } catch (err) {
    error.value = err.response?.data?.detail || 'E-mail, telefone ou senha incorretos. Confira e tente de novo.'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  if (remember.value) {
    const saved = localStorage.getItem('login_email')
    if (saved) form.value.email = saved
  }

})

</script>
