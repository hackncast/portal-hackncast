<template>
  <v-app id="app" :style="{ backgroundImage: getbackgroundImage }">
    <v-toolbar flat dark color="transparent" style="z-index: 2" id="nav-site-title">
      <v-toolbar-side-icon tab-index="-1">
        <v-avatar>
          <img src="@/assets/hnc-logo-noframe-inverted.svg" alt="Logo">
        </v-avatar>
      </v-toolbar-side-icon>
      <v-toolbar-title id="hnc-brand">Hack 'n' Cast</v-toolbar-title>
    </v-toolbar>
    <v-content>
      <v-container fluid fill-height pt-1>
        <v-layout align-center justify-center style="z-index: 2">
          <v-flex xs12 sm6 md4>
            <v-card color="white" class="elevation-3" id="register-card">
              <v-card-title id="register-card-title" primary-title class="text-xs-center blue white--text">
                <h1 class="headline" style="width: 100%">Registration</h1>
                <v-layout row justify-space-around>
                  <v-btn flat icon color="white"><v-icon>fa-github</v-icon></v-btn>
                  <v-btn flat icon color="white"><v-icon>fa-google</v-icon></v-btn>
                  <v-btn flat icon color="white"><v-icon>fa-twitter</v-icon></v-btn>
                </v-layout>
              </v-card-title>
            <v-expansion-panel>
              <v-expansion-panel-content key="1" :value="!registered" :hide-actions="true">
              <v-card-text id="register-card-text" style="height: 100%">
                <v-form @submit.prevent="submit" ref="form">
                  <v-text-field autofocus label="Email" name="email" ref="email" type="email" required
                                v-validate="'required|email'"
                                prepend-icon="mail"
                                data-vv-as="email"
                                :error-messages="errors.collect('email')"
                                v-model="email">
                  </v-text-field>

                  <v-text-field label="Password" name="password1" ref="password1" required
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

                  <v-text-field label="Confirm Password" name="password2" ref="password2" required
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

                  <v-btn block color="blue" class="white--text" :disabled="errors.any() || isNotValidated()" type="submit">Register</v-btn>
                </v-form>
              </v-card-text>
              </v-expansion-panel-content>
            </v-expansion-panel>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
    <v-footer dark color="transparent" style="z-index: 2">
      <span>&copy; 2017</span>
    </v-footer>
  </v-app>
</template>

<script>
import { FormMixin } from '@/mixins/FormMixin'

export default {
  name: 'Login',
  mixins: [FormMixin],
  data () {
    return {
      images: [
        // 'https://cdn.stocksnap.io/img-thumbs/960w/CWYK8CLC61.jpg',
        // 'https://cdn.stocksnap.io/img-thumbs/960w/DKNN0YHNEE.jpg',
        // 'https://cdn.stocksnap.io/img-thumbs/960w/U3W2SHOLWQ.jpg',
        // 'https://cdn.stocksnap.io/img-thumbs/960w/4GO4VAB14Z.jpg',
        // 'https://cdn.stocksnap.io/img-thumbs/960w/YSUCTBXV32.jpg',
        // 'https://cdn.stocksnap.io/img-thumbs/960w/BKWZJHXR57.jpg',
        'https://cdn.stocksnap.io/img-thumbs/960w/YP10KAYY2D.jpg',
        'https://cdn.stocksnap.io/img-thumbs/960w/Z7L87CLJVN.jpg'
      ],
      showPassword: false,
      email: '',
      password1: '',
      password2: '',
      registered: false
    }
  },

  computed: {
    getbackgroundImage () {
      let image = this.images[Math.floor(Math.random() * this.images.length)]
      return `url('${image}')`
    }
  },

  methods: {
    submit () {
      if (this.$validator.validateAll()) {
        const data = {
          email: this.email,
          password1: this.password1,
          password2: this.password1
        }

        this.$http.post('/api/auth/registration/', data)
          .then(data => { console.log('data', data); return data.json() })
          .then(obj => console.log('obj', obj))
          .catch(err => { this.registered = true; return console.log('err', err) })
      }
    }
  }
}
</script>

<style scoped>
#app {
  background-size: cover;
  background-position: center;
}
#app::before {
  background-color: rgba(0, 0, 0, .6);
  position: fixed;
  z-index: 1;
  width: 100%;
  height: 100%;
  display: block;
  left: 0;
  top: 0;
  content: "";
}

@media screen and (max-width: 600px) {
  #nav-site-title .toolbar__title {
    width: 100%;
    text-align: center;
    margin-left: -36px;
  }
}

@media screen and (min-width: 600px) {
  #nav-site-title {
    margin-left: 8%;
    margin-right: 8%;
  }
}

#register-card-title {
  border-top-left-radius: 2px !important;
  border-top-right-radius: 2px !important;
}

#register-card-text {
}

.shrink-enter-active, .shrink-leave-active {
  transition: height 2s;
}
.shrink-enter, .shrink-leave-to {
  animation: mymove .75s;
}

@keyframes mymove {
    0%   {height: 302px; opacity: 1;}
    25%  {opacity: .5;}
    50%  {opacity: .0; padding: 16px}
    100% {height: 0px; padding: 0px; opacity: 0;}
  }
</style>
