export const FormMixin = {
  data () {
    return {
      defaultErrorMessage: 'Sorry, your form still have errors!',
      networkErrorMessage: 'An error occured while communicating with the server, please try again later.',
      nonFieldErrors: []
    }
  },
  methods: {
    isNotValidated () {
      return Object.values(this.fields).filter(i => i.required).some(i => !i.validated)
    },
    injectErrors (data) {
      // Non Field Errors
      if (data.non_field_errors) {
        data.non_field_errors.forEach(value => {
          this.nonFieldErrors.push(value)
        })
        delete data.non_field_errors
      }

      // API/HTTP Errors
      if (data.detail) {
        this.nonFieldErrors.push(data.detail)
        delete data.detail
      }

      // Field Errors
      Object.keys(data).forEach(name => {
        if (this.fields.hasOwnProperty(name)) {
          data[name].forEach(text => {
            this.$validator.errors.add(name, text)
          })
        }
      })
    },
    processErrors (err) {
      if (err.ok === false && err.status === 0) {
        this.nonFieldErrors.push(this.networkErrorMessage)
      } else if (err.json) {
        err.json().then(data => this.injectErrors(data))
      } else if (typeof err === 'object') {
        this.injectErrors(err)
      } else {
        this.nonFieldErrors.push(this.defaultErrorMessage)
      }
    }
  }
}
