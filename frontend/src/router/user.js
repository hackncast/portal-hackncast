import Outside from '@/pages/layouts/Outside'
import EmailConfirmation from '@/pages/user/EmailConfirmation'
import ResetPasswordToken from '@/pages/user/ResetPasswordToken'
import ResetPassword from '@/pages/user/ResetPassword'
import Registration from '@/pages/user/Registration'
import Login from '@/pages/user/Login'

export default [
  {
    path: '/user',
    component: Outside,
    children: [
      {path: 'email_confirmation', name: 'user:email_confirmation', component: EmailConfirmation},
      {path: 'password/reset/send/', name: 'user:reset_password', component: ResetPassword},
      {path: 'password/reset/token/:uidb64/:token/', name: 'user:reset_password_token', component: ResetPasswordToken},
      {path: 'registration', name: 'user:registration', component: Registration},
      {path: 'login', name: 'user:login', component: Login}
    ]
  }
]
