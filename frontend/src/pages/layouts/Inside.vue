<template>
  <v-app :dark="darkTheme" id="app">
    <inside-nav-bar :color="navBarColor">
        <router-view name="navbarExtend" :color="navBarColor" :sliderColor="navSliderColor"/>
    </inside-nav-bar>

    <side-bar/>

    <v-content>
      <v-container fluid fill-height :class="backgroundColor">
        <v-layout justify-center align-center>
          <transition name="fade" mode="out-in">
            <router-view />
          </transition>
        </v-layout>
      </v-container>
    </v-content>

    <v-dialog v-if="!currentUser.verifiedEmail" :value="loaded && !currentUser.verifiedEmail" persistent max-width="350">
      <v-card>
        <v-card-title class="headline">Oops... Have you confirmed your email?</v-card-title>
        <v-card-text>
          <p>In order to enjoy all our site features, we request you to confirm the ownership of the following email address:</p>
          <ul style="margin-left: 2em; margin-bottom: 1.5em">
            <li>{{ currentUser.safeEmailAddress }}</li>
          </ul>
          <p>Please, check your inbox and SPAM box. If there is no email, please click below...</p>
        </v-card-text>
        <v-card-actions>
          <v-btn flat color="green darken-1" v-if="!checkAgain" @click="doResend" :loading="resendWorking">Send-me Again...</v-btn>
          <v-btn flat color="green darken-1" v-else @click="doCheckAgain" :loading="resendWorking">Check Validation...</v-btn>
          <v-spacer></v-spacer>
          <v-btn flat color="red darken-1" @click="doLogout" :loading="logoutWorking">Logout</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import SideBar from '@/components/SideBar'
import InsideNavBar from '@/components/InsideNavBar'

export default {
  components: {InsideNavBar, SideBar},

  data: () => ({
    loaded: false,
    checkAgain: false,
    logoutWorking: false,
    resendWorking: false
  }),

  computed: {
    ...mapGetters(['currentUser']),

    darkTheme () {
      return this.$store.state.Ui.darkTheme
    },

    navBarColor () {
      return this.darkTheme ? 'blue-grey darken-4' : 'blue accent-2'
    },

    navSliderColor () {
      return this.darkTheme ? 'blue lighten-2' : 'blue lighten-4'
    },

    backgroundColor () {
      return this.darkTheme ? 'darkBackground' : 'grey lighten-3'
    }
  },

  methods: {
    ...mapActions(['logout', 'fetchUserData']),

    doResend () {
      this.resendWorking = true
      setTimeout(() => {
        this.$http.post(`/api/user/email/${this.currentUser.pkEmail}/send_confirmation`)
          .then(data => {
            this.checkAgain = true
            this.resendWorking = false
          })
          .catch(err => {
            this.resendWorking = false
            console.log('err', err)
          })
      }, 500)
    },

    doCheckAgain () {
      this.resendWorking = true
      setTimeout(() => {
        this.fetchUserData()
          .then(user => user)
          .catch(err => console.log(err))
          .finally(() => {
            this.resendWorking = false
            this.checkAgain = false
          })
      }, 500)
    },

    doLogout () {
      this.logoutWorking = true
      this.logout()
        .then(data => this.$router.push({ name: 'user:login' }))
        .catch(err => { console.log(err) })
        .finally(() => { this.logoutWorking = false })
    }
  },

  mounted () {
    setTimeout(() => {
      this.loaded = true
    }, 250)
  }
}
</script>

<style scoped>
.darkBackground {
  background-color: #303030 !important;
}
</style>
