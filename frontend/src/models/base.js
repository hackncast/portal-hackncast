function camelCase (word) {
  let first, pieces
  [first, ...pieces] = word.split('_')
  pieces = pieces.map(piece => piece[0].toUpperCase() + piece.slice(1))
  pieces.unshift(first)
  return pieces.join('')
}

export default class BaseModel {
  constructor (data = {}) {
    this.pk = null
    Object.keys(data).forEach(key => { this[key] = data[key] })
  }

  static fromJson (data) {
    let newData = {}
    Object.keys(data).forEach(key => { newData[camelCase(key)] = data[key] })
    return new this(newData)
  }
}
