import { meta } from '@/layouts'

import Home from '@/pages/dashboard/Home'

export default [
  {
    name: 'home',
    path: '/',
    component: Home,
    meta: { ...meta.dashboard }
  }
]
