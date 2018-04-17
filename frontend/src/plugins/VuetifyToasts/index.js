import Vue from 'vue'
import I18n from '@/i18n'
import VuetifyToast from './toast'

let queue = []
let showing = false

let toasts = {
  open (params) {
    if (!params.text) return console.error('[toast] no text supplied')

    let propsData = {
      title: params.title,
      text: params.text,
      closeText: I18n.i18n.t('label.close'),
      type: params.type,
      timeout: params.timeout,
      actions: params.actions || []
    }

    let defaultOptions = {
      color: params.type,
      closeable: true,
      autoHeight: true,
      timeout: params.persist ? null : params.timeout || 5000,
      vertical: !!params.title || params.text.length > 80 || propsData.actions.length > 0
    }

    params.options = Object.assign(defaultOptions, params.options)
    propsData.options = params.options

    // push into queue
    queue.push(propsData)
    processQueue()
  }
}

function processQueue () {
  if (queue.length < 1) return
  if (showing) return

  let nextInLine = queue[0]
  spawn(nextInLine)
  showing = true

  queue.shift()
}

function spawn (propsData) {
  const VuetifyToastComponent = Vue.extend(VuetifyToast)
  return new VuetifyToastComponent({
    el: document.createElement('div'),
    propsData,
    onClose: function () {
      showing = false
      processQueue()
    }
  })
}

const VuetifyToasts = {
  install (Vue, options) {
    Vue.prototype.$toasts = toasts
    Vue.toasts = toasts
  }
}

export default VuetifyToasts
