import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const modules = {}
const requireModule = require.context('.', true, /\.js$/)

requireModule.keys().forEach(fileName => {
  if (fileName === './index.js') return

  let moduleName = fileName.replace(/^\.\//, '').replace(/\.js$/, '')
  const module = requireModule(fileName)
  modules[moduleName] = {
    namespaced: true,
    state: module.state(),
    getters: module.getters,
    mutations: module.mutations,
    actions: module.actions

  }
})

export default new Vuex.Store({ modules })
