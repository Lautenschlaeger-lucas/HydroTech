<template>
  <div class="login-page">
    <div class="bg-gradient"></div>
    <div class="bg-grid"></div>
    <div class="bg-glow"></div>
    <div class="bg-accent-line"></div>

    <div class="login-container">
      <div class="login-card">
        <div class="card-brand">
          <div class="brand-logo">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z" fill="rgba(59,130,246,0.15)"/>
            </svg>
          </div>
          <div class="brand-text">
            <span class="brand-name">HydroTech</span>
            <span class="brand-tagline">Monitoramento Hidrológico</span>
          </div>
        </div>

        <div class="card-header">
          <h1>Acessar o sistema</h1>
          <p>Informe seus dados para entrar na plataforma</p>
        </div>

        <div class="mode-selector">
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
          <Transition name="field-swipe" mode="out-in">
            <div v-if="loginMode === 'email'" key="email" class="field-group">
              <label for="login-email">E-mail</label>
              <div class="field-input" :class="{ error: errors.email }">
                <input id="login-email" v-model="form.email" type="email" placeholder="seu@email.com" autocomplete="email" :aria-invalid="errors.email" @input="clearError('email')" @blur="validateField('email')" />
                <div class="input-border"></div>
              </div>
              <p v-if="errors.email" class="field-error">Informe um e-mail válido</p>
            </div>
            <div v-else key="phone" class="field-group">
              <label for="login-phone">Telefone</label>
              <div class="field-input" :class="{ error: errors.telefone }">
                <input id="login-phone" :value="form.telefone" @input="onPhoneInput($event, 'telefone')" type="tel" inputmode="numeric" placeholder="(99) 99999-9999" autocomplete="tel" :aria-invalid="errors.telefone" @focus="clearError('telefone')" @blur="validateField('telefone')" />
                <div class="input-border"></div>
              </div>
              <p v-if="errors.telefone" class="field-error">Informe um telefone válido</p>
            </div>
          </Transition>

          <div class="field-group">
            <label for="login-password">Senha</label>
            <div class="field-input" :class="{ error: errors.senha }">
              <input id="login-password" v-model="form.senha" :type="showSenha ? 'text' : 'password'" placeholder="Sua senha" autocomplete="current-password" :aria-invalid="errors.senha" @input="clearError('senha')" @blur="validateField('senha')" />
              <div class="input-border"></div>
              <button type="button" class="btn-pw" @click="showSenha = !showSenha" tabindex="-1" :aria-label="showSenha ? 'Ocultar senha' : 'Mostrar senha'">
                <svg v-if="!showSenha" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
              </button>
            </div>
            <p v-if="errors.senha" class="field-error">A senha é obrigatória</p>
          </div>

          <div class="form-footer">
            <label class="checkbox-label">
              <input type="checkbox" v-model="remember" class="checkbox-input" />
              <span class="checkbox-mark">
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
              </span>
              Continuar conectado
            </label>
            <a href="#" class="forgot-link" @click.prevent>Esqueceu a senha?</a>
          </div>

          <p class="error-msg" v-if="error" :key="error" role="alert">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
            {{ error }}
          </p>

          <button class="btn-login" type="submit" :disabled="loading">
            <span class="btn-content" :class="{ hidden: loading }">Entrar no sistema</span>
            <span class="btn-loading" :class="{ visible: loading }">
              <svg class="spin" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="32">
                  <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="0.8s" repeatCount="indefinite"/>
                </circle>
              </svg>
              Entrando...
            </span>
          </button>
        </form>

        <p class="card-signup">
          Não tem conta? <router-link to="/registro">Cadastre-se</router-link>
        </p>
      </div>

      <p class="login-version">HydroTech v2.0 — Plataforma de Monitoramento Hidrológico</p>
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

/* ── Background Layers ── */
.bg-gradient {
  position: fixed;
  inset: 0;
  z-index: 0;
  background: linear-gradient(160deg, #060E1A 0%, #09131F 30%, #0D1B2E 60%, #060E1A 100%);
}

.bg-grid {
  position: fixed;
  inset: 0;
  z-index: 1;
  background-image:
    linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse 70% 60% at 50% 50%, black 20%, transparent 70%);
  -webkit-mask-image: radial-gradient(ellipse 70% 60% at 50% 50%, black 20%, transparent 70%);
}

