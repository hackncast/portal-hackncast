import Login from '@/pages/auth/Login'
import Registration from '@/pages/auth/Registration'
import ResetPassword from '@/pages/auth/ResetPassword'

export const base = 'auth'
export default [
  {path: '/login', component: Login},
  {path: '/registration', component: Registration},
  {path: '/reset', component: ResetPassword}
]
