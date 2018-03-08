import Outside from '@/pages/layouts/Outside'
import Profile from '@/pages/layouts/Profile'

import Login from '@/pages/user/Login'
import Registration from '@/pages/user/Registration'
import ResetPassword from '@/pages/user/ResetPassword'
import EmailConfirmation from '@/pages/user/EmailConfirmation'
import ResetPasswordToken from '@/pages/user/ResetPasswordToken'

import ProfileEmails from '@/pages/user/profile/Emails'
import ProfileAccount from '@/pages/user/profile/Account'
import ProfileSecurity from '@/pages/user/profile/Security'

import UserProfileNavbar from '@/components/UserProfileNavbar'

let UserProfile = { 'navbarExtend': UserProfileNavbar }

export default [
  {
    path: '/user',
    component: Outside,
    children: [
      { path: 'email/confirmation/:key/', name: 'user:email_confirmation', component: EmailConfirmation, meta: { mayRequiresAuth: true } },
      { path: 'password/reset/send/', name: 'user:reset_password', component: ResetPassword },
      { path: 'password/reset/token/:uidb64/:token/', name: 'user:reset_password_token', component: ResetPasswordToken },
      { path: 'registration', name: 'user:registration', component: Registration },
      { path: 'login', name: 'user:login', component: Login }
    ]
  },
  {
    path: '/user/profile',
    component: Profile,
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'user:profile', components: Object.assign({ 'default': ProfileAccount }, UserProfile) },
      { path: 'emails', name: 'user:profile:emails', components: Object.assign({ 'default': ProfileEmails }, UserProfile) },
      { path: 'security', name: 'user:profile:security', components: Object.assign({ 'default': ProfileSecurity }, UserProfile) }
    ]
  }
]
