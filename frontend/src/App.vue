<template>
  <div id="main">
    <vue-topprogress color="#90CAF9" ref="progress"></vue-topprogress>
    <transition :name="transitionName" mode="out-in">
      <router-view/>
    </transition>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'App',

  head: {
    meta () {
      return [
        { name: 'theme-color', content: this.chromeColor }
      ]
    }
  },

  data () {
    return {
      transitionName: ''
    }
  },

  computed: {
    ...mapGetters({ chromeColor: 'getChromeColor' }),

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
