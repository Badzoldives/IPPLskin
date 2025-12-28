import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../components/LandingPage.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import AISkinCheck from '../components/AISkinCheck.vue'
import History from '../components/History.vue'
import Documentation from '../components/Documentation.vue'
import ChatbotPage from '../components/ChatbotPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingPage,
      meta: { title: 'SkinCheck - AI Skin Disease Detection' }
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { title: 'Login - SkinCheck' }
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      meta: { title: 'Register - SkinCheck' }
    },
    {
      path: '/ai-check',
      name: 'aicheck',
      component: AISkinCheck,
      meta: { title: 'AI Skin Check - SkinCheck', requiresAuth: false }
    },
    {
      path: '/history',
      name: 'history',
      component: History,
      meta: { title: 'History - SkinCheck', requiresAuth: true }
    },
    {
      path: '/dokumentasi',
      name: 'documentation',
      component: Documentation,
      meta: { title: 'Dokumentasi - SkinCheck' }
    },
    {
      path: '/chatbot',
      name: 'chatbot',
      component: ChatbotPage,
      meta: { title: 'AI Chatbot - SkinCheck' }
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0, behavior: 'smooth' }
    }
  }
})

// Update document title
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'SkinCheck'
  next()
})

export default router
