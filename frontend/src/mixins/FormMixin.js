export const FormMixin = {
  methods: {
    isNotValidated () {
      return Object.values(this.fields).filter(i => i.required).some(i => !i.validated)
    }
  }
}
