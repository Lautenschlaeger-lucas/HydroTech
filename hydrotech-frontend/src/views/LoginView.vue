<template>
  <div class="login-page">
    <div class="mesh-bg"></div>

    <div class="login-split">
      <div class="login-panel-left">
        <!-- Brand -->
        <div class="panel-brand">
          <div class="panel-logo">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
              <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>
            </svg>
          </div>
          <span>HydroTech</span>
        </div>

        <div class="panel-content">
          <div class="status-chip">
            <span class="status-dot"></span>
            Sistema Operacional
          </div>

          <h1>Monitoramento<br/>Hidrológico</h1>
          <p class="panel-desc">Plataforma institucional de alta precisão para gestão de riscos de enchente e coordenação de infraestrutura crítica.</p>

          <!-- Metrics -->
          <div class="panel-metrics">
            <div class="metric-card">
              <span class="metric-value">127</span>
              <span class="metric-label">Rios monitorados</span>
            </div>
            <div class="metric-divider"></div>
            <div class="metric-card">
              <span class="metric-value">34</span>
              <span class="metric-label">Cidades</span>
            </div>
            <div class="metric-divider"></div>
            <div class="metric-card">
              <span class="metric-value">24/7</span>
              <span class="metric-label">Tempo real</span>
            </div>
          </div>

          <!-- Features -->
          <div class="panel-features">
            <div class="feature-item">
              <div class="feature-icon">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
              </div>
              <span>Monitoramento em tempo real</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
              </div>
              <span>Mapeamento de pontos de risco</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
              </div>
              <span>Alertas instantâneos via WhatsApp</span>
            </div>
          </div>
        </div>

        <!-- Animated Waves Footer -->
        <div class="panel-waves" aria-hidden="true">
          <svg class="wave wave--slow" viewBox="0 0 1440 120" preserveAspectRatio="none">
            <path d="M0,60 C360,120 720,0 1440,60 L1440,120 L0,120 Z" fill="var(--accent)" opacity="0.08"/>
          </svg>
          <svg class="wave wave--med" viewBox="0 0 1440 120" preserveAspectRatio="none">
            <path d="M0,80 C360,20 720,100 1440,40 L1440,120 L0,120 Z" fill="var(--accent)" opacity="0.05"/>
          </svg>
          <svg class="wave wave--fast" viewBox="0 0 1440 120" preserveAspectRatio="none">
            <path d="M0,90 C240,40 480,110 720,60 C960,10 1200,100 1440,50 L1440,120 L0,120 Z" fill="var(--accent)" opacity="0.03"/>
          </svg>
        </div>
      </div>

      <div class="login-panel-right">
        <div class="login-card">
          <div class="login-card-header">
            <h2>Acessar Sistema</h2>
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
            <Transition name="mode-fade" mode="out-in">
              <div v-if="loginMode === 'email'" key="email" class="form-group">
                <div class="input-wrapper" :class="{ filled: form.email, error: errors.email }">
                  <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                    <rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
                  </svg>
                  <input id="login-email" v-model="form.email" type="email" placeholder=" " autocomplete="email" :aria-invalid="errors.email" :aria-describedby="errors.email ? 'login-error' : undefined" @input="clearError('email')" @blur="validateField('email')"/>
                  <label for="login-email">E-mail</label>
                </div>
                <p v-if="errors.email" class="field-error">Informe um e-mail válido.</p>
              </div>
              <div v-else key="phone" class="form-group">
                <div class="input-wrapper" :class="{ filled: form.telefone, error: errors.telefone }">
                  <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                    <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/>
                  </svg>
                  <input id="login-phone" :value="form.telefone" @input="onPhoneInput($event, 'telefone')" type="tel" inputmode="numeric" placeholder=" " autocomplete="tel" :aria-invalid="errors.telefone" :aria-describedby="errors.telefone ? 'login-error' : undefined" @focus="clearError('telefone')" @blur="validateField('telefone')"/>
                  <label for="login-phone">Telefone</label>
                </div>
                <p v-if="errors.telefone" class="field-error">Informe um telefone válido.</p>
              </div>
            </Transition>

            <div class="form-group">
              <div class="input-wrapper" :class="{ filled: form.senha, error: errors.senha }">
                <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                  <rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
                <input id="login-password" v-model="form.senha" :type="showSenha ? 'text' : 'password'" placeholder=" " autocomplete="current-password" :aria-invalid="errors.senha" :aria-describedby="errors.senha ? 'login-error' : undefined" @input="clearError('senha')" @blur="validateField('senha')"/>
                <label for="login-password">Senha</label>
                <button type="button" class="btn-toggle-pw" @click="showSenha = !showSenha" tabindex="-1" :aria-label="showSenha ? 'Ocultar senha' : 'Mostrar senha'">
                  <svg v-if="!showSenha" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                  <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                </button>
              </div>
              <p v-if="errors.senha" class="field-error">A senha é obrigatória.</p>
            </div>

            <div class="form-options">
              <label class="checkbox-label">
                <input type="checkbox" v-model="remember" class="checkbox-input"/>
                <span class="checkbox-custom">
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
                </span>
                Lembrar-me
              </label>
              <a href="#" class="forgot-link" @click.prevent>Esqueceu a senha?</a>
            </div>

            <p class="error-msg" v-if="error" :key="error" id="login-error" role="alert" aria-live="polite">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>
              </svg>
              {{ error }}
            </p>

            <button class="btn-login" type="submit" :disabled="loading">
              <span class="btn-content" :class="{ hidden: loading }">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                  <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/>
                </svg>
                Acessar Sistema
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

          <div class="login-card-footer">
            <p>Novo usuário? <router-link to="/registro">Criar Conta</router-link></p>
          </div>
        </div>
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
    const el = document.getElementById(`login-${id === 'senha' ? 'password' : id}`)
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
  background: var(--bg-primary);
  position: relative;
  overflow: hidden;
}

