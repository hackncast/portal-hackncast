<template>
<v-container fluid fill-height pt-1>
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
                            data-vv-as="email"
                            :error-messages="errors.collect('email')"
                            v-model="email">
              </v-text-field>

              <vue-recaptcha ref="invisibleRecaptcha"
                             @verify="submit"
                             size="invisible"
                             :sitekey="sitekey"
                             tabindex="-1">
                <v-btn light block color="blue" class="white--text" :disabled="errors.any() || isNotValidated()" type="submit" :loading="working" tabindex="2">Reset Password</v-btn>
              </vue-recaptcha>
            </v-form>
          </v-card-text>
        </transition>
      </v-card>

      <v-btn small flat block class="white--text mt-3" :to="{ name: 'user:login' }">I remembered my password!</v-btn>

      <error-bottom-sheet :non-field-errors="nonFieldErrors" @clear-errors="clearNonFieldErrors()"/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import VueRecaptcha from 'vue-recaptcha'
import { FormMixin } from '@/mixins/FormMixin'

export default {
  name: 'ResetPassword',

  components: {VueRecaptcha},

  mixins: [FormMixin],

  head: {
    script: [
      { type: 'text/javascript', src: 'https://www.google.com/recaptcha/api.js?onload=vueRecaptchaApiLoaded&render=explicit', async: true, defer: true }
    ]
  },

  data () {
    return {
      sitekey: process.env.CAPTCHA_PUBLIC_KEY,
      working: false,
      valid: false,
      email: '',
      sent: false
    }
  },

  methods: {
    submit (captchaResponse) {
      if (this.$validator.validateAll()) {
        const data = {
          email: this.email,
          recaptcha: captchaResponse
        }
        this.working = true

        this.$http.post('/api/auth/password/reset/', data)
          .then(data => data.json())
          .then(obj => {
            this.sent = true
            setTimeout(() => {
              this.$router.push({ name: 'user:login' })
            }, 3500)
          })
          .catch(err => {
            this.processErrors(err)
            this.$refs.invisibleRecaptcha.reset()
          })
          .finally(() => { this.working = false })
      }
    }
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
