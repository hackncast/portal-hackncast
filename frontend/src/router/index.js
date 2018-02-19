import { store } from '@/store/store'

import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Registration from '@/pages/user/Registration'

Vue.use(Router)

let router = new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: HelloWorld,
      meta: { requiresAuth: true }
    },
    {
      path: '/user/registration',
      name: 'user:registration',
      component: Registration
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.name === '404') {
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
