import { meta } from '@/layouts'

import Login from '@/pages/user/Login'
import Registration from '@/pages/user/Registration'
import ResetPassword from '@/pages/user/ResetPassword'
import EmailConfirmation from '@/pages/user/EmailConfirmation'
import ResetPasswordToken from '@/pages/user/ResetPasswordToken'

import ProfileEmails from '@/pages/user/profile/Emails'
import ProfileAccount from '@/pages/user/profile/Account'
import ProfileSecurity from '@/pages/user/profile/Security'

export default [
  {
    path: '/user/login',
    name: 'user:login',
    component: Login,
    meta: { ...meta.public }
  },
  {
    path: '/user/registration',
    name: 'user:registration',
    component: Registration,
    meta: { ...meta.public }
  },
  {
    path: '/user/email/confirmation/:key/',
    name: 'user:email_confirmation',
    component: EmailConfirmation,
    meta: { ...meta.publicMayAuth }
  },
  {
    path: '/user/password/reset/send/',
    name: 'user:reset_password',
    component: ResetPassword,
    meta: { ...meta.public }
  },
  {
    path: '/user/password/reset/token/:uidb64/:token/',
    name: 'user:reset_password_token',
    component: ResetPasswordToken,
    meta: { ...meta.public }
  },
  {
    path: '/user/profile',
    name: 'user:profile',
    component: ProfileAccount,
    meta: { ...meta.userProfile }
  },
  {
    path: '/user/profile/emails',
    name: 'user:profile:emails',
    component: ProfileEmails,
    meta: { ...meta.userProfile }
  },
  {
    path: '/user/profile/security',
    name: 'user:profile:security',
    component: ProfileSecurity,
    meta: { ...meta.userProfile }
  }
]