.mesh-bg {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  z-index: 0;
  pointer-events: none;
  background:
    radial-gradient(ellipse at 20% 20%, rgba(14,165,233,0.08) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 80%, rgba(56,189,248,0.05) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 50%, rgba(2,132,199,0.03) 0%, transparent 50%);
}

.login-split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 100vh;
  position: relative;
  z-index: 1;
}

/* ── Left Panel ── */
.login-panel-left {
  position: relative;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border);
  padding: 32px 40px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.panel-logo {
  width: 32px; height: 32px;
  border-radius: var(--radius-sm);
  background: var(--accent-gradient);
  display: flex; align-items: center; justify-content: center;
  color: white;
  box-shadow: 0 0 16px rgba(59, 130, 246, 0.25);
}

.panel-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
  flex: 1;
  justify-content: center;
  max-width: 440px;
  position: relative;
  z-index: 2;
}

.status-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 5px 12px;
  border-radius: var(--radius-full);
  background: var(--status-active-bg);
  border: 1px solid rgba(16, 185, 129, 0.2);
  color: var(--status-active);
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  width: fit-content;
}

.status-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--status-active);
  animation: pulse 2s infinite;
}

.panel-content h1 {
  font-size: 2.2rem;
  font-weight: 800;
  line-height: 1.15;
  letter-spacing: -0.03em;
  color: var(--text-primary);
}

.panel-desc {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.7;
  max-width: 380px;
}

/* Metrics */
.panel-metrics {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  backdrop-filter: blur(4px);
}

.metric-card {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.metric-value {
  font-size: 1.3rem;
  font-weight: 800;
  color: var(--accent);
  line-height: 1;
  letter-spacing: -0.02em;
}

.metric-label {
  font-size: 0.65rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 600;
}

.metric-divider {
  width: 1px;
  height: 32px;
  background: var(--border);
}

/* Features */
.panel-features {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.82rem;
  color: var(--text-secondary);
}

.feature-icon {
  width: 24px; height: 24px;
  border-radius: var(--radius-sm);
  background: var(--accent-soft);
  color: var(--accent);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}

/* Animated Waves */
.panel-waves {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100px;
  pointer-events: none;
  z-index: 1;
}

.wave {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 200%;
  height: 100%;
}

.wave--slow {
  animation: waveSlide 12s linear infinite;
}
.wave--med {
  animation: waveSlide 8s linear infinite reverse;
}
.wave--fast {
  animation: waveSlide 5s linear infinite;
}

@keyframes waveSlide {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

/* ── Right Panel ── */
.login-panel-right {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 48px;
  position: relative;
  z-index: 2;
}

.login-card {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-xl);
  padding: 32px 28px;
  box-shadow: var(--shadow-xl), 0 0 60px rgba(59, 130, 246, 0.06);
  animation: fadeInUp 0.5s ease-out;
  transition: border-color 0.4s ease, box-shadow 0.4s ease;
  position: relative;
}

.login-card:hover {
  border-color: rgba(59, 130, 246, 0.2);
  box-shadow: var(--shadow-xl), 0 0 60px rgba(59, 130, 246, 0.06), 0 0 40px rgba(59, 130, 246, 0.08);
}

.login-card-header {
  text-align: center;
}

.login-card-header h2 {
  font-size: 1.4rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.login-card-header p {
  color: var(--text-secondary);
  font-size: 0.82rem;
  margin-top: 4px;
}

/* Login Mode Toggle */
.login-mode-toggle {
  display: flex;
  gap: 0;
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
  padding: 3px;
  border: 1px solid var(--border);
}

.login-mode-toggle button {
  flex: 1;
  display: flex; align-items: center; justify-content: center; gap: 7px;
  padding: 9px 16px;
  border-radius: calc(var(--radius-md) - 2px);
  border: none;
  background: transparent;
  color: var(--text-muted);
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.25s ease;
  font-family: inherit;
  position: relative;
  overflow: hidden;
}

.login-mode-toggle button.active {
  background: var(--accent);
  color: white;
  box-shadow: 0 2px 10px rgba(59, 130, 246, 0.35);
}

.login-mode-toggle button:not(.active):hover {
  color: var(--text-primary);
  background: rgba(255,255,255,0.04);
}

/* ── Form ── */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
  position: relative;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  border-radius: var(--radius-md);
}

.input-wrapper::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  pointer-events: none;
  transition: box-shadow 0.25s ease;
}

