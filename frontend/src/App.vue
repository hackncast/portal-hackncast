<template>
  <div id="main">
    <vue-progress-bar></vue-progress-bar>
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

  watch: {
    '$route' (to, from) {
      let fromAuth = from.matched.some(record => record.meta.requiresAuth)
      let toAuth = to.matched.some(record => record.meta.requiresAuth)

      if (fromAuth !== toAuth) {
        this.transitionName = 'slide-fade'
      } else {
        this.transitionName = ''
      }
    }
  }
}
</script>
