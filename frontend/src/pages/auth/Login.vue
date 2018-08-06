<template>
<v-container fluid fill-height pt-1>
  <v-layout align-center justify-center style="z-index: 2">
    <v-flex xs12 sm6 md3>
      <v-flex sm12 text-xs-center class="avatar-container">
        <transition name="flipY" mode="out-in">
          <v-avatar v-if="step === 1" key="icon" size="100px" class="primary mb-3">
            <v-icon dark style="font-size: 5em;">person</v-icon>
          </v-avatar>
          <v-avatar v-else key="avatar" size="100px" class="primary mb-3">
            <img :src="avatar" :alt="`Avatar of ${email}`" :title="`Avatar of ${email}`">
          </v-avatar>
        </transition>
      </v-flex>
        <v-form @submit.prevent="submit" v-model="valid" ref="form" style="min-height: 250px; position: relative">
          <transition-group name="customSlide" mode="out-in">
            <section v-show="step === 1" key="email" class="transitioned" style="position: absolute; width: 100%">
              <v-layout row justify-center>
                <v-btn icon @click="notYet"><v-icon class="social-login-icon">fab fa-github</v-icon></v-btn>
                <v-btn icon @click="notYet"><v-icon class="social-login-icon">fab fa-google</v-icon></v-btn>
                <v-btn icon @click="notYet"><v-icon class="social-login-icon">fab fa-twitter</v-icon></v-btn>
              </v-layout>
              <v-text-field autofocus label="Email" name="email" ref="email" type="email" required
                            prepend-icon="person"
                            v-validate="'required|email'"
                            data-vv-as="Email"
                            :error-messages="errors.collect('email')"
                            v-model.trim="email">
              </v-text-field>

              <v-btn block color="primary" class="white--text" @click="nextLoginPage" :disabled="email.length === 0 || errors.has('email')">Next</v-btn>
            </section>
            <section v-show="step === 2" key="password" style="position: absolute; width: 100%">
              <v-btn icon class="ma-0" @click="back()"><v-icon>arrow_back</v-icon></v-btn>
              <v-text-field label="Password" name="password" ref="password" required
                            :type="showPassord ? 'text' : 'password'"
                            prepend-icon="lock"
                            v-validate="'required|min:6'"
                            data-vv-as="Password"
                            :error-messages="errors.collect('password')"
                            v-model="password">
              </v-text-field>

              <v-checkbox disabled label="Remember Me" name="remember" v-model="remember" type="checkbox"/>

              <v-btn block color="primary" type="submit" class="white--text" :loading="working">Login</v-btn>
            </section>
          </transition-group>
        </v-form>

        <v-layout row justify-space-between>
          <v-btn flat small class="ml-0" :to="{ name: 'auth-registration' }">Register</v-btn>
          <v-btn flat small class="mr-0">Need help?</v-btn>
        </v-layout>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import md5 from 'md5/md5'
import { mapActions } from 'vuex'
import { debounce } from '@/utils'
import { FormMixin } from '@/mixins/FormMixin'

export default {
  name: 'LoginPage',

  route: {
    name: 'auth-login',
    layout: 'Public',
    middlewares: ['PublicOnly']
  },

  mixins: [FormMixin],

  data () {
    return {
      working: false,
      step: 1,
      showPassord: false,
      valid: false,
      email: '',
      password: '',
      remember: false,
      avatar: null
    }
  },

  methods: {
    ...mapActions([
      'login'
    ]),

    back () {
      this.step = 1
      this.password = ''
    },

    nextLoginPage () {
      if (!this.errors.has('email')) {
        this.step = 2
        this.$nextTick(() => this.$refs.password.focus())
      }
    },

    submit () {
      if (this.step === 1) {
        if (this.email && !this.errors.has('email')) {
          this.step = 2
          this.$nextTick(() => this.$refs.password.focus())
        }
      } else {
        if (this.$validator.validateAll()) {
          this.working = true
          const data = {
            email: this.email,
            password: this.password
          }
          console.log(data)

          // this.login(data)
          //   .then(user => {
          //     if (this.$route.query.next) {
          //       this.$router.push(this.$route.query.next)
          //     } else {
          //       this.$router.push({name: 'home'})
          //     }
          //   })
          //   .catch(err => {
          //     this.processErrors(err)
          //   })
          //   .finally(() => { this.working = false })
        } else {
          this.nonFieldErrors.push(this.defaultErrorMessage)
        }
      }
    },

    notYet () {
      this.$toast({text: 'Sorry, not working yet...'})
    }
  },

  watch: {
    email: debounce(function () {
      if (this.email.search('@') <= 0) {
        return
      }
      this.avatar = `https://www.gravatar.com/avatar/${md5(this.email)}?s=100&d=retro`
    }, 500)
  }
}
</script>

<style scoped>
.avatar-container .avatar {
  transform-style: preserve-3d;
  transition: transform ease .250s;
}

.social-login-icon {
  font-size: 1.8em;
  margin-bottom: 2px;
}
</style>
