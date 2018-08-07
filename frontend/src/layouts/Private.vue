<template>
  <v-app :dark="$store.state.ui.darkTheme" id="app">
    <slot />
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'PrivateLayout',

  computed: {
    ...mapGetters({
    })
  }
}
</script>
