<template>
  <v-navigation-drawer temporary v-model="drawer" absolute>
    <v-list class="py-0">
      <v-list-tile avatar ripple tag="div" @click="$router.push({ name: 'user:profile' }); drawer = false">
        <v-list-tile-avatar>
          <img :src="currentUser.avatar" >
        </v-list-tile-avatar>
          <v-list-tile-content>
            <v-list-tile-title>{{ currentUser.displayName }}</v-list-tile-title>
            <v-list-tile-sub-title>{{ currentUser.email }}</v-list-tile-sub-title>
          </v-list-tile-content>
          <v-list-tile-action>
              <v-btn icon @click.stop="drawer = !drawer">
              <v-icon>chevron_left</v-icon>
            </v-btn>
          </v-list-tile-action>
      </v-list-tile>
      <v-list-tile id="sidebar-quick-btns">
        <v-btn flat block color="grey" class="ma-0"><v-icon left>color_lens</v-icon> {{ $t('label.ui') }}</v-btn>
        <v-btn flat block color="red darken-2" @click="doLogout" class="ma-0" :loading="working">{{ $t('label.logout') }} <v-icon right>exit_to_app</v-icon></v-btn>
      </v-list-tile>
    </v-list>
    <v-list class="pt-0" dense>
      <v-divider light></v-divider>
      <v-list-tile @click="push('home')">
        <v-list-tile-action>
          <v-icon>home</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title>{{ $t('label.home') }}</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
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
import { mapGetters, mapActions } from 'vuex'

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
      working: false,
      items: [
        { title: 'Vaults', icon: 'https' },
        { title: 'Users', icon: 'people' },
        { title: 'Administration', icon: 'settings' }
      ]
    }
  },

  methods: {
    ...mapActions(['logout']),
    push (name) {
      this.$router.push({ name })
      this.drawer = false
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

<style lang="sass">
#sidebar-quick-btns
  padding: 0px !important;
</style>
