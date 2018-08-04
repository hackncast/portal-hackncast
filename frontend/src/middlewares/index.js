const middlewares = {}
const requireModule = require.context('.', false, /\.js$/)

requireModule.keys().forEach(fileName => {
  if (fileName === './index.js') return

  let name = fileName.replace(/\.js$/, '').replace(/^\.\//, '')
  let module = requireModule(fileName)
  middlewares[name] = module.default
})

export default middlewares
