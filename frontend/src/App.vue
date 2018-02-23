<template>
  <div>
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
      if (from.name !== null) {
        this.transitionName = 'slide-fade'
      }
    }
  }
}
</script>
