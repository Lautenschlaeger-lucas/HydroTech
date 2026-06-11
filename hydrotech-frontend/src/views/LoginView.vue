<template>
  <div class="login-page">
    <div class="bg-base"></div>
    <div class="bg-topo"></div>
    <div class="bg-radar"></div>
    <div class="bg-particles">
      <div v-for="i in 12" :key="i" class="particle" :style="particleStyle(i)"></div>
    </div>
    <div class="bg-scanline"></div>

    <div class="login-container">
      <div class="login-card">
        <div class="card-accent"></div>

        <div class="card-header">
          <div class="brand-block">
            <div class="brand-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z" fill="rgba(255,255,255,0.1)"/>
              </svg>
            </div>
            <div class="brand-lines">
              <span class="brand-name">HydroTech</span>
              <span class="brand-sub">MONITORAMENTO HIDROLÓGICO</span>
            </div>
          </div>
          <div class="brand-badge">v2.0</div>
        </div>

        <div class="card-body">
          <div class="card-title">
            <span class="title-label">ACESSO RESTRITO</span>
            <h1>Autenticação</h1>
            <p>Informe suas credenciais para acessar o painel de monitoramento</p>
          </div>

          <div class="mode-tabs">
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
            <Transition name="slide" mode="out-in">
              <div v-if="loginMode === 'email'" key="email" class="field-box">
                <label for="login-email">E-MAIL</label>
                <div class="field-wrap" :class="{ error: errors.email }">
                  <input id="login-email" v-model="form.email" type="email" placeholder=" " autocomplete="email" :aria-invalid="errors.email" @input="clearError('email')" @blur="validateField('email')" />
                  <span class="field-bar"></span>
                </div>
                <p v-if="errors.email" class="field-err">Informe um e-mail válido</p>
              </div>
              <div v-else key="phone" class="field-box">
                <label for="login-phone">TELEFONE</label>
                <div class="field-wrap" :class="{ error: errors.telefone }">
                  <input id="login-phone" :value="form.telefone" @input="onPhoneInput($event, 'telefone')" type="tel" inputmode="numeric" placeholder=" " autocomplete="tel" :aria-invalid="errors.telefone" @focus="clearError('telefone')" @blur="validateField('telefone')" />
                  <span class="field-bar"></span>
                </div>
                <p v-if="errors.telefone" class="field-err">Informe um telefone válido</p>
              </div>
            </Transition>

            <div class="field-box">
              <label for="login-password">SENHA</label>
              <div class="field-wrap" :class="{ error: errors.senha }">
                <input id="login-password" v-model="form.senha" :type="showSenha ? 'text' : 'password'" placeholder=" " autocomplete="current-password" :aria-invalid="errors.senha" @input="clearError('senha')" @blur="validateField('senha')" />
                <span class="field-bar"></span>
                <button type="button" class="btn-eye" @click="showSenha = !showSenha" tabindex="-1" :aria-label="showSenha ? 'Ocultar senha' : 'Mostrar senha'">
                  <svg v-if="!showSenha" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                  <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                </button>
              </div>
              <p v-if="errors.senha" class="field-err">A senha é obrigatória</p>
            </div>

            <div class="form-meta">
              <label class="check-wrap">
                <input type="checkbox" v-model="remember" class="check-input" />
                <span class="check-box">
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
                </span>
                Manter sessão
              </label>
              <a href="#" class="forgot" @click.prevent>Recuperar senha</a>
            </div>

            <p class="error-msg" v-if="error" :key="error" role="alert">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
              {{ error }}
            </p>

            <button class="btn-submit" type="submit" :disabled="loading">
              <span class="btn-inner" :class="{ hidden: loading }">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
                Acessar Plataforma
              </span>
              <span class="btn-load" :class="{ visible: loading }">
                <svg class="spin" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="32">
                    <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="0.8s" repeatCount="indefinite"/>
                  </circle>
                </svg>
                Autenticando...
              </span>
            </button>
          </form>
        </div>

        <div class="card-footer">
          <p>Novo usuário? <router-link to="/registro">Cadastre-se</router-link></p>
          <div class="footer-sec">
            <span class="sec-dot"></span>
            <span>Conexão segura</span>
          </div>
        </div>
      </div>

      <div class="page-footer">
        <span>HydroTech — Sistema de Monitoramento Hidrológico</span>
        <span class="sep"></span>
        <span>© 2026</span>
        <span class="sep"></span>
        <span>Defesa Civil</span>
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

