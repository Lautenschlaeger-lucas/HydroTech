<template>
  <div class="login-page">
    <div class="bg-orbs">
      <div class="orb orb--1"></div>
      <div class="orb orb--2"></div>
      <div class="orb orb--3"></div>
      <div class="orb orb--4"></div>
    </div>

    <div class="login-container">
      <div class="login-card">
        <div class="card-brand">
          <div class="brand-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
              <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>
            </svg>
          </div>
          <div class="brand-text">
            <span class="brand-name">HydroTech</span>
            <span class="brand-sub">Monitoramento Hidrológico</span>
          </div>
        </div>

        <div class="card-divider"></div>

        <div class="card-header">
          <h1>Acessar Sistema</h1>
          <p>Insira suas credenciais para continuar</p>
        </div>

        <div class="login-mode-toggle">
          <button :class="{ active: loginMode === 'email' }" @click="loginMode = 'email'" type="button">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
            E-mail
          </button>
          <button :class="{ active: loginMode === 'telefone' }" @click="loginMode = 'telefone'" type="button">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            Telefone
          </button>
        </div>

        <form @submit.prevent="login" class="login-form" novalidate>
          <Transition name="field-fade" mode="out-in">
            <div v-if="loginMode === 'email'" key="email" class="field-group">
              <div class="field-wrapper" :class="{ filled: form.email, error: errors.email }">
                <input id="login-email" v-model="form.email" type="email" placeholder=" " autocomplete="email" :aria-invalid="errors.email" @input="clearError('email')" @blur="validateField('email')" />
                <label for="login-email">E-mail</label>
                <div class="field-focus-ring"></div>
              </div>
              <p v-if="errors.email" class="field-error">Informe um e-mail válido</p>
            </div>
            <div v-else key="phone" class="field-group">
              <div class="field-wrapper" :class="{ filled: form.telefone, error: errors.telefone }">
                <input id="login-phone" :value="form.telefone" @input="onPhoneInput($event, 'telefone')" type="tel" inputmode="numeric" placeholder=" " autocomplete="tel" :aria-invalid="errors.telefone" @focus="clearError('telefone')" @blur="validateField('telefone')" />
                <label for="login-phone">Telefone</label>
                <div class="field-focus-ring"></div>
              </div>
              <p v-if="errors.telefone" class="field-error">Informe um telefone válido</p>
            </div>
          </Transition>

          <div class="field-group">
            <div class="field-wrapper" :class="{ filled: form.senha, error: errors.senha }">
              <input id="login-password" v-model="form.senha" :type="showSenha ? 'text' : 'password'" placeholder=" " autocomplete="current-password" :aria-invalid="errors.senha" @input="clearError('senha')" @blur="validateField('senha')" />
              <label for="login-password">Senha</label>
              <div class="field-focus-ring"></div>
              <button type="button" class="btn-pw-toggle" @click="showSenha = !showSenha" tabindex="-1" :aria-label="showSenha ? 'Ocultar senha' : 'Mostrar senha'">
                <svg v-if="!showSenha" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
              </button>
            </div>
            <p v-if="errors.senha" class="field-error">A senha é obrigatória</p>
          </div>

          <div class="form-options">
            <label class="checkbox-label">
              <input type="checkbox" v-model="remember" class="checkbox-input" />
              <span class="checkbox-custom">
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
              </span>
              Lembrar-me
            </label>
            <a href="#" class="forgot-link" @click.prevent>Esqueceu a senha?</a>
          </div>

          <p class="error-msg" v-if="error" :key="error" role="alert">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
            {{ error }}
          </p>

          <button class="btn-login" type="submit" :disabled="loading">
            <span class="btn-content" :class="{ hidden: loading }">
              Entrar
            </span>
            <span class="btn-loading" :class="{ visible: loading }">
              <svg class="spin" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="32">
                  <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="0.8s" repeatCount="indefinite"/>
                </circle>
              </svg>
              Autenticando...
            </span>
          </button>
        </form>

        <div class="card-footer">
          <p>Novo por aqui? <router-link to="/registro">Criar conta</router-link></p>
        </div>
      </div>

      <div class="login-footer">
        <span>HydroTech v2.0</span>
        <span class="footer-dot"></span>
        <span>Sistema de Monitoramento Hidrológico</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
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
    error.value = err.response?.data?.detail || 'Credenciais inválidas. Verifique os dados e tente novamente.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (remember.value) {
    const saved = localStorage.getItem('login_email')
    if (saved) form.value.email = saved
  }
})
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: #060E1A;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ── Animated Background Orbs ── */
.bg-orbs {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  will-change: transform;
}

.orb--1 {
  width: 600px; height: 600px;
  background: radial-gradient(circle, rgba(14,165,233,0.12), transparent 70%);
  top: -15%;
  right: -10%;
  animation: orbFloat 25s ease-in-out infinite;
}

