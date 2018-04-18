<template>
  <v-dialog v-model="show" max-width="290">
    <v-card>
      <v-form @submit.prevent="submit" ref="form">
        <v-card-title class="headline">{{ $t('profile.new-email-address') }}</v-card-title>
        <v-card-text>
          <v-text-field :label="$t('label.new-email')" name="email" ref="email" type="email" tabindex="1" required autofocus
                        v-validate="'required|email'"
                        :data-vv-as="$t('label.new-email')"
                        :error-messages="errors.collect('email')"
                        v-model="email">
          </v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red darken-1" flat="flat" @click.native="$emit('close')">{{ $t('label.cancel') }}</v-btn>
          <v-btn color="green darken-1" flat="flat" :disabled="errors.any() || isNotValidated()" type="submit" :loading="working" tabindex="1">{{ $t('label.add') }}</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>

    <error-bottom-sheet :non-field-errors="nonFieldErrors" @clear-errors="clearNonFieldErrors()"/>
  </v-dialog>
</template>

<script>
import { FormMixin } from '@/mixins/FormMixin'

export default {
  name: 'UserEmailForm',

  mixins: [FormMixin],

  props: {
    show: { type: Boolean }
  },

  data () {
    return {
      working: false,
      email: ''
    }
  },

  methods: {
    submit () {
      this.$validator.validateAll().then(valid => {
        if (valid) {
          this.working = true
          this.$progress.start()

          let data = {
            email: this.email
          }

          this.$http.post('/api/user/email/', data)
            .then(data => data.json())
            .then(email => {
              this.$emit('success')
              this.$emit('close')
              this.email = ''
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
  }
}
</script>
