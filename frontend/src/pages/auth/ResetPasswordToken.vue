<template>
<v-container fluid fill-height pt-1>
  <v-layout align-center justify-center style="z-index: 2">
    <v-flex xs12 sm6 md4>
      <v-card color="white" class="elevation-3" style="overflow: hidden">
        <v-card-title primary-title class="text-xs-center blue white--text" id="register-card-title">
          <transition name="delayed-fade" mode="out-in">
            <div key="registration" v-if="!sent" style="width: 100%">
              <h1 class="headline">Change Password</h1>
            </div>
            <div key="success" v-else style="width: 100%">
              <h1 class="headline">Thank You!</h1>
              <v-progress-linear :indeterminate="true" :active="true" height="2" color="blue darken-3" style="margin-bottom: 0px"/>
            </div>
          </transition>
        </v-card-title>
        <transition name="shrink" duration="500">
          <v-card-text v-show="!sent" v-model="valid">
            <v-form @submit.prevent="submit" ref="form">
              <v-text-field light label="New Password" name="new_password1" ref="new_password1" required autofocus
                            v-model="new_password1"
                            prepend-icon="lock"
                            v-validate="'required'"
                            data-vv-as="new password"
                            :error-messages="errors.collect('new_password1')"
                            :append-icon="showPassword ? 'visibility_off' : 'visibility'"
                            @click:append="() => (showPassword = !showPassword)"
                            :type="showPassword ? 'text' : 'password'"
                            >
              </v-text-field>

              <v-text-field light label="Confirm New Password" name="new_password2" ref="new_password2" required
                            v-model="new_password2"
                            v-validate="'required|confirmed:new_password1'"
                            prepend-icon="lock"
                            data-vv-as="confirm new password"
                            :error-messages="errors.collect('new_password2')"
                            :append-icon="showPassword ? 'visibility_off' : 'visibility'"
                            @click:append="() => (showPassword = !showPassword)"
                            :type="showPassword ? 'text' : 'password'"
                            >
              </v-text-field>

              <v-btn light block color="blue" class="white--text" :disabled="errors.any() || isNotValidated()" type="submit" :loading="loading">Change</v-btn>
            </v-form>
          </v-card-text>
        </transition>
      </v-card>

      <v-btn flat block small class="white--text mt-3" :to="{ name: 'auth-login' }">I Remebered My Password!</v-btn>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import { FormMixin } from '@/mixins/FormMixin'

export default {
  name: 'ResetPasswordToken',

  route: {
    name: 'auth-reset-password-token',
    layout: 'Public',
    middlewares: ['PublicOnly']
  },

  mixins: [FormMixin],

  data () {
    return {
      supressNonFieldErrors: true,
      valid: false,
      showPassword: false,
      new_password1: '',
      new_password2: '',
      sent: false
    }
  },

  methods: {
    serializeForm () {
      return {
        new_password1: this.new_password1,
        new_password2: this.new_password2,
        uid: this.$route.params.uidb64,
        token: this.$route.params.token
      }
    },

    apiSubmit (data) { return this.$api.auth.resetPasswordToken(data) },

    onSuccess (data) {
      this.sent = true
      setTimeout(() => { this.$router.push({ name: 'auth-login' }) }, 3500)
    },

    onError (data) {
      if (data.response.data.uid || data.response.data.token) {
        this.$store.dispatch('formerrors/show', ['The informed token is invalid!'])
      }
    }

    // submit () {
    //   if (this.$validator.validateAll()) {
    //     this.working = true

    //     this.$http.post('/api/auth/password/reset/confirm/', data)
    //       .then(data => data.json())
    //       .then(obj => {
    //       })
    //       .catch(err => {
    //         if (err.json) {
    //           err.json().then(data => {
    //             if (data.uid || data.token) {
    //               this.nonFieldErrors.push('The informed token is invalid!')
    //             }
    //           })
    //         }
    //         this.processErrors(err)
    //       })
    //       .finally(() => { this.working = false })
    //   }
    // }
  }
}
</script>

<style scoped>
#register-card-title {
  min-height: 105px;
  border-top-left-radius: 2px !important;
  border-top-right-radius: 2px !important;
}
</style>
