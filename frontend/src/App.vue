<template>
  <v-app :dark="$store.state.ui.darkTheme" id="app" :class="backgroundColor">
    <vue-topprogress color="#90CAF9" ref="progress"></vue-topprogress>

    <transition :name="transitionName" mode="out-in">
      <layout-broker :layouts="layouts" :current="$route.meta.layout"/>
    </transition>

    <toast />
    <form-errors />
    <ui-settings-dialog />
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex'
import layouts from '@/layouts'
import Toast from '@/plugins/toast/Toast'
import LayoutBroker from 'vue-layout-broker'
import UiSettingsDialog from '@/components/UiSettings'
import FormErrors from '@/plugins/formerrors/FormErrors'

export default {
  name: 'App',

  components: { LayoutBroker, Toast, FormErrors, UiSettingsDialog },

  head: {
    meta () {
      return [
        { name: 'theme-color', content: this.chromeColor }
      ]
    }
  },

  data () {
    return {
      transitionName: '',
      layouts
    }
  },

  computed: {
    ...mapGetters({
      progressStatus: 'ui/progressBarStatus',
      chromeColor: 'ui/chromeColor',
      backgroundColor: 'ui/backgroundColor'
    })
  },

  watch: {
    chromeColor (to, from) { this.$emit('updateHead') },

    '$route' (to, from) {
      let fromAuth = false
      let toAuth = false

      if (from.meta.middlewares) { fromAuth = from.meta.middlewares.some(name => name === 'PrivateOnly') }
      if (to.meta.middlewares) { toAuth = to.meta.middlewares.some(name => name === 'PrivateOnly') }

      if (fromAuth !== toAuth) {
        this.transitionName = 'slide-fade'
      } else {
        this.transitionName = ''
      }
    },

    progressStatus (to, from) {
      if (to === 'fail') {
        setTimeout(() => { this.$refs.progress.fail() }, 500)
      } else if (to === 'start' && from !== 'start') {
        this.$refs.progress.start()
      } else if (to === 'stop' && from !== 'stop') {
        setTimeout(() => { this.$refs.progress.done() }, 500)
      }
    }
  },

  created () {
    this.$router.beforeEach((to, from, next) => {
      this.$store.dispatch('ui/startProgressBar')
      setTimeout(() => { next() }, 250)
    })

    this.$router.afterEach((to, from) => {
      this.$store.dispatch('ui/endProgressBar')
    })
  }
}
</script>
