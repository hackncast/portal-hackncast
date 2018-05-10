import { ApiHelper } from '@/plugins/Api'
import { ModelIsTransient } from '@/exceptions'

export default class BaseService {
  static api = new ApiHelper()

  static use (model) {
    this.__model = model

    if (!this.__endpoint || !this.__endpoint.context) return

    let detailName = this.__endpoint.detail || null
    if (!detailName && this.__endpoint.name) {
      detailName = this.__endpoint.name + 'Detail'
    }
    if (detailName) {
      this.__detail = this.api[this.__endpoint.context][detailName]
    }

    let listName = this.__endpoint.list || null
    if (!listName && this.__endpoint.name) {
      listName = this.__endpoint.name + 'List'
    }
    if (listName) {
      this.__list = this.api[this.__endpoint.context][listName]
    }
  }

  static get (pk) {
    return new Promise((resolve, reject) => {
      this.__detail.query({ pk })
        .then(data => data.json())
        .then(data => resolve(this.__model.fromJson(data)))
        .catch(err => { reject(err) })
    })
  }

  static all () {
    return new Promise((resolve, reject) => {
      this.__list.query()
        .then(data => data.json())
        .then(data => {
          let list = []
          for (let item of data) { list.push(this.__model.fromJson(item)) }
          return resolve(list)
        })
        .catch(err => { reject(err) })
    })
  }

  static delete (object) {
    return new Promise((resolve, reject) => {
      if (!object.pk) {
        reject(new ModelIsTransient(
          'Can\'t delete a transient model instance'
        ))
      }

      this.__detail.delete({ pk: object.pk })
        .then(data => resolve(data))
        .catch(err => reject(err))
    })
  }
}
