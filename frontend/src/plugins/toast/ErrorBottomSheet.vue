<template>
  <v-bottom-sheet inset persistent :value="nonFieldErrors.length > 0">
    <v-card dark>
      <v-card-title>
        <div>
          <v-btn ref="errorBottomSheetCloseButton" small absolute dark fab top right color="red darken-2" @click="closeErrorSheet"><v-icon>close</v-icon></v-btn>
          <v-subheader style="line-height: 1.5em; padding: 0px;">Os seguintes erros ocorreram durante o envio do formulário:</v-subheader>
          <ul style="padding-left: 2em; color: hsla(0%, 0%, 100%, .7)">
            <li v-for="erro in nonFieldErrors">{{ erro }}</li>
          </ul>
        </div>
      </v-card-title>
    </v-card>
  </v-bottom-sheet>
</template>

<script>
export default {
  computed: {
    nonFieldErrors () {
      return this.$store.state.nonFieldErrors
    }
  },

  methods: {
    closeErrorSheet () {
      this.$store.dispatch('toastErrors')
    },

    refocusForm () {
      let input = document.forms[0].querySelector('[autofocus]')
      if (input && input.offsetLeft) return input.focus()

      let allInputs = document.forms[0].getElementsByTagName('input')
      input = Array.from(allInputs).find(e => e.offsetLeft)

      if (input) return input.focus()

      if (allInputs && allInputs.length > 0) return allInputs[0].focus()
    }
  },

  watch: {
    nonFieldErrors (val) {
      if (this.nonFieldErrors.length > 0) {
        this.$nextTick(() => this.$refs.errorBottomSheetCloseButton.$el.focus())
      } else {
        if (document.forms.length > 0) { this.$nextTick(() => this.refocusForm()) }
      }
    }
  }
}
</script>
