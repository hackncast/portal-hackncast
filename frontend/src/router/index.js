import Vue from 'vue'
import Router from 'vue-router'
import { store } from '@/store/store'
import { UI } from '@/store/mutation-types'

const routes = []
const requireModule = require.context('.', false, /\.js$/)

requireModule.keys().forEach(fileName => {
  if (fileName === './index.js') return

  routes.push(requireModule(fileName).default)
})

Vue.use(Router)

let router = new Router({
  scrollBehavior (to, from, savedPosition) {
    return { x: 0, y: 0 }
  },
  routes: Array.concat(...routes)
})

router.afterEach((to, from, next) => {
  setTimeout(() => {
    store.commit(UI.PROGRESS_STOP)
  }, 250)
})

router.beforeEach((to, from, next) => {
  store.commit(UI.PROGRESS_START)
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
