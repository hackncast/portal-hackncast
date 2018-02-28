import Vue from 'vue'
import Router from 'vue-router'
import { store } from '@/store/store'

import Inside from '@/pages/layouts/Inside'
import UserRoutes from '@/router/user'
import HelloWorld from '@/components/HelloWorld'

Vue.use(Router)

let router = new Router({
  scrollBehavior (to, from, savedPosition) {
    return { x: 0, y: 0 }
  },
  routes: Array.concat(
    [
      {
        path: '/',
        component: Inside,
        meta: { requiresAuth: true },
        children: [
          {path: '', name: 'home', component: HelloWorld}
        ]
      }
    ],
    UserRoutes
  )
})

router.beforeEach((to, from, next) => {
  if (to.name === '404' || to.meta.mayRequiresAuth) {
    next()
    return
  }

  store.dispatch('checkStoredLogin')
    .then(data => {
      if (to.matched.some(record => record.meta.requiresAuth)) {
        next()
      } else {
        next({ name: 'home' })
      }
    })
    .catch(err => {
      if (to.matched.some(record => record.meta.requiresAuth)) {
        next({ name: 'user:login', query: {next: to.path} })
      } else {
        next()
      }
      return err
    })
})

export default router
