<template>
<v-toolbar app dark dense fixed clipped-left complex color="blue-grey darken-4">
  <v-toolbar-title style="width: 300px" class="ml-0 pl-3">
    <v-toolbar-side-icon @click.stop=""></v-toolbar-side-icon>
  </v-toolbar-title>
  <v-spacer></v-spacer>
  <v-menu offset-y :close-on-content-click="false" :nudge-width="200" :nudge-bottom="6" :nudge-left="210" v-model="menu">
    <v-btn flat dark icon slot="activator">
      <v-icon>account_circle</v-icon>
    </v-btn>
    <v-card>
      <v-list>
        <v-list-tile avatar>
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
      <v-card-actions>
        <v-btn flat @click="menu = false">Close</v-btn>
        <v-spacer></v-spacer>
        <v-btn color="red darken-2" flat @click="doLogout" :loading="working">Logout <v-icon right>exit_to_app</v-icon></v-btn>
      </v-card-actions>
    </v-card>
  </v-menu>
</v-toolbar>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  data: () => ({
    menu: false,
    working: false
  }),

  computed: {
    ...mapGetters(['currentUser'])
  },

  methods: {
    ...mapActions(['logout']),

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
