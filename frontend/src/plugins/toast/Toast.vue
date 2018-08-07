<template>
  <v-snackbar v-model="toastVisible" bottom :timeout="toast.timeout" :color="toast.color">
    {{ toast.text }}
    <v-btn :color="toast.closeColor" flat @click="toastVisible = false" >
      Fechar
    </v-btn>
  </v-snackbar>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters({
      toast: 'toast/currentToast'
    }),

    toastVisible: {
      get () { return this.$store.state.toast.visible },
      set (val) { this.$store.dispatch('toast/show', val) }
    }
  }
}
</script>
