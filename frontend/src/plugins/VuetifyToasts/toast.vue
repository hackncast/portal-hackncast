<template>
  <v-snackbar right bottom v-model="open" v-bind="options">
    <div class="ctn">
      <div class="title mb-2" style="font-size: 16px !important" v-if="title">{{ title }}</div>
      <div class="txt" :class="type === 'warning' ? 'black--text' : ''">{{ text }}</div>
    </div>
    <div class="text-xs-right">
      <v-btn flat v-for="action in actions" :key="action.name" :style="closeBtnStyle" :color="action.color" @click.native="action.callback()">{{ action.name }}</v-btn>
      <v-btn flat v-if="options.closeable" :style="closeBtnStyle" :color="type ? (type === 'warning' ? 'black' : 'white') : 'red'" @click.native="open = false">Close</v-btn>
    </div>
  </v-snackbar>
</template>

<script>
export default {
  name: 'VuetifyToast',

  props: {
    title: String,
    text: String,
    type: String,
    options: Object,
    actions: Array
  },

  data () {
    return {
      open: false
    }
  },

  watch: {
    open: function (val) {
      if (!val) {
        this.close()
      }
    }
  },

  computed: {
    closeBtnStyle () {
      return this.options.vertical ? 'margin-left: 10px; margin-top: 5px; flex: 0;' : 'flex: 0;'
    }
  },

  methods: {
    close () {
      if (this.open) this.open = false
      setTimeout(() => {
        this.$options.onClose()
        this.$destroy()
        removeElement(this.$el)
      }, 700) // wait for close animation
    }
  },

  beforeMount () {
    document.querySelector('#app').appendChild(this.$el)
  },

  mounted () {
    this.open = true
  }
}

function removeElement (el) {
  if (typeof el.remove !== 'undefined') {
    el.remove()
  } else {
    el.parentNode.removeChild(el)
  }
}
</script>

<style scoped>
@media (min-width: 600px) {
  .snack__wrapper {
    max-width: 45%
  }
}

@media (min-width: 1264px) {
  .snack__wrapper {
    max-width: 25%
  }
}
</style>