const particleStyle = (i) => {
  const x = ((i * 31) % 100)
  const y = ((i * 17 + 23) % 100)
  const size = 1.5 + (i % 3) * 1.5
  const dur = 8 + (i % 5) * 4
  const delay = (i * 0.7) % 8
  return {
    left: `${x}%`,
    top: `${y}%`,
    width: `${size}px`,
    height: `${size}px`,
    animationDuration: `${dur}s`,
    animationDelay: `${delay}s`,
    opacity: 0.2 + (i % 4) * 0.15
  }
}

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
  background: #050B14;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ══════════════ BACKGROUND ══════════════ */
.bg-base {
  position: fixed; inset: 0; z-index: 0;
  background: linear-gradient(170deg, #050B14 0%, #0A1628 35%, #0D1B2E 60%, #050B14 100%);
}

.bg-topo {
  position: fixed; inset: 0; z-index: 1;
  opacity: 0.15;
  background-image:
    radial-gradient(circle at 30% 50%, transparent 0%, transparent 40%, rgba(59,130,246,0.06) 42%, transparent 44%),
    radial-gradient(circle at 70% 60%, transparent 0%, transparent 35%, rgba(59,130,246,0.04) 37%, transparent 39%),
    radial-gradient(circle at 50% 30%, transparent 0%, transparent 50%, rgba(59,130,246,0.03) 52%, transparent 54%),
    radial-gradient(circle at 20% 70%, transparent 0%, transparent 45%, rgba(56,189,248,0.04) 47%, transparent 49%),
    radial-gradient(circle at 80% 40%, transparent 0%, transparent 38%, rgba(56,189,248,0.03) 40%, transparent 42%),
    radial-gradient(circle at 40% 80%, transparent 0%, transparent 42%, rgba(59,130,246,0.05) 44%, transparent 46%);
  background-size: 200px 200px;
  animation: topoShift 40s linear infinite;
}

@keyframes topoShift {
  0% { transform: translate(0, 0) rotate(0deg); }
  33% { transform: translate(20px, -15px) rotate(0.5deg); }
  66% { transform: translate(-10px, 10px) rotate(-0.3deg); }
  100% { transform: translate(0, 0) rotate(0deg); }
}

.bg-radar {
  position: fixed; z-index: 1;
  width: 500px; height: 500px;
  border-radius: 50%;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  background: radial-gradient(circle, rgba(59,130,246,0.04) 0%, transparent 60%);
  animation: radarPulse 5s ease-in-out infinite;
}

@keyframes radarPulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
  50% { transform: translate(-50%, -50%) scale(1.3); opacity: 1; }
}

.bg-scanline {
  position: fixed; inset: 0; z-index: 2;
  pointer-events: none;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0,0,0,0.03) 2px,
    rgba(0,0,0,0.03) 4px
  );
}

/* ── Particles ── */
.bg-particles {
  position: fixed; inset: 0; z-index: 2;
  pointer-events: none;
}

.particle {
  position: absolute;
  border-radius: 50%;
  background: rgba(59, 130, 246, 0.4);
  box-shadow: 0 0 6px rgba(59, 130, 246, 0.2);
  animation: particleFloat linear infinite;
}

@keyframes particleFloat {
  0% { transform: translateY(0) scale(1); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translateY(-120px) scale(0.5); opacity: 0; }
}

/* ══════════════ CONTAINER ══════════════ */
.login-container {
  position: relative; z-index: 3;
  width: 100%; max-width: 440px;
  padding: 20px;
  display: flex; flex-direction: column; align-items: center; gap: 24px;
}

