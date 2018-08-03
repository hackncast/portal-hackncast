import Login from '@/pages/auth/Login'
import Registration from '@/pages/auth/Registration'

export const base = 'auth'
export default [
  {path: '/login', component: Login},
  {path: '/registration', component: Registration}
]
