<template>
  <div id="main">
    <vue-topprogress color="#90CAF9" ref="progress"></vue-topprogress>
    <transition :name="transitionName" mode="out-in">
      <router-view/>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'App',

  data () {
    return {
      transitionName: ''
    }
  },

  computed: {
    progressStatus () {
      return this.$store.state.Ui.progressStatus
    }
  },

  watch: {
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
