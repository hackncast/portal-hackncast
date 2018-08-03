import Vue from 'vue'
import axios from 'axios'
import Vuetify from 'vuetify'
import VueHead from 'vue-head'
import VueAxios from 'vue-axios'
import VueMoment from 'vue-moment'
import TopProgress from 'vue-top-progress'

Vue.use(VueHead)
Vue.use(Vuetify)
Vue.use(VueMoment)
Vue.use(Vuetify, {})
Vue.use(TopProgress)
Vue.use(VueAxios, axios)
