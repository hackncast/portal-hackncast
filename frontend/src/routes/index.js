import Vue from 'vue'
import Router from 'vue-router'
import middlewares from '@/middlewares'

Vue.use(Router)

const routes = []
const requireModule = require.context('.', false, /\.js$/)

requireModule.keys().forEach(fileName => {
  if (fileName === './index.js') return

  let module = requireModule(fileName)
  let base = module.base ? `/${module.base}` : ''
  module.default.map(r => {
    if (base) { r.path = base + r.path }

    if (!r.component.route || !r.component.route.name) {
      console.error(`The page '${r.component.__file}' does not define a route name!`)
    }

    routes.push({
      path: r.path,
      name: r.component.route.name,
      component: r.component,
      meta: { layout: r.component.route.layout ? r.component.route.layout : '' },
      beforeEnter: (to, from, next) => {
        if (!r.component.route.middlewares) {
          return next()
        }

        r.component.route.middlewares.forEach(middlewareName => {
          if (middlewares.hasOwnProperty(middlewareName)) {
            middlewares[middlewareName](to, from, (routeObj) => next(routeObj))
          } else {
            console.warn(`Middleware defined at '${r.component.__file}' not found:`, middlewareName)
          }
        })
      }
    })
  })
})

export default new Router({
  mode: 'history',
  routes: routes,
  base: process.env.BASE_URL ? process.env.BASE_URL : undefined
})
