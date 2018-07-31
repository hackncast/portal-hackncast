<template>
  <v-dialog :value="visible" persistent max-width="350">
    <v-card>
      <v-card-title class="headline">{{ $t(title) }}</v-card-title>
      <v-card-text>
        <slot></slot>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn flat color="red" :disabled="loading" @click="$emit('negative')">{{ $t(negativeText) }}</v-btn>
        <v-btn flat color="blue" @click="loading = true; $emit('positive', dialogKey)" :loading="loading">{{ $t(positiveText) }}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'ConfirmDialog',

  props: {
    visible: {
      type: Boolean,
      default: false
    },
    title: { type: String, default: 'dialog.confirm-step.title' },
    positiveText: { type: String, default: 'label.yes' },
    negativeText: { type: String, default: 'label.no' },
    dialogKey: ''
  },

  data () {
    return {
      loading: false
    }
  },

  watch: {
    visible (to, from) {
      if (to === false) {
        this.loading = false
      }
    }
  }
}
</script>
