<template>
  <v-bottom-sheet inset persistent :value="nonFieldErrors.length > 0">
    <v-card>
      <v-card-title>
        <div>
          <v-btn small absolute :dark="dark" fab top right color="red darken-2" @click="$emit('clear-errors')"><v-icon>close</v-icon></v-btn>
          <v-subheader style="line-height: 1.5em; padding: 0px;">{{ text }}</v-subheader>
          <ul style="padding-left: 2em; color: hsla(0,0%,100%,.7)">
            <li v-for="erro in nonFieldErrors">{{ erro }}</li>
          </ul>
        </div>
      </v-card-title>
    </v-card>
  </v-bottom-sheet>
</template>

<script>
export default {
  name: 'ErrorBottomSheet',

  props: {
    dark: {
      type: Boolean,
      default: true
    },
    text: {
      type: String,
      default: 'The following errors ocurred while submitting your form:'
    },
    nonFieldErrors: {
      type: Array,
      required: true
    }
  }
}
</script>

<style scoped>
</style>
