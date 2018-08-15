<template>
  <v-toolbar :flat="flat" app dark dense scroll-off-screen tabs clipped-left :scroll-threshold="100" :color="color">
    <div style="width: 290px; display: flex">
      <v-toolbar-side-icon v-if="back" @click="$router.go(-1)">
        <v-icon>keyboard_arrow_left</v-icon>
      </v-toolbar-side-icon>
      <v-toolbar-side-icon v-else @click.stop="showDrawer()"></v-toolbar-side-icon>
      <!--
      <v-btn flat icon :to="{ name: 'home' }" color="transparent">
        <v-avatar>
          <img :src="logo" alt="Logo" style="margin-top: -3px; z-index: 1">
        </v-avatar>
      </v-btn>
      <v-toolbar-title class="ml-0 pl-0 hnc-title" style="font-size: 2em; padding-bottom: 5px">
        Hack'n'Cast
      </v-toolbar-title>
        -->
    </div>

    <v-breadcrumbs class="breadcrumbs--toolbar" v-show="$vuetify.breakpoint.smAndUp">
      <v-icon slot="divider">chevron_right</v-icon>
      <v-breadcrumbs-item v-for="item in breadcrumbs" :key="item.title">
        <template v-if="item.target">
          <router-link :to="item.target">
            <v-icon v-if="item.icon" :style="item.title ? 'margin-right: 5px' : ''">{{ item.icon }}</v-icon>
            <template v-if="item.title">{{ item.title }}</template>
          </router-link>
        </template>
        <template v-else>
          <v-icon v-if="item.icon" :style="item.title ? 'margin-right: 5px' : ''">{{ item.icon }}</v-icon>
          <template v-if="item.title">{{ item.title }}</template>
        </template>
      </v-breadcrumbs-item>
    </v-breadcrumbs>

    <v-spacer></v-spacer>

    <v-menu offset-y :close-on-content-click="false" :nudge-width="200" :nudge-left="210" v-model="menu">
      <v-btn flat dark icon slot="activator">
        <v-icon>account_circle</v-icon>
      </v-btn>
      <v-card>
        <v-list two-line class="py-0">
          <v-list-tile avatar @click="$router.push({ name: 'user-profile-account' }); menu = false">
            <v-list-tile-avatar>
              <!-- TODO: Add currentUser avatar -->
              <img :src="currentUser.avatar" :alt="currentUser.displayName">
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>{{ currentUser.displayName }}</v-list-tile-title>
              <v-list-tile-sub-title>{{ currentUser.email }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>

        <v-divider></v-divider>

        <v-list class="py-0">
          <v-list-tile>
            <v-list-tile-action>
              <v-switch v-model="darkTheme" color="blue darken-2"></v-switch>
            </v-list-tile-action>
            <v-list-tile-title>Dark Theme</v-list-tile-title>
            <v-list-tile-action style="margin-right: -30px">
              <v-btn flat icon color="grey" @click="showUiSettings"><v-icon>settings</v-icon></v-btn>
            </v-list-tile-action>
          </v-list-tile>

          <v-list-tile>
            <v-list-tile-action>
              <v-switch v-model="compactSidebar" color="blue darken-2"></v-switch>
            </v-list-tile-action>
            <v-list-tile-title>Compact Sidebar</v-list-tile-title>
          </v-list-tile>
        </v-list>

        <v-divider></v-divider>

        <v-card-actions>
          <v-btn flat @click="menu = false">Close</v-btn>
          <v-spacer></v-spacer>
          <v-btn flat color="red darken-2" @click="doLogout" :loading="loading">Logout <v-icon right>exit_to_app</v-icon></v-btn>
        </v-card-actions>
      </v-card>
    </v-menu>

    <slot slot="extension"></slot>
</v-toolbar>
</template>

<script>
import { mapGetters, mapActions, mapState } from 'vuex'

export default {
  data: () => ({
    menu: false,
    loading: false
  }),

  props: {
    flat: { type: Boolean, default: false },
    back: { type: Boolean, default: false }
  },

  computed: {
    ...mapGetters({
      currentUser: 'auth/currentUser',
      color: 'ui/navbarColor'
    }),

    ...mapState({
      breadcrumbs: state => state.ui.breadcrumbs
    }),

    darkTheme: {
      get () { return this.$store.state.ui.darkTheme },
      set (val) { this.setDarkTheme(val) }
    },

    compactSidebar: {
      get () { return this.$store.state.ui.miniSidebar },
      set (val) { this.setMiniSidebar(val) }
    },

    logo () {
      if (this.$store.state.ui.darkTheme) {
        return require('@/assets/hnc-logo-noframe-inverted.svg')
      } else {
        return require('@/assets/hnc-logo-noframe.svg')
      }
    }
  },

  methods: {
    ...mapActions({
      logout: 'auth/logout',
      setDarkTheme: 'ui/setDarkTheme',
      setMiniSidebar: 'ui/setMiniSidebar'
    }),

    showDrawer () { this.$store.dispatch('ui/showSidebar', true) },

    // TODO: Add the Ui Settings back
    showUiSettings () {
      this.menu = false
      this.$store.state.ui.uiSettingsVisible = true
    },

    doLogout () {
      this.loading = true
      this.logout()
        .then(data => {
          this.menu = false
          this.$router.push({ name: 'auth-login' })
        })
        .catch(err => { console.log('err', err) })
        .finally(() => { this.loading = false })
    }
  }
}
</script>

<style lang="scss">
.breadcrumbs--toolbar {
  font-weight: 500;
  flex-flow: row !important;
  text-transform: uppercase;
  overflow: scroll;

  .v-breadcrumbs__item, .v-breadcrumbs__item i {
    color: rgba(255, 255, 255, .7);
  }

  li:last-child .v-breadcrumbs__item {
    color: rgba(255, 255, 255, 1) !important;
  }

  li {
    flex: 1;
  }

}
</style>