/* ══════════════ CARD ══════════════ */
.login-card {
  width: 100%;
  background: linear-gradient(180deg, rgba(15,25,45,0.95) 0%, rgba(10,18,35,0.98) 100%);
  border: 1px solid rgba(59, 130, 246, 0.08);
  border-radius: 12px;
  display: flex; flex-direction: column;
  box-shadow:
    0 30px 80px rgba(0,0,0,0.6),
    0 0 60px rgba(59,130,246,0.03),
    inset 0 1px 0 rgba(255,255,255,0.03);
  animation: cardIn 0.55s ease-out;
  position: relative;
  overflow: hidden;
}

.card-accent {
  position: absolute;
  top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent, #3B82F6, #60A5FA, #3B82F6, transparent);
  background-size: 200% 100%;
  animation: accentSlide 3s ease-in-out infinite;
}

@keyframes accentSlide {
  0%, 100% { background-position: 200% 0; }
  50% { background-position: 0% 0; }
}

@keyframes cardIn {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ── Card Header ── */
.card-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255,255,255,0.04);
}

.brand-block {
  display: flex; align-items: center; gap: 12px;
}

.brand-icon {
  width: 36px; height: 36px;
  border-radius: 8px;
  background: linear-gradient(135deg, #1D4ED8 0%, #3B82F6 100%);
  display: flex; align-items: center; justify-content: center;
  color: white;
  box-shadow: 0 2px 12px rgba(59,130,246,0.25);
}

.brand-lines {
  display: flex; flex-direction: column; gap: 1px;
}

.brand-name {
  font-size: 1rem; font-weight: 800;
  color: #E2E8F0; letter-spacing: -0.02em;
}

.brand-sub {
  font-size: 0.6rem; font-weight: 600;
  color: #3B82F6; letter-spacing: 0.15em;
}

.brand-badge {
  font-size: 0.6rem; font-weight: 700;
  color: #4F6D8A;
  background: rgba(255,255,255,0.03);
  padding: 3px 10px;
  border-radius: 20px;
  border: 1px solid rgba(255,255,255,0.04);
  letter-spacing: 0.05em;
}

/* ── Card Body ── */
.card-body {
  padding: 24px;
  display: flex; flex-direction: column; gap: 20px;
}

.card-title {
  display: flex; flex-direction: column; gap: 4px;
}

.title-label {
  font-size: 0.6rem; font-weight: 700;
  color: #3B82F6; letter-spacing: 0.15em;
  text-transform: uppercase;
}

.card-title h1 {
  font-size: 1.35rem; font-weight: 700;
  color: #F1F5F9; letter-spacing: -0.02em;
  line-height: 1.2;
}

.card-title p {
  font-size: 0.82rem; color: #4F6D8A;
  margin-top: 4px; line-height: 1.5;
}

/* ── Mode Tabs ── */
.mode-tabs {
  display: flex; gap: 0;
  background: rgba(255,255,255,0.02);
  border-radius: 8px;
  padding: 3px;
  border: 1px solid rgba(255,255,255,0.04);
}

.mode-tabs button {
  flex: 1;
  display: flex; align-items: center; justify-content: center; gap: 6px;
  padding: 9px 16px;
  border-radius: 6px;
  border: none;
  background: transparent;
  color: #4F6D8A;
  font-weight: 600; font-size: 0.78rem;
  cursor: pointer;
  transition: all 0.25s ease;
  font-family: inherit;
}

.mode-tabs button.active {
  background: #3B82F6;
  color: white;
  box-shadow: 0 2px 10px rgba(59,130,246,0.25);
}

.mode-tabs button:not(.active):hover {
  color: #8AA6C1;
  background: rgba(255,255,255,0.04);
}

/* ── Form ── */
.login-form {
  display: flex; flex-direction: column; gap: 18px;
}

.field-box {
  display: flex; flex-direction: column; gap: 5px;
}

.field-box label {
  font-size: 0.65rem; font-weight: 700;
  color: #4F6D8A; letter-spacing: 0.1em;
  padding-left: 2px;
}

.field-wrap {
  position: relative; display: flex; align-items: center;
  border-radius: 6px;
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.05);
  transition: border-color 0.25s ease, background 0.25s ease;
}

