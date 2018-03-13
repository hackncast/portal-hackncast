<template>
  <v-app :dark="darkTheme" id="app" :class="backgroundColor">
    <inside-nav-bar flat />

    <side-bar/>

    <v-content>
      <v-container fluid :class="$store.state.Ui.navbarColor" class="pb-0 px-0 elevation-2">
        <v-flex xs12 sm6 offset-sm3 md4 offset-md4>
          <v-layout align-center justify-center style="">
            <v-avatar size="120px" class="elevation-2">
              <img :src="currentUser.avatar" :alt="currentUser.displayName">
              <v-btn fab absolute dark small class="elevation-3" color="blue" style="bottom: 0px; left: 80px;" @click="notYet">
                <v-icon dark>edit</v-icon>
              </v-btn>
            </v-avatar>
          </v-layout>
          <v-layout row justify-space-around text-xs-center>
            <v-flex xs3>
              <div class="body-2 text--lighten-4" :class="textColor">1</div>
              <div class="caption text--lighten-3" :class="textColor">LEVEL</div>
            </v-flex>
            <v-flex xs3>
              <div class="body-2 text--lighten-4" :class="textColor">0</div>
              <div class="caption text--lighten-3" :class="textColor">EXPERIENCE</div>
            </v-flex>
          </v-layout>
        </v-flex>
        <v-tabs fixed-tabs icons-and-text show-arrows color="transparent" dark slider-color="yellow" class="pt-2" style="padding-bottom: 2.8em">
          <v-tab ripple :to="{ name: 'user:profile' }">Account <v-icon>account_box</v-icon></v-tab>
          <v-tab ripple :to="{ name: 'user:profile:emails' }">Emails <v-icon>email</v-icon></v-tab>
          <v-tab ripple :to="{ name: 'user:profile:security' }">Security <v-icon>security</v-icon></v-tab>
        </v-tabs>
      </v-container>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex'
import SideBar from '@/components/SideBar'
import InsideNavBar from '@/components/InsideNavBar'

export default {
  components: {InsideNavBar, SideBar},

  data: () => ({
  }),

  computed: {
    ...mapGetters(['currentUser']),

    darkTheme () {
      return this.$store.state.Ui.darkTheme
    },

    navbarColor () {
      return this.$store.state.Ui.navbarColor
    },

    backgroundColor () {
      return this.$store.state.Ui.backgroundColor
    },

    textColor () {
      return this.darkTheme ? 'blue-grey--text' : 'blue--text'
    }
  },

  methods: {
    notYet () {
      this.$toasts.open({text: 'Sorry, not working yet...'})
    }
  }
}
</script>