.orb--2 {
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(59,130,246,0.08), transparent 70%);
  bottom: -20%;
  left: -10%;
  animation: orbFloat 30s ease-in-out infinite reverse;
}

.orb--3 {
  width: 400px; height: 400px;
  background: radial-gradient(circle, rgba(16,185,129,0.05), transparent 70%);
  top: 40%;
  left: 60%;
  animation: orbFloat 20s ease-in-out infinite;
}

.orb--4 {
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(56,189,248,0.06), transparent 70%);
  top: 10%;
  left: 20%;
  animation: orbFloat 35s ease-in-out infinite reverse;
}

@keyframes orbFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -40px) scale(1.05); }
  50% { transform: translate(-20px, 20px) scale(0.95); }
  75% { transform: translate(40px, 30px) scale(1.02); }
}

/* ── Login Container ── */
.login-container {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 420px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

/* ── Card ── */
.login-card {
  width: 100%;
  background: rgba(13, 27, 46, 0.75);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 20px;
  padding: 36px 32px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  box-shadow:
    0 24px 80px rgba(0, 0, 0, 0.6),
    0 0 60px rgba(59, 130, 246, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.04);
  animation: cardIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  transition: border-color 0.4s ease, box-shadow 0.4s ease;
}

.login-card:hover {
  border-color: rgba(59, 130, 246, 0.12);
  box-shadow:
    0 24px 80px rgba(0, 0, 0, 0.6),
    0 0 60px rgba(59, 130, 246, 0.06),
    0 0 80px rgba(59, 130, 246, 0.03),
    inset 0 1px 0 rgba(255, 255, 255, 0.04);
}

@keyframes cardIn {
  from { opacity: 0; transform: translateY(24px) scale(0.97); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

/* ── Brand ── */
.card-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.25);
  flex-shrink: 0;
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.brand-name {
  font-size: 1rem;
  font-weight: 800;
  color: #F1F5F9;
  letter-spacing: -0.02em;
}

.brand-sub {
  font-size: 0.7rem;
  color: #4F6D8A;
  font-weight: 500;
  letter-spacing: 0.02em;
}

.card-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
  margin: 0;
}

.card-header h1 {
  font-size: 1.35rem;
  font-weight: 800;
  color: #F1F5F9;
  letter-spacing: -0.02em;
  line-height: 1.3;
}

.card-header p {
  font-size: 0.82rem;
  color: #4F6D8A;
  margin-top: 4px;
  font-weight: 400;
}

/* ── Mode Toggle ── */
.login-mode-toggle {
  display: flex;
  gap: 0;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  padding: 3px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.login-mode-toggle button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  padding: 10px 16px;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: #4F6D8A;
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.25s ease;
  font-family: inherit;
}

.login-mode-toggle button.active {
  background: #3B82F6;
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.login-mode-toggle button:not(.active):hover {
  color: #8AA6C1;
  background: rgba(255,255,255,0.04);
}

/* ── Form ── */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.field-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  border-radius: 10px;
}

.field-wrapper input {
  width: 100%;
  padding: 20px 44px 8px 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 10px;
  color: #F1F5F9;
  font-size: 0.9rem;
  transition: border-color 0.25s ease, background-color 0.25s ease;
  font-family: inherit;
  outline: none;
}

.field-wrapper input:focus {
  border-color: rgba(59, 130, 246, 0.4);
  background: rgba(255, 255, 255, 0.05);
}

.field-wrapper.error input {
  border-color: rgba(220, 38, 38, 0.4);
  background: rgba(220, 38, 38, 0.04);
}

.field-wrapper.error input:focus {
  border-color: rgba(220, 38, 38, 0.5);
}

.field-wrapper input::placeholder {
  color: transparent;
}

/* ── Focus Ring ── */
.field-focus-ring {
  position: absolute;
  inset: -1px;
  border-radius: 11px;
  pointer-events: none;
  transition: opacity 0.3s ease;
  opacity: 0;
  box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.3), 0 0 24px rgba(59, 130, 246, 0.06);
}

.field-wrapper:focus-within .field-focus-ring {
  opacity: 1;
}

.field-wrapper.error:focus-within .field-focus-ring {
  box-shadow: 0 0 0 1px rgba(220, 38, 38, 0.3), 0 0 24px rgba(220, 38, 38, 0.06);
  opacity: 1;
}

/* ── Floating Labels ── */
.field-wrapper label {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.875rem;
  color: #4F6D8A;
  pointer-events: none;
  transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 400;
  transform-origin: left center;
  line-height: 1;
}

.field-wrapper:focus-within label,
.field-wrapper.filled label {
  top: 8px;
  transform: translateY(0) scale(0.7);
  left: 14px;
  color: #3B82F6;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.field-wrapper.error label {
  color: rgba(220, 38, 38, 0.7);
}

.field-wrapper.error:focus-within label,
.field-wrapper.error.filled label {
  color: #DC2626;
}