.field-wrap:focus-within {
  border-color: rgba(59,130,246,0.2);
  background: rgba(59,130,246,0.03);
}

.field-wrap.error {
  border-color: rgba(220,38,38,0.25);
  background: rgba(220,38,38,0.03);
}

.field-wrap input {
  width: 100%; padding: 12px 44px 12px 14px;
  background: transparent;
  border: none;
  color: #E2E8F0;
  font-size: 0.9rem; font-family: inherit;
  outline: none;
}

.field-wrap input::placeholder {
  color: #2A4A6A;
}

.field-bar {
  position: absolute; bottom: -1px; left: 0; right: 0; height: 1px;
  background: #3B82F6;
  transform: scaleX(0); transform-origin: center;
  transition: transform 0.3s cubic-bezier(0.4,0,0.2,1);
  opacity: 0.5;
}

.field-wrap:focus-within .field-bar {
  transform: scaleX(1);
}

.field-wrap.error .field-bar {
  background: #DC2626;
  transform: scaleX(1);
  opacity: 0.6;
}

.field-err {
  font-size: 0.7rem; color: rgba(220,38,38,0.7);
  font-weight: 500; padding-left: 4px;
  animation: fadeIn 0.2s ease;
}

/* ── Eye Toggle ── */
.btn-eye {
  position: absolute; right: 8px; top: 50%; transform: translateY(-50%);
  background: none; border: none;
  color: #4F6D8A; cursor: pointer;
  padding: 6px; display: flex; align-items: center; justify-content: center;
  border-radius: 4px;
  transition: color 0.2s, background 0.2s;
}

.btn-eye:hover {
  color: #8AA6C1;
  background: rgba(255,255,255,0.04);
}

/* ── Form Meta ── */
.form-meta {
  display: flex; align-items: center; justify-content: space-between;
  margin-top: -2px;
}

.check-wrap {
  display: flex; align-items: center; gap: 8px;
  font-size: 0.8rem; color: #4F6D8A;
  cursor: pointer; user-select: none;
  transition: color 0.2s;
}

