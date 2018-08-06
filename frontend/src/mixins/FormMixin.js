export const FormMixin = {
  data () {
    return {
      djDefaultErrorMessage: 'Desculpe, mas seu formulário contém erros!'
    }
  },

  methods: {
    isNotValidated () {
      return Object.values(this.fields)
        .filter(i => i.required)
        .some(i => !i.validated)
    },

    djInjectErrors (data) {
      // Non Field Errors
      if (data.non_field_errors) {
        this.$store.dispatch('toastErrors', data.non_field_errors)
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
            this.$store.dispatch('toastErrors', errors.map(error => name + ': ' + error))
          }
        } else {
          this.djProcessFieldErrors(errors)
        }
      })
    },

    djProcessErrors (err) {
      setTimeout(() => {
        if (!err.response) {
          this.$store.dispatch('toastErrors', [err.message])
        } else if (err.response && err.response.status && err.response.data) {
          if (err.response.status === 400) {
            this.djInjectErrors(err.response.data)
          } else if (err.response.status >= 500 && err.response.status <= 599) {
            this.$store.dispatch('toastErrors', ['Erro ao se comunicar com o servidor!'])
          }
        } else {
          this.$store.dispatch('toastErrors', [this.defaultErrorMessage])
        }
      }, 150)
    },

    djClearNonFieldErrors () {
      this.$store.dispatch('toastErrors')
    }
  }
}
