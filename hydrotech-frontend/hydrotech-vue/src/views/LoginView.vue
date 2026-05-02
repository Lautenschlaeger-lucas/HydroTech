<template>
  <div class="login-page">
    <div class="login-wrapper">
      <div class="login-card">

        <!-- Header -->
        <div class="login-header">
          <div class="login-logo">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>
            </svg>
          </div>
          <h1>Bem-vindo de volta</h1>
          <p>Acesse sua conta para gerenciar o monitoramento</p>
        </div>

        <!-- Form -->
        <form @submit.prevent="login" class="login-form">
          <div class="form-group">
            <label for="login-email">E-mail</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
              <input
                id="login-email"
                v-model="form.email"
                type="email"
                placeholder="seu@email.com"
                autocomplete="email"
              />
            </div>
          </div>

          <div class="form-group">
            <label for="login-password">Senha</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              <input
                id="login-password"
                v-model="form.senha"
                type="password"
                placeholder="Digite sua senha"
                autocomplete="current-password"
              />
            </div>
          </div>

          <button class="btn-login" type="submit" :disabled="loading">
            <svg v-if="loading" class="spinner" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="32"><animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="0.8s" repeatCount="indefinite"/></circle></svg>
            <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
            {{ loading ? 'Entrando...' : 'Entrar' }}
          </button>
        </form>

        <p class="error-msg" v-if="error" :class="{ shake: error }">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
          {{ error }}
        </p>

        <div class="login-footer">
          <p>Não tem uma conta? <router-link to="/registro">Crie agora</router-link></p>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const form = ref({ email: '', senha: '' })
const loading = ref(false)
const error = ref('')

const login = async () => {
  if (!form.value.email || !form.value.senha) {
    error.value = 'Preencha todos os campos.'
    return
  }

  loading.value = true
  error.value = ''

  try {
    const response = await api.login({
      email: form.value.email,
      senha: form.value.senha,
    })
    const { access, refresh, usuario } = response.data

    localStorage.setItem('user_token', access)
    localStorage.setItem('refresh_token', refresh)
    localStorage.setItem('user_name', usuario.nome)
    window.dispatchEvent(new Event('storage-update'))
    router.push('/dashboard')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erro ao realizar login.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(170deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
}

.login-wrapper {
  min-height: calc(100vh - 72px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.login-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 48px 44px;
  width: 100%;
  max-width: 440px;
  box-shadow: var(--shadow-xl);
  display: flex;
  flex-direction: column;
  gap: 24px;
  animation: fadeInUp 0.4s ease-out;
}

/* Header */
.login-header {
  text-align: center;
}

.login-logo {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  border-radius: var(--radius-lg);
  background: var(--accent-soft);
  color: var(--accent);
  margin-bottom: 20px;
}

.login-header h1 {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.login-header p {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-top: 6px;
}

/* Form */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.form-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  pointer-events: none;
}

.input-wrapper input {
  padding-left: 42px;
}

/* Login Button */
.btn-login {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: 100%;
  padding: 13px;
  border-radius: var(--radius-md);
  background: var(--accent-gradient);
  color: white;
  font-weight: 700;
  font-size: 0.95rem;
  border: none;
  cursor: pointer;
  margin-top: 4px;
  transition: transform var(--transition-normal), box-shadow var(--transition-normal);
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: var(--shadow-glow);
}

.btn-login:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.spinner {
  animation: spin 0.8s linear infinite;
}

/* Error */
.error-msg {
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: center;
  color: var(--risk-high);
  background: var(--risk-high-bg);
  padding: 10px 16px;
  border-radius: var(--radius-md);
  font-size: 0.85rem;
  font-weight: 500;
}

.error-msg.shake {
  animation: shake 0.5s ease-out;
}

/* Footer */
.login-footer {
  text-align: center;
  margin-top: 4px;
}

.login-footer p {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.login-footer a {
  color: var(--accent);
  text-decoration: none;
  font-weight: 600;
}

.login-footer a:hover {
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 480px) {
  .login-card {
    padding: 32px 24px;
  }

  .login-header h1 {
    font-size: 1.35rem;
  }
}
</style>