.bg-glow {
  position: fixed;
  width: 700px;
  height: 700px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(59,130,246,0.08), transparent 70%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1;
  pointer-events: none;
  animation: glowPulse 6s ease-in-out infinite;
}

.bg-accent-line {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  z-index: 2;
  background: linear-gradient(90deg, transparent, #3B82F6, #2563EB, #3B82F6, transparent);
  background-size: 200% 100%;
  animation: lineSweep 4s ease-in-out infinite;
}

@keyframes glowPulse {
  0%, 100% { opacity: 0.6; transform: translate(-50%, -50%) scale(1); }
  50% { opacity: 1; transform: translate(-50%, -50%) scale(1.08); }
}

@keyframes lineSweep {
  0%, 100% { background-position: 200% 0; }
  50% { background-position: 0% 0; }
}

/* ── Container ── */
.login-container {
  position: relative;
  z-index: 3;
  width: 100%;
  max-width: 420px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

/* ── Card ── */
.login-card {
  width: 100%;
  background: #0F1F35;
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 16px;
  padding: 40px 36px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.5),
    0 0 40px rgba(59, 130, 246, 0.03);
  animation: cardUp 0.55s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  border-left: 2px solid rgba(59, 130, 246, 0.15);
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.login-card:hover {
  border-left-color: rgba(59, 130, 246, 0.3);
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.5),
    0 0 60px rgba(59, 130, 246, 0.05);
}

@keyframes cardUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ── Brand ── */
.card-brand {
  display: flex;
  align-items: center;
  gap: 14px;
}

.brand-logo {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, #1D4ED8 0%, #3B82F6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
  flex-shrink: 0;
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.brand-name {
  font-size: 1.1rem;
  font-weight: 800;
  color: #F1F5F9;
  letter-spacing: -0.03em;
}

.brand-tagline {
  font-size: 0.72rem;
  color: #4F6D8A;
  font-weight: 500;
  letter-spacing: 0.03em;
}

/* ── Header ── */
.card-header h1 {
  font-size: 1.4rem;
  font-weight: 700;
  color: #F1F5F9;
  letter-spacing: -0.02em;
  line-height: 1.3;
}

.card-header p {
  font-size: 0.85rem;
  color: #4F6D8A;
  margin-top: 6px;
  line-height: 1.5;
}

/* ── Mode Selector ── */
.mode-selector {
  display: flex;
  gap: 0;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  padding: 3px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.mode-selector button {
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

.mode-selector button.active {
  background: #3B82F6;
  color: #fff;
  box-shadow: 0 4px 14px rgba(59, 130, 246, 0.3);
}

.mode-selector button:not(.active):hover {
  color: #8AA6C1;
  background: rgba(255, 255, 255, 0.04);
}

/* ── Form ── */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-group label {
  font-size: 0.78rem;
  font-weight: 600;
  color: #64748B;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding-left: 2px;
}

.field-input {
  position: relative;
  display: flex;
  align-items: center;
  border-radius: 8px;
}

.field-input input {
  width: 100%;
  padding: 13px 44px 13px 16px;
  background: rgba(255, 255, 255, 0.03);
  border: none;
  border-radius: 8px;
  color: #F1F5F9;
  font-size: 0.9rem;
  font-family: inherit;
  outline: none;
  transition: background 0.2s ease;
}

.field-input input:focus {
  background: rgba(255, 255, 255, 0.05);
}

.field-input input::placeholder {
  color: #2A4A6A;
  font-weight: 400;
}

.field-input.error input {
  background: rgba(220, 38, 38, 0.04);
}

/* ── Input Border (animated underline) ── */
.input-border {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1.5px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 0 0 8px 8px;
  overflow: hidden;
  pointer-events: none;
}

.input-border::after {
  content: '';
  position: absolute;
  inset: 0;
  background: #3B82F6;
  transform: scaleX(0);
  transform-origin: center;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.field-input:focus-within .input-border::after {
  transform: scaleX(1);
}

.field-input.error .input-border::after {
  background: #DC2626;
  transform: scaleX(1);
}

/* ── Password Toggle ── */
.btn-pw {
  position: absolute;
  right: 8px;
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

.btn-pw:hover {
  color: #8AA6C1;
  background: rgba(255, 255, 255, 0.05);
}

/* ── Form Footer ── */
.form-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: -4px;
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

.checkbox-mark {
  width: 18px;
  height: 18px;
  border-radius: 4px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.checkbox-mark svg {
  opacity: 0;
  transition: opacity 0.15s ease;
  color: #fff;
}

.checkbox-input:checked + .checkbox-mark {
  background: #3B82F6;
  border-color: #3B82F6;
}

.checkbox-input:checked + .checkbox-mark svg {
  opacity: 1;
}

.forgot-link {
  font-size: 0.82rem;
  color: #3B82F6;
  font-weight: 600;
  text-decoration: none;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.forgot-link:hover {
  opacity: 1;
}

/* ── Error ── */
.error-msg {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #DC2626;
  background: rgba(220, 38, 38, 0.08);
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 500;
  border: 1px solid rgba(220, 38, 38, 0.12);
  animation: shake 0.4s ease;
}

.field-error {
  font-size: 0.72rem;
  color: rgba(220, 38, 38, 0.8);
  font-weight: 500;
  padding-left: 4px;
  animation: fadeIn 0.2s ease;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  50% { transform: translateX(4px); }
  75% { transform: translateX(-2px); }
}

/* ── Button ── */
.btn-login {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 14px;
  border-radius: 8px;
  background: linear-gradient(135deg, #2563EB 0%, #3B82F6 100%);
  color: #fff;
  font-weight: 700;
  font-size: 0.9rem;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 0.01em;
  overflow: hidden;
  min-height: 48px;
  font-family: inherit;
}

.btn-login::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(135deg, #1D4ED8 0%, #2563EB 50%, #3B82F6 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.btn-login:hover:not(:disabled)::before {
  opacity: 1;
}

.btn-login:hover:not(:disabled) {
  box-shadow: 0 6px 28px rgba(59, 130, 246, 0.3);
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

/* ── Signup Link ── */
.card-signup {
  text-align: center;
  font-size: 0.85rem;
  color: #4F6D8A;
}

.card-signup a {
  color: #3B82F6;
  font-weight: 600;
  text-decoration: none;
  position: relative;
}

.card-signup a::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 0;
  height: 1px;
  background: #3B82F6;
  transition: width 0.25s ease;
}

.card-signup a:hover::after {
  width: 100%;
}

/* ── Version Footer ── */
.login-version {
  font-size: 0.72rem;
  color: rgba(79, 109, 138, 0.4);
  font-weight: 500;
  text-align: center;
  letter-spacing: 0.02em;
}

/* ── Field Transition ── */
.field-swipe-enter-active {
  animation: swipeIn 0.25s ease-out;
}

.field-swipe-leave-active {
  animation: swipeOut 0.2s ease-in;
}

@keyframes swipeIn {
  from { opacity: 0; transform: translateY(-6px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes swipeOut {
  from { opacity: 1; transform: translateY(0); }
  to { opacity: 0; transform: translateY(4px); }
}

/* ── Shared ── */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* ── Reduced Motion ── */
@media (prefers-reduced-motion: reduce) {
  .login-card { animation: none; }
  .bg-glow, .bg-accent-line { animation: none; }
  .error-msg { animation: none; }
  .field-swipe-enter-active, .field-swipe-leave-active { transition: none !important; }
  .field-swipe-enter-active { animation: none; }
  .field-swipe-leave-active { animation: none; }
}

/* ── Responsive ── */
@media (max-width: 480px) {
  .login-container { padding: 16px; }
  .login-card { padding: 28px 20px; border-left-width: 1px; border-radius: 12px; }
  .card-header h1 { font-size: 1.2rem; }
  .mode-selector button { font-size: 0.75rem; padding: 8px 12px; }
  .form-footer { flex-direction: column; gap: 10px; align-items: flex-start; }
  .bg-grid { background-size: 40px 40px; }
}
</style>
