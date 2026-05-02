<template>
  <div class="register-page">
    <div class="register-wrapper">
      <div class="register-card">

        <!-- Header -->
        <div class="register-header">
          <div class="register-logo">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>
            </svg>
          </div>
          <h1>Criar sua conta</h1>
          <p>Preencha os dados para acessar o monitoramento</p>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleRegistro" class="register-form">
          <div class="form-group">
            <label for="reg-nome">Nome Completo</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
              <input id="reg-nome" v-model="form.nome" type="text" placeholder="Digite seu nome" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="reg-email">E-mail</label>
              <div class="input-wrapper">
                <svg class="input-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
                <input id="reg-email" v-model="form.email" type="email" placeholder="seu@email.com" />
              </div>
            </div>
            <div class="form-group">
              <label for="reg-nascimento">Data de Nascimento</label>
              <div class="input-wrapper">
                <svg class="input-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                <input id="reg-nascimento" v-model="form.data_nascimento" type="date" />
              </div>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="reg-senha">Senha</label>
              <div class="input-wrapper">
                <svg class="input-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                <input id="reg-senha" v-model="form.senha" type="password" placeholder="Crie uma senha" />
              </div>
            </div>
            <div class="form-group">
              <label for="reg-confirmar">Confirmar Senha</label>
              <div class="input-wrapper">
                <svg class="input-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                <input id="reg-confirmar" v-model="form.confirmarSenha" type="password" placeholder="Repita a senha" />
              </div>
            </div>
          </div>

          <!-- Password strength -->
          <div class="pw-strength" v-if="form.senha">
            <div class="pw-bar">
              <div class="pw-fill" :class="pwStrengthClass" :style="{ width: pwStrengthPercent + '%' }"></div>
            </div>
            <span class="pw-label" :class="pwStrengthClass">{{ pwStrengthLabel }}</span>
          </div>

          <button class="btn-register" type="submit" :disabled="loading">
            <svg v-if="loading" class="spinner" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="32"><animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="0.8s" repeatCount="indefinite"/></circle></svg>
            <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><line x1="19" y1="8" x2="19" y2="14"/><line x1="22" y1="11" x2="16" y2="11"/></svg>
            {{ loading ? 'Processando...' : 'Criar Conta' }}
          </button>
        </form>

        <p class="error-msg" v-if="error">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
          {{ error }}
        </p>

        <p class="success-msg" v-if="success">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
          {{ success }}
        </p>

        <div class="register-footer">
          <p>Já tem uma conta? <router-link to="/login">Faça Login</router-link></p>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

import api from '../services/api'

const router = useRouter()
const loading = ref(false)
const error = ref('')
const success = ref('')

const form = ref({
  nome: '',
  email: '',
  data_nascimento: '',
  senha: '',
  confirmarSenha: ''
})

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

  if (!form.value.nome || !form.value.email || !form.value.data_nascimento || !form.value.senha) {
    error.value = 'Preencha todos os campos obrigatórios.'
    return
  }

  if (form.value.senha !== form.value.confirmarSenha) {
    error.value = 'As senhas não conferem.'
    return
  }

  loading.value = true

  try {
    const data = {
      nome: form.value.nome,
      email: form.value.email,
      senha: form.value.senha,
      data_nascimento: form.value.data_nascimento,
    }
    const response = await api.register(data)
    const { access, refresh, usuario } = response.data

    localStorage.setItem('user_token', access)
    localStorage.setItem('refresh_token', refresh)
    localStorage.setItem('user_name', usuario.nome)
    window.dispatchEvent(new Event('storage-update'))
    success.value = 'Conta criada com sucesso! Redirecionando...'

    setTimeout(() => {
      router.push('/dashboard')
    }, 1500)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ocorreu um erro ao criar a conta. Verifique o servidor.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(170deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
}

.register-wrapper {
  min-height: calc(100vh - 72px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.register-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 48px 44px;
  width: 100%;
  max-width: 520px;
  box-shadow: var(--shadow-xl);
  display: flex;
  flex-direction: column;
  gap: 20px;
  animation: fadeInUp 0.4s ease-out;
}

/* Header */
.register-header {
  text-align: center;
}

.register-logo {
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

.register-header h1 {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.register-header p {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-top: 6px;
}

/* Form */
.register-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
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

/* Password Strength */
.pw-strength {
  display: flex;
  align-items: center;
  gap: 10px;
}

.pw-bar {
  flex: 1;
  height: 4px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.pw-fill {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width 0.3s ease, background 0.3s ease;
}

.pw-fill.pw-weak { background: var(--risk-high); }
.pw-fill.pw-medium { background: var(--risk-medium); }
.pw-fill.pw-strong { background: var(--risk-low); }

.pw-label {
  font-size: 0.75rem;
  font-weight: 600;
  min-width: 45px;
}

.pw-label.pw-weak { color: var(--risk-high); }
.pw-label.pw-medium { color: var(--risk-medium); }
.pw-label.pw-strong { color: var(--risk-low); }

/* Register Button */
.btn-register {
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

.btn-register:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: var(--shadow-glow);
}

.btn-register:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.spinner {
  animation: spin 0.8s linear infinite;
}

/* Messages */
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

.success-msg {
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: center;
  color: var(--risk-low);
  background: var(--risk-low-bg);
  padding: 10px 16px;
  border-radius: var(--radius-md);
  font-size: 0.85rem;
  font-weight: 500;
}

/* Footer */
.register-footer {
  text-align: center;
  margin-top: 4px;
}

.register-footer p {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.register-footer a {
  color: var(--accent);
  text-decoration: none;
  font-weight: 600;
}

.register-footer a:hover {
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 480px) {
  .register-card {
    padding: 32px 24px;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>