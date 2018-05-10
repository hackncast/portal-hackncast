const modules = {}
const requireModule = require.context('.', false, /\.js$/)

requireModule.keys().forEach(fileName => {
  if (fileName === './index.js') return

  const moduleName = fileName.split('/')[1].replace('.js', '')
  modules[moduleName] = requireModule(fileName).default
})

modules['initialize'] = function initialize () {
  Object.keys(modules).forEach(name => {
    if (name === 'Base' || !modules[name].initialize) return
    modules[name].initialize()
  })
}

export default modules
