import Home from '@/pages/dashboard/Home'

export default [
  {
    name: 'home',
    path: '/',
    component: Home,
    meta: { layout: 'Dashboard', requiresAuth: true }
  }
]