.input-wrapper:focus-within::after {
  box-shadow: 0 0 0 2px var(--accent-soft), 0 0 20px rgba(59, 130, 246, 0.08);
}

.input-wrapper.error:focus-within::after {
  box-shadow: 0 0 0 2px rgba(220, 38, 38, 0.2);
}

.input-icon {
  position: absolute;
  left: 14px;
  top: 24px;
  color: var(--text-muted);
  pointer-events: none;
  transition: color 0.25s ease;
  z-index: 2;
}

.input-wrapper:focus-within .input-icon {
  color: var(--accent);
}

.input-wrapper.error .input-icon {
  color: var(--risk-high);
}

.input-wrapper input {
  width: 100%;
  padding: 22px 44px 8px 42px;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-size: 0.9rem;
  transition: border-color 0.25s ease, background-color 0.25s ease, box-shadow 0.25s ease;
  font-family: inherit;
}

.input-wrapper input:focus {
  outline: none;
  border-color: var(--accent);
  background: var(--bg-card);
}

.input-wrapper.error input {
  border-color: rgba(220, 38, 38, 0.5);
  background: rgba(220, 38, 38, 0.04);
}

.input-wrapper.error input:focus {
  border-color: var(--risk-high);
}

.input-wrapper input::placeholder {
  color: transparent;
}

/* ── Floating Labels ── */
.input-wrapper label {
  position: absolute;
  left: 42px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.85rem;
  color: var(--text-muted);
  pointer-events: none;
  transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 400;
  z-index: 2;
  transform-origin: left center;
  line-height: 1;
}

.input-wrapper:focus-within label,
.input-wrapper.filled label {
  top: 10px;
  transform: translateY(0) scale(0.72);
  left: 40px;
  color: var(--accent);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.input-wrapper.error label {
  color: var(--risk-high);
}

.input-wrapper.error:focus-within label,
.input-wrapper.error.filled label {
  color: var(--risk-high);
}

/* Password Toggle */
.btn-toggle-pw {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: color 0.2s, background 0.2s;
  z-index: 2;
}

.btn-toggle-pw:hover {
  color: var(--text-primary);
  background: rgba(255,255,255,0.06);
}

/* Form Options */
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
  color: var(--text-secondary);
  cursor: pointer;
  user-select: none;
}

.checkbox-input {
  display: none;
}

.checkbox-custom {
  width: 18px;
  height: 18px;
  border-radius: 4px;
  border: 2px solid var(--border);
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
  background: var(--accent);
  border-color: var(--accent);
}

.checkbox-input:checked + .checkbox-custom svg {
  opacity: 1;
}

.checkbox-label:hover .checkbox-custom {
  border-color: var(--accent);
}

.forgot-link {
  font-size: 0.82rem;
  color: var(--accent);
  font-weight: 600;
  text-decoration: none;
  transition: opacity 0.2s;
}

.forgot-link:hover {
  opacity: 0.7;
  text-decoration: underline;
}

/* Error Message */
.error-msg {
  display: flex; align-items: center; gap: 8px;
  color: var(--risk-high);
  background: var(--risk-high-bg);
  padding: 10px 14px;
  border-radius: var(--radius-md);
  font-size: 0.82rem; font-weight: 500;
  border: 1px solid rgba(220, 38, 38, 0.2);
  animation: shakeIn 0.4s ease;
}

@keyframes shakeIn {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-6px); }
  40% { transform: translateX(6px); }
  60% { transform: translateX(-4px); }
  80% { transform: translateX(4px); }
}

