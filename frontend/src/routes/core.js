import Home from '@/pages/Home'
import NotFound from '@/pages/NotFound'

export default [
  {path: '', component: Home},
  {path: '*', component: NotFound}
]
