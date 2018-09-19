<template>
  <v-snackbar
    bottom
    v-model="toastVisible"
    :timeout="toast.timeout"
    :color="toast.color"
    :multi-line="toast.text && toast.text.length >= 60"
    >
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
