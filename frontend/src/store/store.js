import Vue from 'vue'
import Vuex from 'vuex'

import Ui from '@/store/modules/ui'
import User from '@/store/modules/user'

Vue.use(Vuex)

export const store = new Vuex.Store({
  modules: {
    Ui,
    User
  }
})
