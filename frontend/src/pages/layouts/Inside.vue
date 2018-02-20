<template>
  <v-app id="inspire">
    <inside-nav-bar />
    <v-navigation-drawer dark class="blue-grey darken-2" fixed :clipped="$vuetify.breakpoint.mdAndUp" app :mini-variant.sync="mini"  value="true" v-model="drawer">
      <v-list class="pa-0 blue-grey darken-3">
        <v-list-tile avatar>
          <v-list-tile-avatar>
            <img src="@/assets/hnc-logo-noframe-inverted.svg" alt="Logo" style="margin-top: -3px">
          </v-list-tile-avatar>
          <v-list-tile-content>
            <v-list-tile-title>Portal Hack 'n' Cast</v-list-tile-title>
            <v-list-tile-sub-title>Administration</v-list-tile-sub-title>
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
import InsideNavBar from '@/components/InsideNavBar'

export default {
  components: {InsideNavBar},

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
