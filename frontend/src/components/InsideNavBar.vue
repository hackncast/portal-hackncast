<template>
  <v-toolbar app dark dense scroll-off-screen tabs :scroll-threshold="100" :color="color">
  <v-toolbar-side-icon @click.stop="showDrawer()"></v-toolbar-side-icon>
  <v-spacer></v-spacer>
  <v-btn flat icon :to="{ name: 'home' }" color="transparent">
    <v-avatar>
      <img :src="logo" alt="Logo" style="margin-top: -3px; z-index: 1">
    </v-avatar>
  </v-btn>
  <v-toolbar-title class="ml-0 pl-0 hnc-title" style="font-size: 2em; padding-bottom: 5px">
    Hack'n'Cast
  </v-toolbar-title>
  <v-spacer></v-spacer>
  <v-menu offset-y :close-on-content-click="false" :nudge-width="200" :nudge-left="210" v-model="menu">
    <v-btn flat dark icon slot="activator">
      <v-icon>account_circle</v-icon>
    </v-btn>
    <v-card>
      <v-list two-line class="py-0">
        <v-list-tile avatar @click="$router.push({ name: 'user:profile' }); menu = false">
          <v-list-tile-avatar>
            <img :src="currentUser.avatar" :alt="currentUser.displayName">
          </v-list-tile-avatar>
          <v-list-tile-content>
            <v-list-tile-title>{{ currentUser.displayName }}</v-list-tile-title>
            <v-list-tile-sub-title>{{ currentUser.email }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>

      <v-divider></v-divider>

      <v-list>
        <v-list-tile>
          <v-list-tile-action>
            <v-switch v-model="darkTheme" color="blue darken-2"></v-switch>
          </v-list-tile-action>
          <v-list-tile-title>Dark Theme</v-list-tile-title>
        </v-list-tile>
      </v-list>

      <v-divider></v-divider>

      <v-card-actions>
        <v-btn flat @click="menu = false">Close</v-btn>
        <v-spacer></v-spacer>
        <v-btn color="red darken-2" flat @click="doLogout" :loading="working">Logout <v-icon right>exit_to_app</v-icon></v-btn>
      </v-card-actions>
    </v-card>
  </v-menu>

  <slot slot="extension" />
</v-toolbar>
</template>

<script>
import { UI } from '@/store/mutation-types'
import { mapGetters, mapActions, mapMutations } from 'vuex'

export default {
  data: () => ({
    menu: false,
    working: false
  }),

  props: {
    color: { type: String }
  },

  computed: {
    ...mapGetters(['currentUser']),

    darkTheme: {
      get () {
        return this.$store.state.Ui.darkTheme
      },
      set (val) {
        this.setDarkTheme(val)
      }
    },

    logo () {
      if (this.$store.state.Ui.darkTheme) {
        return require('@/assets/hnc-logo-noframe-inverted.svg')
      } else {
        return require('@/assets/hnc-logo-noframe.svg')
      }
    }
  },

  methods: {
    ...mapActions(['logout']),
    ...mapMutations({
      setDarkTheme: UI.DARK_THEME
    }),

    showDrawer () {
      this.$store.state.Ui.sidebarVisible = true
    },

    doLogout () {
      this.working = true
      this.logout()
        .then(data => this.$router.push({ name: 'user:login' }))
        .catch(err => { console.log('err', err) })
        .finally(() => { this.working = false })
    }
  }
}
</script>
