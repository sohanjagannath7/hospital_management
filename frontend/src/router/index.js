import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  { path: '/', name: 'Home', component: () => import('@/views/HomeView.vue') },
  { path: '/login', name: 'Login', component: () => import('@/views/LoginView.vue') },
  { path: '/register', name: 'Register', component: () => import('@/views/RegisterView.vue') },
  {
    path: '/patient',
    meta: { requiresAuth: true, role: 'patient' },
    children: [
      { path: 'intake', name: 'PatientIntake', component: () => import('@/views/PatientIntakeView.vue') },
      { path: 'cases', name: 'MyCases', component: () => import('@/views/MyCasesView.vue') },
      { path: 'chat', name: 'Chat', component: () => import('@/views/ChatView.vue') },
      { path: 'profile', name: 'PatientProfile', component: () => import('@/views/PatientProfileView.vue') },
    ]
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { requiresAuth: true, role: 'staff' },
  },
  {
    path: '/cases',
    name: 'CaseManagement',
    component: () => import('@/views/CaseManagementView.vue'),
    meta: { requiresAuth: true, role: 'staff' },
  },
  {
    path: '/analytics',
    name: 'Analytics',
    component: () => import('@/views/AnalyticsView.vue'),
    meta: { requiresAuth: true, role: 'staff' },
  },
  {
    path: '/providers',
    name: 'Providers',
    component: () => import('@/views/ProvidersView.vue'),
    meta: { requiresAuth: true, role: 'staff' },
  },
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next('/login')
  } else if (to.meta.role === 'staff' && auth.isPatient) {
    next('/patient/intake')
  } else if (to.meta.role === 'patient' && auth.isProvider) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
