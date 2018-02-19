import Outside from '@/pages/layouts/Outside'
import Registration from '@/pages/user/Registration'
import Login from '@/pages/user/Login'

export default [
  {
    path: '/user',
    component: Outside,
    children: [
      {path: 'registration', name: 'user:registration', component: Registration},
      {path: 'login', name: 'user:login', component: Login}
    ]
  }
]
