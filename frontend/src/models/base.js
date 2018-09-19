function camelCase (word) {
  let first, pieces
  [first, ...pieces] = word.split('_')
  pieces = pieces.map(piece => piece[0].toUpperCase() + piece.slice(1))
  pieces.unshift(first)
  return pieces.join('')
}

function cleanMethodName (word) {
  let camelCaseWord = camelCase(word)
  return 'clean' + camelCaseWord[0].toUpperCase() + camelCaseWord.slice(1)
}

export default class BaseModel {
  constructor (data = {}) {
    this.pk = null
    let baseValues = this.defaultValues()

    Object.keys(baseValues).forEach(key => {
      this[camelCase(key)] = baseValues[key]
    })

    this.fromJson(data)
  }

  fromJson (data) {
    Object.keys(data).forEach(key => {
      let name = cleanMethodName(key)
      if (typeof this[name] === 'function') {
        this[name](data[key])
      } else {
        this[camelCase(key)] = data[key]
      }
    })
  }
}
