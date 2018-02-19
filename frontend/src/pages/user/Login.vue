<template>
  <v-app id="app" dark :style="{ backgroundImage: getbackgroundImage }">
    <v-toolbar flat color="transparent" style="z-index: 2" id="nav-site-title">
      <v-toolbar-side-icon tab-index="-1">
        <v-avatar>
          <img src="@/assets/hnc-logo-noframe-inverted.svg" alt="Logo">
        </v-avatar>
      </v-toolbar-side-icon>
      <v-toolbar-title>Hack 'n' Cast</v-toolbar-title>
    </v-toolbar>
    <v-content>
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
                      <v-btn icon><v-icon>fa-github</v-icon></v-btn>
                      <v-btn icon><v-icon>fa-google</v-icon></v-btn>
                      <v-btn icon><v-icon>fa-twitter</v-icon></v-btn>
                    </v-layout>
                    <v-text-field autofocus label="Email" name="email" ref="email" type="email" required
                                  prepend-icon="person"
                                  v-validate="'required|email'"
                                  data-vv-as="email"
                                  :error-messages="errors.collect('email')"
                                  v-model.trim="email">
                    </v-text-field>

                    <v-btn block color="primary" class="white--text" @click="nextLoginPage" :disabled="email.length === 0 || errors.has('email')">Next</v-btn>
                  </section>
                  <section v-show="step === 2" key="password" style="position: absolute; width: 100%">
                    <v-btn icon class="ma-0" @click="step = 1"><v-icon>arrow_back</v-icon></v-btn>
                    <v-text-field label="Password" name="password" ref="password" required
                                  :type="showPassord ? 'text' : 'password'"
                                  prepend-icon="lock"
                                  v-validate="'required|min:6'"
                                  data-vv-as="password"
                                  :error-messages="errors.collect('password')"
                                  v-model="password">
                    </v-text-field>

                    <v-checkbox label="Remember-me" name="remember" v-model="remember" type="checkbox">
                    </v-checkbox>

                    <v-btn block color="primary" type="submit" class="white--text">Login</v-btn>

                  </section>
                </transition-group>
              </v-form>

              <v-bottom-sheet inset persistent :value="nonFieldErrors.length > 0">
                <v-card>
                  <v-card-title>
                  <div>
                    <v-btn small absolute dark fab top right color="red darken-2" @click="nonFieldErrors.splice(0, nonFieldErrors.length)">
                      <v-icon>close</v-icon>
                    </v-btn>
                    <v-subheader style="line-height: 1.5em;">Os seguintes erros ocorreram ao subemter o formulário:</v-subheader>
                    <ul style="padding-left: 3em; color: hsla(0,0%,100%,.7)">
                      <li v-for="erro in nonFieldErrors">{{ erro }}</li>
                    </ul>
                  </div>
                  </v-card-title>
                </v-card>
              </v-bottom-sheet>

              <v-layout row justify-space-between>
                <v-btn flat small class="ml-0" :to="{ name: 'user:registration' }">Register</v-btn>
                <v-btn flat small class="mr-0">Need Help?</v-btn>
              </v-layout>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
    <v-footer color="transparent" style="z-index: 2">
      <span>&copy; 2017</span>
    </v-footer>
  </v-app>
</template>

<script>
// import md5 from 'md5/md5'
import _ from 'lodash'
import { FormMixin } from '@/mixins/FormMixin'
import { mapActions } from 'vuex'

export default {
  name: 'Login',

  mixins: [FormMixin],

  data () {
    return {
      step: 1,
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
      showPassord: false,
      valid: false,
      email: '',
      password: '',
      remember: false,
      avatar: null,
      showErrors: false
    }
  },

  watch: {
    email: _.debounce(function () {
      if (this.email.search('@') <= 0) {
        return
      }
      // this.avatar = `https://www.gravatar.com/avatar/${md5(this.email)}?s=100&d=retro`
      this.avatar = `https://www.gravatar.com/avatar/123456?s=100&d=retro`
      // setTimeout(function () {
      //   this.avatar = 'OK'
      // }.bind(this), 2000)
    }, 500)
  },

  computed: {
    getbackgroundImage () {
      let image = this.images[Math.floor(Math.random() * this.images.length)]
      return `url('${image}')`
    }
  },

  methods: {
    ...mapActions([
      'login'
    ]),

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
        this.$validator.validateAll().then(res => {
          if (res) {
            const data = {
              email: this.email,
              password: this.password
            }

            this.login(data)
              .then(user => {
                if (this.$route.query.next) {
                  this.$router.push(this.$route.query.next)
                } else {
                  this.$router.push({name: 'home'})
                }
              })
              .catch(err => {
                this.processErrors(err)
              })
          } else {
            this.nonFieldErrors.push(this.defaultErrorMessage)
          }
        })
      }
    }
  }
}
</script>

<style scoped>
#app {
  // background-image: url('https://cdn.stocksnap.io/img-thumbs/960w/BKWZJHXR57.jpg');
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

#toolbar-login {
  height: 45vh
}

.card--flex-toolbar {
  margin-top: -64px;
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

.avatar-container .avatar {
  transform-style: preserve-3d;
  transition: transform ease .250s;
}

.fa.icon {
  font-size: 20px;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .250s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

.flipY-enter-active, .flipY-leave-active {
  transition: all .150s;
}
.flipY-enter, .flipY-leave-to {
  transform: rotateY(90deg);
}

.customSlide-enter-active, .customSlide-leave-active {
  transition: transform ease .250s;
}
.customSlide-enter {
  transform: translateX(-100vw);
}
.customSlide-leave-to {
  transform: translateX(100vw);
}
</style>
