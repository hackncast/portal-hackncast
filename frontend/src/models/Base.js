import camelCase from 'lodash/camelCase'

export default class BaseModel {
  constructor (data = {}) {
    for (let attr in data) {
      this[attr] = data[attr]
    }
  }

  static initialize () {
    this.service.use(this)
    this.prototype.service = this.service
  }

  static fromJson (data) {
    let newData = {}
    for (let key in data) {
      newData[camelCase(key)] = data[key]
    }
    return new this(newData)
  }

  delete () {
    return this.service.delete(this)
  }
}
