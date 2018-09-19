// eslint-disable-next-line
Object.defineProperty(Array.prototype, 'findByPk', {
  enumerable: false,
  value: function (pk) { return this.find(o => o.pk === pk) }
})
