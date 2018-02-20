<template>
  <v-app id="inspire">
    <v-toolbar color="blue-grey darken-4" dark app :clipped-left="$vuetify.breakpoint.mdAndUp" fixed>
      <v-toolbar-title style="width: 300px" class="ml-0 pl-3">
        <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
        <span class="text-md-left text-sm-center">Administration</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>

    <v-navigation-drawer dark class="blue-grey darken-2" fixed :clipped="$vuetify.breakpoint.mdAndUp" app :mini-variant.sync="mini"  value="true" v-model="drawer">
        <v-list class="pa-0 blue-grey darken-3">
          <v-list-tile avatar>
            <v-list-tile-avatar>
              <img :src="currentUser.avatar" >
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>{{ currentUser.displayName }}</v-list-tile-title>
            </v-list-tile-content>
            <v-list-tile-action>
              <v-btn icon @click.native.stop="mini = !mini">
                <v-icon>chevron_left</v-icon>
              </v-btn>
            </v-list-tile-action>
          </v-list-tile>
        </v-list>

      <v-list class="pt-0" dense>
        <v-divider></v-divider>
        <v-list-tile v-for="item in items" :key="item.title" @click="">
          <v-list-tile-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>{{ item.title }}</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <li>
          <v-bottom-nav absolute :value="true" color="blue-grey darken-2" style="box-shadow: unset;">
            <v-btn v-show="!mini">
              <span>Settings</span>
              <v-icon>settings</v-icon>
            </v-btn>
            <v-btn @click.native.stop="logout">
              <span>Logout</span>
              <v-icon>exit_to_app</v-icon>
            </v-btn>
          </v-bottom-nav>
        </li>
      </v-list>
    </v-navigation-drawer>

    <v-content>
      <v-container fluid fill-height>
        <v-layout justify-center align-center>
          <transition name="fade" mode="out-in">
            <router-view />
          </transition>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  data: () => ({
    mini: true,
    dialog: false,
    drawer: null,
    items: [
      { title: 'Home', icon: 'dashboard' },
      { title: 'About', icon: 'question_answer' }
    ]
  }),

  computed: {
    ...mapGetters(['currentUser'])
  },

  props: {
    source: String
  },

  methods: {
    logout () {
      console.log('logout')
    }
  }
}
</script>
