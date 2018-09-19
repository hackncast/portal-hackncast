import { distanceInWords } from 'date-fns'

export default {
  install (Vue, options) {
    Vue.filter('defaultValue', function (value, defaultValue) {
      if (!defaultValue) defaultValue = '-'
      if (value === undefined || value === null || value.length === 0) return defaultValue
      return value
    })

    Vue.filter('fmtDate', function (value) {
      return value.toLocaleDateString()
    })

    Vue.filter('fmtRelativeDate', function (endDate, startDate) {
      if (!endDate) return null
      if (!startDate) startDate = new Date()
      return distanceInWords(endDate, startDate)
    })
  }
}
