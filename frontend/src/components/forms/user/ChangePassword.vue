<template>
  <v-dialog v-model="show" max-width="400">
    <v-card>
      <v-form @submit.prevent="submit" ref="form">
        <v-card-title class="headline">Change Password</v-card-title>
        <v-card-text>
          <v-text-field light label="Old Password" name="old_password" ref="oldPassword" tabindex="1" required autofocus
                        type="password"
                        v-model="oldPassword"
                        v-validate="'required'"
                        data-vv-as="old password"
                        :error-messages="errors.collect('old_password')">
          </v-text-field>
          <v-text-field light label="New Password" name="new_password1" ref="newPassword1" tabindex="2" required
                        v-model="newPassword1"
                        v-validate="'required|not_equals:oldPassword'"
                        data-vv-as="new password"
                        :error-messages="errors.collect('new_password1')"
                        :append-icon="showPassword ? 'visibility_off' : 'visibility'"
                        :append-icon-cb="() => (showPassword = !showPassword)"
                        :type="showPassword ? 'text' : 'password'">
          </v-text-field>
          <v-text-field light label="Confirm New Password" name="new_password2" ref="newPassword2" tabindex="3" required
                        v-model="newPassword2"
                        v-validate="'required|confirmed:$newPassword1'"
                        data-vv-as="confirm password"
                        :error-messages="errors.collect('new_password2')"
                        :append-icon="showPassword ? 'visibility_off' : 'visibility'"
                        :append-icon-cb="() => (showPassword = !showPassword)"
                        :type="showPassword ? 'text' : 'password'">
          </v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red darken-1" flat="flat" @click.native="$emit('close')" tabindex="4">Cancel</v-btn>
          <v-btn color="green darken-1" flat="flat" :disabled="errors.any() || isNotValidated()" type="submit" :loading="working" tabindex="5">Change</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>

    <error-bottom-sheet :non-field-errors="nonFieldErrors" @clear-errors="clearNonFieldErrors()"/>
  </v-dialog>
</template>

<script>
import { FormMixin } from '@/mixins/FormMixin'
import { Validator } from 'vee-validate'

export default {
  name: 'UserChangePasswordForm',

  mixins: [FormMixin],

  props: {
    show: { type: Boolean }
  },

  data () {
    return {
      working: false,
      showPassword: false,
      oldPassword: '',
      newPassword1: '',
      newPassword2: ''
    }
  },

  watch: {
    show (to, from) {
      if (from === false && to === true) {
        this.init()
        this.$nextTick(() => this.$refs.oldPassword.focus())
      }
    }
  },

  methods: {
    init () {
      this.showPassword = false
      this.working = false
      this.oldPassword = ''
      this.newPassword1 = ''
      this.newPassword2 = ''
      this.$validator.reset()
    },

    submit () {
      this.$validator.validateAll().then(valid => {
        if (valid) {
          this.working = true
          this.$progress.start()

          let data = {
            old_password: this.oldPassword,
            new_password1: this.newPassword1,
            new_password2: this.newPassword2
          }

          this.$http.post('/api/auth/password/change/', data)
            .then(data => data.json())
            .then(email => {
              this.$emit('success')
              this.$emit('close')
            })
            .catch((err) => {
              this.$progress.fail()
              this.processErrors(err)
            })
            .finally(() => {
              this.$progress.stop()
              this.working = false
            })
        }
      })
    }
  },
  created () {
    Validator.extend('equals', {
      getMessage: field => 'Passwords doesn\'t match',
      validate: (value, other) => {
        return String(value) === String(this[other])
      }
    })
    Validator.extend('not_equals', {
      getMessage: field => 'The new password must differ from tha last one',
      validate: (value, other) => {
        return String(value) !== String(this[other])
      }
    })
  }
}
</script>
