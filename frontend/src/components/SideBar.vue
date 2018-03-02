<template>
  <v-navigation-drawer temporary v-model="drawer" absolute>
    <v-list class="pa-1">
      <v-list-tile avatar tag="div">
        <v-list-tile-avatar>
          <img :src="currentUser.avatar" >
        </v-list-tile-avatar>
          <v-list-tile-content>
            <v-list-tile-title>{{ currentUser.displayName }}</v-list-tile-title>
          </v-list-tile-content>
          <v-list-tile-action>
              <v-btn icon @click.stop="drawer = !drawer">
              <v-icon>chevron_left</v-icon>
            </v-btn>
          </v-list-tile-action>
      </v-list-tile>
    </v-list>
    <v-list class="pt-0" dense>
      <v-divider light></v-divider>
      <v-list-tile v-for="item in items" :key="item.title" @click="">
        <v-list-tile-action>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title>{{ item.title }}</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters(['currentUser']),

    drawer: {
      get () { return this.$store.state.Ui.sidebarVisible },
      set (val) { this.$store.state.Ui.sidebarVisible = val }
    }
  },

  data () {
    return {
      items: [
        { title: 'Vaults', icon: 'https' },
        { title: 'Users', icon: 'people' },
        { title: 'Administration', icon: 'settings' }
      ]
    }
  }
}
</script>
