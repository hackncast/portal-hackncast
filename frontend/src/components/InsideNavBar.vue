<template>
<v-toolbar app dark dense fixed clipped-left complex color="blue-grey darken-4">
  <v-toolbar-title style="width: 300px" class="ml-0 pl-3">
    <v-toolbar-side-icon @click.stop=""></v-toolbar-side-icon>
  </v-toolbar-title>
  <v-spacer></v-spacer>
  <v-toolbar-items class="">
    <v-menu offset-y :close-on-content-click="false" :nudge-width="200" :nudge-bottom="5" :nudge-left="200" v-model="menu">
      <v-btn flat dark slot="activator">
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
          <v-btn color="red darken-2" flat @click="">Logout <v-icon right>exit_to_app</v-icon></v-btn>
        </v-card-actions>
      </v-card>
    </v-menu>
  </v-toolbar-items>
</v-toolbar>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data: () => ({
    menu: false
  }),

  computed: {
    ...mapGetters(['currentUser'])
  }
}
</script>
