<template>
  <v-app :dark="$store.state.Ui.darkTheme" id="app" :class="backgroundColor">
    <vue-topprogress color="#90CAF9" ref="progress"></vue-topprogress>

    <transition :name="transitionName" mode="out-in">
      <layout-broker :layouts="layouts" :current="$route.meta.layout"/>
    </transition>

    <unconfirmed-email-dialog/>
    <ui-settings-dialog/>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex'
import layouts from '@/layouts'
import LayoutBroker from 'vue-layout-broker'
import UiSettingsDialog from '@/components/dialog/UiSettings'
import UnconfirmedEmailDialog from '@/components/dialog/UnconfirmedEmail'

export default {
  name: 'App',

  components: { LayoutBroker, UiSettingsDialog, UnconfirmedEmailDialog },

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
      chromeColor: 'getChromeColor',
      currentUser: 'currentUser'
    }),

    backgroundColor () {
      return this.$store.state.Ui.backgroundColor
    },

    progressStatus () {
      return this.$store.state.Ui.progressStatus
    }
  },

  watch: {
    chromeColor (to, from) { this.$emit('updateHead') },

    '$route' (to, from) {
      let fromAuth = from.matched.some(record => record.meta.requiresAuth)
      let toAuth = to.matched.some(record => record.meta.requiresAuth)

      if (fromAuth !== toAuth) {
        this.transitionName = 'slide-fade'
      } else {
        this.transitionName = ''
      }
    },

    progressStatus (to, from) {
      if (to === 'fail') {
        this.$refs.progress.fail()
      } else if (to === 'start' && from !== 'start') {
        this.$refs.progress.start()
      } else if (to === 'stop' && from !== 'stop') {
        this.$refs.progress.done()
      }
    }
  }
}
</script>
