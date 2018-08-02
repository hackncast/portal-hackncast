import axios from 'axios'
import Vuetify from 'vuetify'
import VueHead from 'vue-head'
import VueAxios from 'vue-axios'
import VueMoment from 'vue-moment'
import TopProgress from 'vue-top-progress'

export default {
  install (vue) {
    vue.use(VueHead)
    vue.use(Vuetify)
    vue.use(VueMoment)
    vue.use(TopProgress)
    vue.use(VueAxios, axios)
  }
}