@media (prefers-reduced-motion: reduce) {
  .error-msg { animation: none; }
  .login-card { animation: none; }
  .status-dot { animation: none; }
  .wave { animation: none; }
  .wave--slow, .wave--med, .wave--fast { animation: none; }
  .mode-fade-enter-active,
  .mode-fade-leave-active { transition: none !important; }
}

.field-error {
  font-size: 0.72rem;
  color: var(--risk-high);
  margin-top: 2px;
  padding-left: 2px;
  font-weight: 500;
  animation: fadeIn 0.25s ease;
}

/* Login Button */
.btn-login {
  position: relative;
  display: flex; align-items: center; justify-content: center;
  width: 100%; padding: 14px;
  border-radius: var(--radius-md);
  background: var(--accent-gradient);
  color: white;
  font-weight: 700; font-size: 0.9rem;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 0.02em;
  overflow: hidden;
  min-height: 48px;
  background-size: 200% 100%;
  background-position: 0% 50%;
}

.btn-login::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 50%, #3B82F6 100%);
  background-size: 200% 100%;
  background-position: 0% 50%;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.btn-login:hover:not(:disabled)::before {
  opacity: 1;
}

.btn-login:hover:not(:disabled) {
  box-shadow: 0 0 30px rgba(59, 130, 246, 0.35), 0 4px 12px rgba(0, 0, 0, 0.3);
  transform: translateY(-2px);
  background-position: 100% 50%;
}

.btn-login:active:not(:disabled) {
  transform: translateY(0);
  transition-duration: 0.1s;
}

.btn-login:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-content,
.btn-loading {
  position: relative;
  z-index: 1;
}

.btn-content {
  display: flex; align-items: center; gap: 8px;
  transition: opacity 0.2s ease;
}

.btn-loading {
  display: flex; align-items: center; gap: 8px;
  position: absolute;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.btn-content.hidden { opacity: 0; }
.btn-loading.visible { opacity: 1; }

/* Footer */
.login-card-footer {
  text-align: center;
}

.login-card-footer p {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.login-card-footer a {
  color: var(--accent);
  font-weight: 600;
  text-decoration: none;
  transition: opacity 0.2s;
  position: relative;
}

.login-card-footer a::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 1px;
  background: var(--accent);
  transition: width 0.25s ease;
}

.login-card-footer a:hover::after {
  width: 100%;
}

.login-card-footer a:hover {
  opacity: 1;
}

/* ── Mode Transition ── */
.mode-fade-enter-active {
  animation: modeIn 0.3s ease-out;
}

.mode-fade-leave-active {
  animation: modeOut 0.2s ease-in;
}

@keyframes modeIn {
  from { opacity: 0; transform: translateY(-6px) scale(0.98); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes modeOut {
  from { opacity: 1; transform: translateY(0) scale(1); }
  to { opacity: 0; transform: translateY(4px) scale(0.98); }
}

/* Animations */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

/* ── Responsive ── */
@media (max-width: 1024px) {
  .login-panel-left {
    padding: 24px 28px;
  }
  .panel-content h1 {
    font-size: 1.6rem;
  }
  .panel-metrics {
    gap: 12px;
    padding: 12px 16px;
  }
}

@media (max-width: 768px) {
  .login-split {
    grid-template-columns: 1fr;
  }

  .login-panel-left {
    padding: 20px 24px 60px;
    border-right: none;
    border-bottom: 1px solid var(--border);
    min-height: auto;
  }

  .panel-content {
    justify-content: flex-start;
    gap: 16px;
    padding: 12px 0 0;
  }

  .panel-content h1 {
    font-size: 1.4rem;
  }

  .panel-desc {
    font-size: 0.8rem;
  }

  .panel-metrics {
    display: none;
  }

  .panel-waves {
    display: none;
  }

  .panel-features {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 6px;
  }

  .feature-item {
    font-size: 0.72rem;
    gap: 6px;
    background: rgba(255,255,255,0.03);
    padding: 6px 10px;
    border-radius: var(--radius-md);
    border: 1px solid var(--border-light);
  }

  .feature-icon {
    width: 20px; height: 20px;
  }

  .login-panel-right {
    padding: 24px 16px;
    align-items: flex-start;
  }

  .login-card {
    padding: 28px 20px;
    background: transparent;
    border: none;
    backdrop-filter: none;
    box-shadow: none;
  }
}

@media (max-width: 480px) {
  .login-panel-left {
    padding: 16px 16px 48px;
  }

  .panel-content h1 {
    font-size: 1.2rem;
  }

  .login-panel-right {
    padding: 16px 12px;
  }

  .login-card {
    padding: 20px 12px;
    gap: 18px;
  }

  .login-mode-toggle button {
    font-size: 0.72rem;
    padding: 8px 10px;
  }

  .form-options {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
}
</style>
