// eslint-disable-next-line
Object.defineProperty(Array.prototype, 'findByPk', {
  enumerable: false,
  value: function (pk) { return this.find(o => o.pk === pk) }
})

// eslint-disable-next-line
Object.defineProperty(Array.prototype, 'empty', {
  enumerable: false,
  value: function (pk) { return this.splice(0, this.length) }
})
