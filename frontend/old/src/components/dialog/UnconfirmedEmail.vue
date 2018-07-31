<template>
  <v-dialog v-if="visible" :value="loaded && visible" persistent max-width="350">
    <v-card>
      <v-card-title class="headline">{{ $t('dialog.unverified-email.title')  }}</v-card-title>
      <v-card-text>
        <p style="text-align: justify">{{ $t('dialog.unverified-email.text') }}</p>
        <ul style="margin-left: 2em; margin-bottom: 1.5em">
          <li>{{ currentUser.safeEmailAddress }}</li>
        </ul>
        <p style="text-align: justify">{{ $t('dialog.unverified-email.spam-alert') }}</p>
      </v-card-text>
      <v-card-actions>
        <v-btn flat color="green darken-1" v-if="!checkAgain" @click="doResend" :loading="resendWorking">{{ $t('label.send-me-again') }}</v-btn>
        <v-btn flat color="green darken-1" v-else @click="doCheckAgain" :loading="resendWorking">{{ $t('label.check-validation') }}</v-btn>
        <v-spacer></v-spacer>
        <v-btn flat color="red darken-1" @click="doLogout" :loading="logoutWorking">{{ $t('label.logout') }}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'UnconfirmedEmailDialog',

  data () {
    return {
      loaded: false,
      checkAgain: false,
      logoutWorking: false,
      resendWorking: false
    }
  },

  computed: {
    ...mapGetters({
      currentUser: 'currentUser'
    }),

    visible () {
      if (!this.currentUser.isAuthenticated) {
        return false
      }
      if (!this.$route.matched.some(record => record.meta.requiresAuth)) {
        return false
      }

      return !this.currentUser.verifiedEmail
    }
  },

  watch: {
    currentUser (to, from) {
      if (to.isAuthenticated) {
        setTimeout(() => {
          this.loaded = true
        }, 550)
      } else {
        this.loaded = false
      }
    }
  },

  methods: {
    ...mapActions(['logout', 'fetchUserData']),

    doResend () {
      this.resendWorking = true
      setTimeout(() => {
        this.$http.post(`/api/user/email/${this.currentUser.pkEmail}/send_confirmation/`)
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
          .then(user => {
            if (!user.verifiedEmail) {
              this.$toasts.open({ text: this.$t('message.email-not-confirmed') })
            }
          })
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
  }
}
</script>
