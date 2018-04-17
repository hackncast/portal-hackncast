import VueI18n from 'vue-i18n'
import messages from './messages'
import dateTimeFormats from './dateTimeFormats'
import { Validator } from 'vee-validate'
import VeeMessagePtBR from 'vee-validate/dist/locale/pt_BR'

let I18n = {
  i18n: null,
  __locale: null,

  getLocale () {
    return localStorage.getItem('language') || navigator.language || navigator.languages[0]
  },

  get locale () {
    if (this.__locale) {
      return this.__locale
    }
    this.__locale = this.getLocale()
    return this.__locale
  },

  set locale (locale) {
    this.__locale = locale
    this.i18n.locale = locale
    localStorage.setItem('language', locale)
    this.__updateHtmlLang()
    Validator.localize(this.veeValidateLocale)
  },

  get veeValidateLocale () {
    if (this.__locale === null) {
      this.__locale = this.getLocale()
    }
    return this.__locale.replace('-', '_')
  },

  init (vue) {
    vue.use(VueI18n)
    this.i18n = new VueI18n({
      locale: this.locale,
      messages,
      dateTimeFormats
    })
    this.__updateHtmlLang()
    Validator.localize('pt_BR', VeeMessagePtBR)
    return this.i18n
  },

  __updateHtmlLang () {
    document.documentElement.setAttribute('lang', this.locale)
  }
}

export default I18n
