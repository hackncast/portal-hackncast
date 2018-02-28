<template>
<v-container fluid fill-height pt-1>
  <v-layout align-center justify-center style="z-index: 2">
    <v-flex xs12 sm6 md4>
      <v-card color="white" class="elevation-3" style="overflow: hidden">
        <v-card-title primary-title class="text-xs-center blue white--text" id="register-card-title">
          <transition name="delayed-fade" mode="out-in">
            <div key="registration" v-if="!registered" style="width: 100%">
              <h1 class="headline">Registration</h1>
              <v-layout row justify-space-around>
                <v-btn flat icon color="white"><v-icon class="social-login-icon">fa-github</v-icon></v-btn>
                <v-btn flat icon color="white"><v-icon class="social-login-icon">fa-google</v-icon></v-btn>
                <v-btn flat icon color="white"><v-icon class="social-login-icon">fa-twitter</v-icon></v-btn>
              </v-layout>
            </div>
            <div key="success" v-else style="width: 100%">
              <h1 class="headline">Thank you!</h1>
              <v-progress-linear :indeterminate="true" :active="true" height="2" color="blue darken-3" style="margin-bottom: 0px"/>
            </div>
          </transition>
        </v-card-title>
        <transition name="shrink" duration="500">
          <v-card-text v-show="!registered" v-model="valid">
            <v-form @submit.prevent="submit" ref="form">
              <v-text-field light autofocus label="Email" name="email" ref="email" type="email" tabindex="1" required autofocus
                            v-validate="'required|email'"
                            prepend-icon="mail"
                            data-vv-as="email"
                            :error-messages="errors.collect('email')"
                            v-model="email">
              </v-text-field>

              <v-text-field light label="Password" name="password1" ref="password1" tabindex="2" required
                            v-model="password1"
                            prepend-icon="lock"
                            v-validate="'required'"
                            data-vv-as="password"
                            :error-messages="errors.collect('password1')"
                            :append-icon="showPassword ? 'visibility_off' : 'visibility'"
                            :append-icon-cb="() => (showPassword = !showPassword)"
                            :type="showPassword ? 'text' : 'password'"
                            >
              </v-text-field>

              <v-text-field light label="Confirm Password" name="password2" ref="password2" tabindex="3" required
                            v-model="password2"
                            v-validate="'required|confirmed:password1'"
                            prepend-icon="lock"
                            data-vv-as="password"
                            :error-messages="errors.collect('password2')"
                            :append-icon="showPassword ? 'visibility_off' : 'visibility'"
                            :append-icon-cb="() => (showPassword = !showPassword)"
                            :type="showPassword ? 'text' : 'password'"
                            >
              </v-text-field>

              <vue-recaptcha ref="invisibleRecaptcha"
                             @verify="submit"
                             size="invisible"
                             :sitekey="sitekey"
                             tabindex="-1"
                             >
                <v-btn light block color="blue" class="white--text" :disabled="errors.any() || isNotValidated()" type="submit" :loading="working" tabindex="4">Register</v-btn>
              </vue-recaptcha>
            </v-form>
          </v-card-text>
        </transition>
      </v-card>
      <transition name="fade">
        <v-btn v-show="!registered" flat block class="white--text mt-3" :to="{ name: 'user:login' }">Already registered?</v-btn>
      </transition>

      <error-bottom-sheet :non-field-errors="nonFieldErrors" @clear-errors="clearNonFieldErrors()"/>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import VueRecaptcha from 'vue-recaptcha'
import { FormMixin } from '@/mixins/FormMixin'

export default {
  name: 'Registration',

  components: {VueRecaptcha},

  mixins: [FormMixin],

  data () {
    return {
      working: false,
      valid: false,
      sitekey: process.env.CAPTCHA_PUBLIC_KEY,
      showPassword: false,
      email: '',
      password1: '',
      password2: '',
      registered: false
    }
  },

  methods: {
    submit (captchaResponse = '') {
      if (this.$validator.validateAll() && captchaResponse !== '') {
        const data = {
          email: this.email,
          password1: this.password1,
          password2: this.password1,
          recaptcha: captchaResponse
        }
        this.working = true

        this.$http.post('/api/auth/registration/', data)
          .then(data => data.json())
          .then(obj => {
            this.registered = true
            setTimeout(() => {
              this.$router.push({ name: 'home' })
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

.social-login-icon {
  font-size: 1.8em;
  margin-bottom: 2px;
}
</style>
