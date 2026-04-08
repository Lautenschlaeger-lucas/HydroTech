import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import RiosView from '../views/RiosView.vue'
import UsuariosView from '../views/UsuariosView.vue'
import LoginView from '../views/LoginView.vue'
import LandingPage from '@/views/LandingPage.vue'
import RegistroView from '@/views/RegistroView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
    {
    path: '/registro',
    name: 'registro',
    component: RegistroView
    },
    {
      path: '/',
      name: 'home',
      component: LandingPage
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/rios',
      name: 'rios',
      component: RiosView
    },
    {
      path: '/usuarios',
      name: 'usuarios',
      component: UsuariosView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    }
  ]
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('user_token')

  const privatePages = ['/dashboard', '/rios', '/usuarios']
  const authRequired = privatePages.includes(to.path)

  if (authRequired && !isAuthenticated) {
    next('/login')
  } 
  else if (to.path === '/login' && isAuthenticated) {
    next('/dashboard')
  } 
  else {
    next()
  }
})


export default router