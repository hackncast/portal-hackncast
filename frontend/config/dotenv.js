'use strict'

const Dotenv = require('dotenv-webpack')

module.exports = new Dotenv({
  path: './.env',
  safe: true,
  systemvars: true,
  silent: false
})
