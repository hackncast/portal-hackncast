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
    meta: { layout: 'Public' }
  },
  {
    path: '/user/registration',
    name: 'user:registration',
    component: Registration,
    meta: { layout: 'Public' }
  },
  {
    path: '/user/email/confirmation/:key/',
    name: 'user:email_confirmation',
    component: EmailConfirmation,
    meta: { mayRequiresAuth: true }
  },
  {
    path: '/user/password/reset/send/',
    name: 'user:reset_password',
    component: ResetPassword,
    meta: { layout: 'Public' }
  },
  {
    path: '/user/password/reset/token/:uidb64/:token/',
    name: 'user:reset_password_token',
    component: ResetPasswordToken,
    meta: { layout: 'Public' }
  },
  {
    path: '/user/profile',
    name: 'user:profile',
    component: ProfileAccount,
    meta: { layout: 'UserProfile', requiresAuth: true }
  },
  {
    path: '/user/profile/emails',
    name: 'user:profile:emails',
    component: ProfileEmails,
    meta: { layout: 'UserProfile', requiresAuth: true }
  },
  {
    path: '/user/profile/security',
    name: 'user:profile:security',
    component: ProfileSecurity,
    meta: { layout: 'UserProfile', requiresAuth: true }
  }
]
