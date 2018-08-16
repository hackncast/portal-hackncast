<template>
  <v-dialog :value="visible" fullscreen transition="dialog-bottom-transition" :overlay="false" scrollable>
    <v-card tile>
      <v-toolbar card dark color="primary">
        <v-toolbar-title>User Interface Settings</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon @click.native="visible = false" dark>
          <v-icon>close</v-icon>
        </v-btn>
      </v-toolbar>

      <v-card-text>
        <v-subheader>General</v-subheader>
        <v-switch label="Dark Theme"
                  v-model="darkTheme"
                  color="blue darken-2"
                  hint="Use the darke theme in lower ligths environments."
                  persistent-hint>
        </v-switch>
        <v-switch label="Compact Sidebar"
                  v-model="miniSidebar"
                  color="blue darken-2"
                  hint="Use a compact sidebar with popup menus. This option does not have effect on mobile devices."
                  persistent-hint>
        </v-switch>
        <v-select :items="languages"
                  v-model="language"
                  label="Language"
                  @input="onLanguage"
                  hint="User Interface Language."
                  persistent-hint>
        </v-select>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'UiSettingsDialog',

  data () {
    return {
      language: null,
      languages: [
        { text: 'Portugês', locale: 'pt-BR' },
        { text: 'English', locale: 'en-US' }
      ]
    }
  },

  computed: {
    darkTheme: {
      get () { return this.$store.state.ui.darkTheme },
      set (val) { this.setDarkTheme(val) }
    },

    miniSidebar: {
      get () { return this.$store.state.ui.miniSidebar },
      set (val) { this.setMiniSidebar(val) }
    },

    visible: {
      get () { return this.$store.state.ui.uiSettingsVisible },
      set (val) { this.showUiSettings(val) }
    }
  },

  methods: {
    ...mapActions({
      showUiSettings: 'ui/showUiSettings',
      setMiniSidebar: 'ui/setMiniSidebar',
      setDarkTheme: 'ui/setDarkTheme'
    }),

    onLanguage () {
      // this.setLanguage(this.language.locale)
    }
  }

  // created () {
  //   let locale = localStorage.getItem('language') || navigator.language || navigator.languages[0]
  //   this.language = this.languages.find(lang => lang.locale === locale)

  //   if (!this.language) {
  //     this.language = this.languages.find(lang => lang.locale === 'en-US')
  //   }
  // }
}
</script>
