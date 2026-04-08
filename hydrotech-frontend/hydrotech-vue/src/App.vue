<template>
  <div class="app-wrapper" :data-theme="theme">
    <LandingHeader />

    <main class="main-content" :class="{ 'full-width': isFullWidth }">
      <RouterView v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>

    <LandingFooter />

    <ToastNotification ref="toastRef" />
    <ConfirmModal ref="modalRef" />
  </div>
</template>

<script setup>
import { ref, onMounted, provide, computed } from 'vue'
import { useRoute } from 'vue-router'
import LandingHeader from '@/views/LandingHeader.vue'
import LandingFooter from '@/views/LandingFooter.vue'
import ToastNotification from '@/components/ToastNotification.vue'
import ConfirmModal from '@/components/ConfirmModal.vue'

const route = useRoute()
const theme = ref(localStorage.getItem('theme') || 'light')
const toastRef = ref(null)
const modalRef = ref(null)

// Provide toast & modal to all child components
provide('toast', {
  success: (...args) => toastRef.value?.success(...args),
  error: (...args) => toastRef.value?.error(...args),
  info: (...args) => toastRef.value?.info(...args),
  warning: (...args) => toastRef.value?.warning(...args),
})

provide('modal', {
  show: (...args) => modalRef.value?.show(...args),
})

const isFullWidth = computed(() => {
  return route.path === '/' || route.path === '/login' || route.path === '/registro'
})

const updateTheme = () => {
  const savedTheme = localStorage.getItem('theme') || 'light'
  theme.value = savedTheme
  document.documentElement.setAttribute('data-theme', savedTheme)
}

onMounted(() => {
  updateTheme()
  window.addEventListener('theme-changed', updateTheme)
})
</script>

<style scoped>
.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  width: 100%;
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 32px 24px;
}

.main-content.full-width {
  max-width: 100% !important;
  padding: 0 !important;
  margin: 0 !important;
}

/* Page Transitions */
.page-enter-active {
  animation: pageIn 0.3s ease-out;
}

.page-leave-active {
  animation: pageOut 0.15s ease-in;
}

@keyframes pageIn {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pageOut {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}
</style>