/* ── Password Toggle ── */
.btn-pw-toggle {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #4F6D8A;
  cursor: pointer;
  padding: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: color 0.2s, background 0.2s;
}

.btn-pw-toggle:hover {
  color: #8AA6C1;
  background: rgba(255,255,255,0.06);
}

/* ── Form Options ── */
.form-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 2px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.82rem;
  color: #64748B;
  cursor: pointer;
  user-select: none;
  transition: color 0.2s;
}

.checkbox-label:hover {
  color: #8AA6C1;
}

.checkbox-input {
  display: none;
}

.checkbox-custom {
  width: 18px;
  height: 18px;
  border-radius: 5px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.checkbox-custom svg {
  opacity: 0;
  transition: opacity 0.15s ease;
  color: white;
}

.checkbox-input:checked + .checkbox-custom {
  background: #3B82F6;
  border-color: #3B82F6;
}

.checkbox-input:checked + .checkbox-custom svg {
  opacity: 1;
}

.forgot-link {
  font-size: 0.82rem;
  color: #3B82F6;
  font-weight: 600;
  text-decoration: none;
  transition: opacity 0.2s;
  opacity: 0.8;
}

.forgot-link:hover {
  opacity: 1;
}

/* ── Error Message ── */
.error-msg {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #DC2626;
  background: rgba(220, 38, 38, 0.08);
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 0.8rem;
  font-weight: 500;
  border: 1px solid rgba(220, 38, 38, 0.15);
  animation: shakeIn 0.4s ease;
}

.field-error {
  font-size: 0.72rem;
  color: rgba(220, 38, 38, 0.8);
  font-weight: 500;
  padding-left: 4px;
  animation: fadeIn 0.2s ease;
}

@keyframes shakeIn {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-5px); }
  40% { transform: translateX(5px); }
  60% { transform: translateX(-3px); }
  80% { transform: translateX(3px); }
}

/* ── Button ── */
.btn-login {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 14px;
  border-radius: 10px;
  background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
  color: white;
  font-weight: 700;
  font-size: 0.9rem;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 0.02em;
  overflow: hidden;
  min-height: 48px;
  font-family: inherit;
}

.btn-login::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 50%, #3B82F6 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.btn-login:hover:not(:disabled)::before {
  opacity: 1;
}

.btn-login:hover:not(:disabled) {
  box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
  transform: translateY(-1px);
}

.btn-login:active:not(:disabled) {
  transform: translateY(0);
  transition-duration: 0.1s;
}

.btn-login:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-content,
.btn-loading {
  position: relative;
  z-index: 1;
}

.btn-content {
  display: flex;
  align-items: center;
  gap: 8px;
  transition: opacity 0.2s ease;
}

.btn-loading {
  display: flex;
  align-items: center;
  gap: 8px;
  position: absolute;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.btn-content.hidden { opacity: 0; }
.btn-loading.visible { opacity: 1; }

/* ── Card Footer ── */
.card-footer {
  text-align: center;
  padding-top: 4px;
}

.card-footer p {
  font-size: 0.82rem;
  color: #4F6D8A;
}

.card-footer a {
  color: #3B82F6;
  font-weight: 600;
  text-decoration: none;
  transition: opacity 0.2s;
  position: relative;
}

.card-footer a::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 1px;
  background: #3B82F6;
  transition: width 0.25s ease;
}

.card-footer a:hover::after {
  width: 100%;
}

/* ── Page Footer ── */
.login-footer {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.72rem;
  color: rgba(79, 109, 138, 0.5);
  font-weight: 500;
}

.footer-dot {
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: rgba(79, 109, 138, 0.3);
}

/* ── Transitions ── */
.field-fade-enter-active {
  animation: fieldIn 0.25s ease-out;
}

.field-fade-leave-active {
  animation: fieldOut 0.2s ease-in;
}

@keyframes fieldIn {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fieldOut {
  from { opacity: 1; transform: translateY(0); }
  to { opacity: 0; transform: translateY(3px); }
}

/* ── Shared Animations ── */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* ── Reduced Motion ── */
@media (prefers-reduced-motion: reduce) {
  .orb { animation: none !important; }
  .login-card { animation: none; }
  .error-msg { animation: none; }
  .field-fade-enter-active,
  .field-fade-leave-active { transition: none !important; }
  .field-fade-enter-active { animation: none; }
  .field-fade-leave-active { animation: none; }
}

/* ── Responsive ── */
@media (max-width: 480px) {
  .login-container {
    padding: 16px;
    gap: 20px;
  }

  .login-card {
    padding: 28px 20px;
    border-radius: 16px;
    background: rgba(13, 27, 46, 0.85);
  }

  .card-header h1 {
    font-size: 1.2rem;
  }

  .login-mode-toggle button {
    font-size: 0.75rem;
    padding: 8px 12px;
  }

  .form-options {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }

  .orb { display: none; }
}
</style>
