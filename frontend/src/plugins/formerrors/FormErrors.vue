<template>
  <v-bottom-sheet inset persistent :value="formErrors.length > 0">
    <v-card dark>
      <v-card-title>
        <div>
          <v-btn ref="errorCloseButton" small absolute dark fab top right color="red darken-2" @click="closeErrors"><v-icon>close</v-icon></v-btn>
          <v-subheader style="line-height: 1.5em; padding: 0px;">Os seguintes erros ocorreram durante o envio do formulário:</v-subheader>
          <ul style="padding-left: 2em; color: hsla(0%, 0%, 100%, .7)">
            <li :key="index" v-for="(error, index) in formErrors">{{ error }}</li>
          </ul>
        </div>
      </v-card-title>
    </v-card>
  </v-bottom-sheet>
</template>

<script>
export default {
  computed: {
    formErrors () { return this.$store.state.formerrors.all }
  },

  methods: {
    closeErrors () {
      this.$store.dispatch('formerrors/clear')
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
    formErrors (val) {
      if (this.formErrors.length > 0) {
        this.$nextTick(() => this.$refs.errorCloseButton.$el.focus())
      } else {
        if (document.forms.length > 0) { this.$nextTick(() => this.refocusForm()) }
      }
    }
  }
}
</script>
