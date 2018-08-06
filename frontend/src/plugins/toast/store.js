import Vue from 'vue'

export default {
  namespaced: true,

  state: {
    toasts: [],
    toast: {},
    toastVisible: false,
    nonFieldErrors: []
  },

  getters: {
    currentToast: (state) => { return state.toast }
  },

  mutations: {
    SET_TOAST_VISIBILITY (state, value) {
      state.toastVisible = value
    },

    PROCESS_TOAST_QUEUE (state) {
      if (state.toasts.length <= 0) return
      if (state.toastVisible) return

      let toast = state.toasts.splice(0, 1)[0]
      Vue.set(state, 'toast', toast)
      state.toastVisible = true
    },

    PUSH_TOAST (state, toast) {
      state.toasts.push(toast)
    },

    SET_NONFIELD_ERRORS (state, errors) {
      errors.forEach(err => state.nonFieldErrors.push(err))
    },

    CLEAR_NONFIELD_ERRORS (state) {
      state.nonFieldErrors.splice(0, state.nonFieldErrors.length)
    }
  },

  actions: {
    toastErrors ({commit}, errors) {
      commit('CLEAR_NONFIELD_ERRORS')
      if (errors) {
        commit('SET_NONFIELD_ERRORS', errors)
      }
    },

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
        commit('PROCESS_TOAST_QUEUE')
        resolve()
      })
    },

    showToast ({commit}, val) {
      return new Promise((resolve, reject) => {
        commit('SET_TOAST_VISIBILITY', val)
        setTimeout(() => {
          commit('PROCESS_TOAST_QUEUE')
        }, 700)
        resolve()
      })
    }
  }
}
