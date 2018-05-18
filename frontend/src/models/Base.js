import camelCase from 'lodash/camelCase'

export default class BaseModel {
  constructor (data = {}) {
    Object.keys(data).forEach(key => { this[key] = data[key] })
  }

  static initialize () {
    this.service.use(this)
    this.prototype.service = this.service
  }

  static fromJson (data) {
    let newData = {}
    Object.keys(data).forEach(key => { newData[camelCase(key)] = data[key] })
    return new this(newData)
  }

  delete () {
    return this.service.delete(this)
  }
}