.check-wrap:hover { color: #8AA6C1; }

.check-input { display: none; }

.check-box {
  width: 17px; height: 17px;
  border-radius: 3px;
  border: 2px solid rgba(255,255,255,0.08);
  background: transparent;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.2s ease; flex-shrink: 0;
}

.check-box svg { opacity: 0; transition: opacity 0.15s ease; color: white; }

.check-input:checked + .check-box {
  background: #3B82F6;
  border-color: #3B82F6;
}

.check-input:checked + .check-box svg { opacity: 1; }

.forgot {
  font-size: 0.8rem; color: #3B82F6;
  font-weight: 600; text-decoration: none;
  opacity: 0.7; transition: opacity 0.2s;
}

.forgot:hover { opacity: 1; }

/* ── Error ── */
.error-msg {
  display: flex; align-items: center; gap: 8px;
  color: #DC2626;
  background: rgba(220,38,38,0.06);
  padding: 10px 14px;
  border-radius: 6px;
  font-size: 0.8rem; font-weight: 500;
  border: 1px solid rgba(220,38,38,0.1);
  animation: shake 0.35s ease;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  50% { transform: translateX(4px); }
  75% { transform: translateX(-2px); }
}

/* ── Submit Button ── */
.btn-submit {
  position: relative;
  display: flex; align-items: center; justify-content: center;
  width: 100%; padding: 13px;
  border-radius: 6px;
  background: linear-gradient(135deg, #2563EB 0%, #3B82F6 100%);
  color: white;
  font-weight: 700; font-size: 0.88rem;
  border: none; cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
  min-height: 48px;
  font-family: inherit;
  letter-spacing: 0.01em;
}

.btn-submit::before {
  content: '';
  position: absolute; inset: 0;
  border-radius: inherit;
  background: linear-gradient(135deg, #1D4ED8 0%, #2563EB 50%, #3B82F6 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.btn-submit::after {
  content: '';
  position: absolute; inset: -2px;
  border-radius: inherit;
  background: linear-gradient(135deg, #3B82F6, #60A5FA);
  opacity: 0;
  transition: opacity 0.4s ease;
  z-index: -1;
  filter: blur(8px);
}

.btn-submit:hover:not(:disabled)::before { opacity: 1; }
.btn-submit:hover:not(:disabled)::after { opacity: 0.3; }

.btn-submit:hover:not(:disabled) {
  transform: translateY(-1px);
}

.btn-submit:active:not(:disabled) {
  transform: translateY(0);
  transition-duration: 0.1s;
}

.btn-submit:disabled {
  opacity: 0.4; cursor: not-allowed;
}

.btn-inner, .btn-load {
  position: relative; z-index: 1;
  display: flex; align-items: center; gap: 8px;
}

.btn-inner { transition: opacity 0.2s ease; }
.btn-load { position: absolute; opacity: 0; transition: opacity 0.2s ease; }
.btn-inner.hidden { opacity: 0; }
.btn-load.visible { opacity: 1; }

/* ── Card Footer ── */
.card-footer {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 24px;
  border-top: 1px solid rgba(255,255,255,0.04);
  background: rgba(0,0,0,0.15);
}

.card-footer p {
  font-size: 0.8rem; color: #4F6D8A;
}

.card-footer a {
  color: #3B82F6; font-weight: 600;
  text-decoration: none; transition: opacity 0.2s;
}

.card-footer a:hover { opacity: 0.8; }

.footer-sec {
  display: flex; align-items: center; gap: 6px;
  font-size: 0.65rem; color: #2A4A6A;
  font-weight: 600;
}

.sec-dot {
  width: 5px; height: 5px;
  border-radius: 50%;
  background: #10B981;
  box-shadow: 0 0 6px rgba(16,185,129,0.3);
  animation: dotPulse 2s infinite;
}

@keyframes dotPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

/* ── Page Footer ── */
.page-footer {
  display: flex; align-items: center; gap: 8px;
  font-size: 0.68rem; color: rgba(79,109,138,0.35);
  font-weight: 500; flex-wrap: wrap; justify-content: center;
}

.sep {
  width: 3px; height: 3px;
  border-radius: 50%;
  background: rgba(79,109,138,0.2);
}

/* ── Transitions ── */
.slide-enter-active { animation: slideIn 0.22s ease-out; }
.slide-leave-active { animation: slideOut 0.18s ease-in; }

@keyframes slideIn {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideOut {
  from { opacity: 1; transform: translateY(0); }
  to { opacity: 0; transform: translateY(4px); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* ── Reduced Motion ── */
@media (prefers-reduced-motion: reduce) {
  .login-card, .bg-topo, .bg-radar, .bg-accent { animation: none !important; }
  .particle { display: none; }
  .card-accent { animation: none; }
  .error-msg { animation: none; }
  .slide-enter-active, .slide-leave-active { transition: none !important; }
  .slide-enter-active { animation: none; }
  .slide-leave-active { animation: none; }
}

/* ── Responsive ── */
@media (max-width: 480px) {
  .login-container { padding: 12px; }
  .card-header { padding: 16px; }
  .card-body { padding: 20px 16px; }
  .card-footer { padding: 12px 16px; flex-direction: column; gap: 8px; align-items: flex-start; }
  .card-title h1 { font-size: 1.15rem; }
  .mode-tabs button { font-size: 0.72rem; padding: 8px 10px; }
  .form-meta { flex-direction: column; gap: 8px; align-items: flex-start; }
  .page-footer { font-size: 0.62rem; }
  .bg-particles { display: none; }
}
</style>
