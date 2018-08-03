import Vue from 'vue'
import Router from 'vue-router'

const routes = []
const requireModule = require.context('.', false, /\.js$/)

requireModule.keys().forEach(fileName => {
  if (fileName === './index.js') return

  let module = requireModule(fileName)
  let base = module.base ? `/${module.base}` : ''
  module.default.map(r => {
    if (base) { r.path = base + r.path }

    if (!r.component.route) { throw Error('The page must define a route name!') }

    routes.push({
      path: r.path,
      name: r.component.route,
      component: r.component,
      meta: {
        layout: r.component.layout ? r.component.layout : ''
      }
    })
  })
})

Vue.use(Router)

export default new Router({
  base: process.env.BASE_URL ? process.env.BASE_URL : undefined,
  mode: 'history',
  routes: Array.concat(routes)
})
