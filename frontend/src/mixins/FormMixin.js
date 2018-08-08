export const FormMixin = {
  data () {
    return {
      loading: false,
      djDefaultErrorMessage: 'Desculpe, mas seu formulário contém erros!'
    }
  },

  methods: {
    serializeForm () {
      throw Error('The serializeForm method MUST be overwritten!')
    },

    submit (args) {
      console.log('before', this)
      this.$validator.validateAll()
        .then(success => {
          if (!success) return

          const data = this.serializeForm(args)
          this.loading = true

          this.apiSubmit(data)
            .then(data => {
              return this.onSuccess(data)
            })
            .catch(err => {
              this.djProcessErrors(err)
              this.onError(err)
              return err
            })
            .finally(() => { this.loading = false })
        })
    },

    isNotValidated () {
      return Object.values(this.fields)
        .filter(i => i.required)
        .some(i => !i.validated)
    },

    djInjectErrors (data) {
      // Non Field Errors
      if (data.non_field_errors) {
        this.$store.dispatch('formerrors/show', data.non_field_errors)
        delete data.non_field_errors
      }

      // Field Errors
      this.djProcessFieldErrors(data)
    },

    djProcessFieldErrors (data) {
      Object.keys(data).forEach(name => {
        let errors = data[name]
        if (Array.isArray(errors)) {
          const field = this.$validator.fields.find({ name })
          if (field) {
            errors.forEach(error => {
              this.$validator.errors.add({
                id: field.id, field: name, msg: error
              })
            })
          } else {
            this.$store.dispatch('formerrors/show', errors.map(error => name + ': ' + error))
          }
        } else {
          this.djProcessFieldErrors(errors)
        }
      })
    },

    djProcessErrors (err) {
      setTimeout(() => {
        if (!err.response) {
          this.$store.dispatch('formerrors/show', [err.message])
        } else if (err.response && err.response.status && err.response.data) {
          if (err.response.status === 400) {
            this.djInjectErrors(err.response.data)
          } else if (err.response.status >= 500 && err.response.status <= 599) {
            this.$store.dispatch('formerrors/show', ['Erro ao se comunicar com o servidor!'])
          }
        } else {
          this.$store.dispatch('formerrors/show', [this.defaultErrorMessage])
        }
      }, 150)
    },

    djClearNonFieldErrors () {
      this.$store.dispatch('formerrors/show')
    }
  }
}
