<template>
  <header class="header" :class="{ 'header--scrolled': isScrolled }">
    <div class="header-container">

      <!-- Brand -->
      <router-link to="/" class="brand">
        <div class="brand-logo">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>
          </svg>
        </div>
        <span class="brand-text">Hydro<span class="brand-accent">Tech</span></span>
      </router-link>

      <!-- Desktop Nav -->
      <nav class="nav" :class="{ 'nav--open': mobileOpen }">
        <router-link v-if="isLoggedIn" to="/dashboard" class="nav-link" @click="closeMobile">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
          Dashboard
        </router-link>
        <router-link v-if="isLoggedIn" to="/rios" class="nav-link" @click="closeMobile">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M2 18c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/></svg>
          Rios
        </router-link>
        <router-link v-if="isLoggedIn" to="/usuarios" class="nav-link" @click="closeMobile">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          Usuários
        </router-link>

        <!-- Mobile-only auth -->
        <div class="nav-mobile-auth" v-if="mobileOpen">
          <template v-if="!isLoggedIn">
            <router-link to="/login" class="nav-link" @click="closeMobile">Entrar</router-link>
            <router-link to="/registro" class="btn-cta-mobile" @click="closeMobile">Criar Conta</router-link>
          </template>
          <button v-else class="btn-logout-mobile" @click="logout">Sair da Conta</button>
        </div>
      </nav>

      <!-- Desktop Actions -->
      <div class="actions">
        <template v-if="!isLoggedIn">
          <router-link to="/login" class="btn-text">Entrar</router-link>
          <router-link to="/registro" class="btn-cta">Criar Conta</router-link>
        </template>
        <template v-else>
          <div class="user-badge">
            <div class="user-avatar">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            </div>
            <span class="user-name">{{ userName }}</span>
          </div>
          <button @click="logout" class="btn-logout">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
            Sair
          </button>
        </template>

        <button class="theme-toggle" @click="toggleTheme" :title="theme === 'dark' ? 'Modo claro' : 'Modo escuro'">
          <svg v-if="theme === 'dark'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
          </svg>
          <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
          </svg>
        </button>

        <!-- Hamburger -->
        <button class="hamburger" :class="{ 'hamburger--open': mobileOpen }" @click="mobileOpen = !mobileOpen">
          <span></span><span></span><span></span>
        </button>
      </div>

    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const theme = ref('light')
const isLoggedIn = ref(!!localStorage.getItem('user_token'))
const userName = ref(localStorage.getItem('user_name') || 'Usuário')
const mobileOpen = ref(false)
const isScrolled = ref(false)

const checkLogin = () => {
  isLoggedIn.value = !!localStorage.getItem('user_token')
  userName.value = localStorage.getItem('user_name') || 'Usuário'
}

const closeMobile = () => {
  mobileOpen.value = false
}

const toggleTheme = () => {
  const newTheme = theme.value === 'light' ? 'dark' : 'light'
  theme.value = newTheme
  localStorage.setItem('theme', newTheme)
  document.documentElement.setAttribute('data-theme', newTheme)
  window.dispatchEvent(new Event('theme-changed'))
}

const logout = () => {
  localStorage.removeItem('user_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user_name')
  checkLogin()
  closeMobile()
  router.push('/')
}

const handleScroll = () => {
  isScrolled.value = window.scrollY > 10
}

onMounted(() => {
  theme.value = localStorage.getItem('theme') || 'light'
  window.addEventListener('storage-update', checkLogin)
  window.addEventListener('storage', checkLogin)
  window.addEventListener('scroll', handleScroll, { passive: true })
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('storage-update', checkLogin)
  window.removeEventListener('storage', checkLogin)
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.header {
  width: 100%;
  height: 72px;
  background: var(--nav-bg);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid transparent;
  position: sticky;
  top: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  transition: border-color var(--transition-normal), box-shadow var(--transition-normal);
}

.header--scrolled {
  border-bottom-color: var(--border);
  box-shadow: var(--shadow-sm);
}

.header-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Brand */
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  z-index: 10;
}

.brand-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: var(--radius-md);
  background: var(--accent-gradient);
  color: white;
}

