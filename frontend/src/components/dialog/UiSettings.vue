<template>
  <v-dialog :value="visible" fullscreen transition="dialog-bottom-transition" :overlay="false" scrollable>
    <v-card tile>
      <v-toolbar card dark color="primary">
        <v-toolbar-title>{{ $t('label.ui-settings') }}</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon @click.native="$store.state.Ui.uiSettingsVisible = false" dark>
          <v-icon>close</v-icon>
        </v-btn>
      </v-toolbar>

      <v-card-text>
        <v-list three-line subheader>
          <v-subheader>{{ $t('label.general') }}</v-subheader>
          <v-list-tile avatar>
            <v-list-tile-action>
              <v-switch v-model="darkTheme" color="blue darken-2"></v-switch>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>{{ $t('label.dark-theme') }}</v-list-tile-title>
              <v-list-tile-sub-title>{{ $t('helper.dark-ui')  }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <v-list-tile avatar>
            <v-list-tile-action>
              <v-icon>language</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-select :items="languages"
                        v-model="language"
                        label="Language"
                        single-line
                        @input="onLanguage"
                        :hint="$t('helper.ui-language')"
                        persistent-hint>
              </v-select>
            </v-list-tile-content>
          </v-list-tile>

        </v-list>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import { UI } from '@/store/mutation-types'
import { mapGetters, mapMutations } from 'vuex'

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
    ...mapGetters([ 'currentUser' ]),

    darkTheme: {
      get () {
        return this.$store.state.Ui.darkTheme
      },
      set (val) {
        this.setDarkTheme(val)
      }
    },

    visible () {
      if (!this.currentUser.isAuthenticated) {
        return false
      }

      return this.$store.state.Ui.uiSettingsVisible
    }
  },

  methods: {
    ...mapMutations({
      setDarkTheme: UI.DARK_THEME,
      setLanguage: UI.LANGUAGE
    }),

    onLanguage () {
      this.setLanguage(this.language.locale)
    }
  },

  created () {
    let locale = localStorage.getItem('language') || navigator.language || navigator.languages[0]
    this.language = this.languages.find(lang => lang.locale === locale)

    if (!this.language) {
      this.language = this.languages.find(lang => lang.locale === 'en-US')
    }
  }
}
</script>
