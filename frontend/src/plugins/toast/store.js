import Vue from 'vue'

export default {
  namespaced: true,

  state: {
    all: [],
    current: {},
    visible: false
  },

  getters: {
    currentToast: (state) => { return state.current }
  },

  mutations: {
    SET_VISIBILITY (state, value) {
      state.visible = value
    },

    PROCESS_QUEUE (state) {
      if (state.all.length <= 0) return
      if (state.visible) return

      let toast = state.all.splice(0, 1)[0]
      Vue.set(state, 'current', toast)
      state.visible = true
    },

    PUSH_TOAST (state, toast) {
      state.all.push(toast)
    }
  },

  actions: {
    toast ({commit}, toast) {
      if (!toast.closeColor) {
        if (toast.color === 'error') {
          toast.closeColor = 'white'
        }
      }
      toast = Object.assign({
        color: '',
        closeText: 'Fechar',
        closeColor: 'red',
        timeout: 6000,
        actions: null,
        onClose: null
      }, toast)

      return new Promise((resolve, reject) => {
        commit('PUSH_TOAST', toast)
        commit('PROCESS_QUEUE')
        resolve()
      })
    },

    show ({commit}, val) {
      return new Promise((resolve, reject) => {
        commit('SET_VISIBILITY', val)
        setTimeout(() => { commit('PROCESS_QUEUE') }, 700)
        resolve()
      })
    }
  }
}