.brand-text {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.brand-accent {
  color: var(--accent);
}

/* Nav */
.nav {
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  color: var(--text-secondary);
  font-weight: 500;
  font-size: 0.9rem;
  padding: 8px 14px;
  border-radius: var(--radius-md);
  transition: color var(--transition-fast), background-color var(--transition-fast);
}

.nav-link:hover {
  color: var(--text-primary);
  background-color: var(--accent-soft);
}

.nav-link.router-link-active {
  color: var(--accent);
  background-color: var(--accent-soft);
  font-weight: 600;
}

.nav-mobile-auth {
  display: none;
}

/* Actions */
.actions {
  display: flex;
  align-items: center;
  gap: 10px;
  z-index: 10;
}

.btn-text {
  text-decoration: none;
  color: var(--text-primary);
  font-weight: 600;
  font-size: 0.875rem;
  padding: 8px 14px;
  border-radius: var(--radius-md);
  transition: background-color var(--transition-fast);
}

.btn-text:hover {
  background-color: var(--bg-secondary);
}

.btn-cta {
  display: inline-flex;
  align-items: center;
  background: var(--accent-gradient);
  color: white;
  padding: 9px 20px;
  border-radius: var(--radius-md);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.875rem;
  transition: transform var(--transition-fast), box-shadow var(--transition-fast);
}

.btn-cta:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-glow);
}

.user-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: var(--radius-full);
  background: var(--bg-secondary);
  border: 1px solid var(--border);
}

.user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: var(--radius-full);
  background: var(--accent-gradient);
  color: white;
}

.user-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-primary);
}

.btn-logout {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: var(--radius-md);
  background: var(--risk-high-bg);
  color: var(--risk-high);
  font-weight: 600;
  font-size: 0.85rem;
  border: 1px solid transparent;
  transition: all var(--transition-fast);
}

.btn-logout:hover {
  background: var(--risk-high);
  color: white;
  transform: none;
}

.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: var(--radius-md);
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  color: var(--text-secondary);
  transition: all var(--transition-fast);
}

.theme-toggle:hover {
  color: var(--accent);
  border-color: var(--accent);
  background: var(--accent-soft);
  transform: none;
}

/* Hamburger */
.hamburger {
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 38px;
  height: 38px;
  border-radius: var(--radius-md);
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  gap: 5px;
  padding: 0;
  cursor: pointer;
}

.hamburger span {
  display: block;
  width: 18px;
  height: 2px;
  background: var(--text-primary);
  border-radius: 2px;
  transition: all 0.3s ease;
  transform-origin: center;
}

.hamburger--open span:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}

.hamburger--open span:nth-child(2) {
  opacity: 0;
  transform: scaleX(0);
}

.hamburger--open span:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

/* ── Responsive ── */
@media (max-width: 768px) {
  .hamburger {
    display: flex;
  }

  .nav {
    position: fixed;
    top: 72px;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--card-bg);
    flex-direction: column;
    align-items: stretch;
    padding: 20px;
    gap: 4px;
    transform: translateX(100%);
    transition: transform 0.3s ease;
    z-index: 999;
  }

  .nav--open {
    transform: translateX(0);
  }

  .nav-link {
    font-size: 1rem;
    padding: 14px 16px;
    border-radius: var(--radius-md);
  }

  .nav-mobile-auth {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: auto;
    padding-top: 20px;
    border-top: 1px solid var(--border);
  }

  .btn-cta-mobile {
    display: block;
    text-align: center;
    background: var(--accent-gradient);
    color: white;
    padding: 14px;
    border-radius: var(--radius-md);
    text-decoration: none;
    font-weight: 600;
  }

  .btn-logout-mobile {
    padding: 14px;
    border-radius: var(--radius-md);
    background: var(--risk-high-bg);
    color: var(--risk-high);
    font-weight: 600;
    border: none;
    cursor: pointer;
  }

  .actions .btn-text,
  .actions .btn-cta,
  .actions .btn-logout,
  .actions .user-badge {
    display: none;
  }
}

@media (max-width: 480px) {
  .brand-text {
    font-size: 1.15rem;
  }
}
</style>