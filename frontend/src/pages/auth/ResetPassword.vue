<template>
<v-container fluid fill-height pt-1>
  <loading-dialog v-if="!captchaReady" />

  <v-layout align-center justify-center style="z-index: 2">
    <v-flex xs12 sm6 md4>
      <v-card color="white" class="elevation-3" style="overflow: hidden">
        <v-card-title primary-title class="text-xs-center blue white--text" id="register-card-title">
          <transition name="delayed-fade" mode="out-in">
            <div key="registration" v-if="!sent" style="width: 100%">
              <h1 class="headline">Lost Your Password?</h1>
            </div>
            <div key="success" v-else style="width: 100%">
              <h1 class="headline">Please, check your email!</h1>
              <v-progress-linear :indeterminate="true" :active="true" height="2" color="blue darken-3" style="margin-bottom: 0px"/>
            </div>
          </transition>
        </v-card-title>
        <transition name="shrink" duration="500">
          <v-card-text v-show="!sent" v-model="valid">
            <v-form @submit.prevent="submit" ref="form">
              <v-text-field light autofocus label="Email" name="email" ref="email" type="email" required tabindex="1"
                            v-validate="'required|email'"
                            prepend-icon="mail"
                            :data-vv-as="email"
                            :error-messages="errors.collect('email')"
                            v-model="email">
              </v-text-field>

              <vue-recaptcha ref="invisibleRecaptcha"
                             @verify="submit"
                             @render="onCaptchaReady"
                             size="invisible"
                             :sitekey="sitekey"
                             tabindex="-1">
                <v-btn light block color="blue" class="white--text" :disabled="errors.any() || isNotValidated()" type="submit" :loading="loading" tabindex="2">Reset Password!</v-btn>
              </vue-recaptcha>
            </v-form>
          </v-card-text>
        </transition>
      </v-card>

      <v-btn small flat block class="white--text mt-3" :to="{ name: 'auth-login' }">I remembered my password!</v-btn>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import VueRecaptcha from 'vue-recaptcha'
import { FormMixin } from '@/mixins/FormMixin'
import LoadingDialog from '@/components/Loading'

export default {
  name: 'ResetPassword',

  route: {
    name: 'auth-reset-password',
    layout: 'Public',
    middlewares: ['PublicOnly']
  },

  mixins: [FormMixin],

  components: { VueRecaptcha, LoadingDialog },

  head: {
    script: [
      { type: 'text/javascript', src: 'https://www.google.com/recaptcha/api.js?onload=vueRecaptchaApiLoaded&render=explicit', async: true, defer: true }
    ]
  },

  data () {
    return {
      sitekey: process.env.VUE_APP_CAPTCHA_PUBLIC_KEY,
      captchaReady: false,
      valid: false,
      email: '',
      sent: false
    }
  },

  methods: {
    serializeForm (captchaResponse) {
      return {
        email: this.email,
        recaptcha: captchaResponse
      }
    },

    apiSubmit (data) { return this.$api.auth.resetPassword(data) },

    onSuccess (data) {
      this.sent = true
      setTimeout(() => {
        this.$router.push({ name: 'auth-login' })
      }, 3500)
    },

    onError (data) { this.$refs.invisibleRecaptcha.reset() },

    onCaptchaReady () { this.captchaReady = true }
  }
}
</script>

<style scoped>
#register-card-title {
  min-height: 120px;
  border-top-left-radius: 2px !important;
  border-top-right-radius: 2px !important;
}
</style>
