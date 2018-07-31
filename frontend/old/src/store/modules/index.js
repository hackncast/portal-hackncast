const modules = {}
const requireModule = require.context('.', true, /index\.js$/)

requireModule.keys().forEach(fileName => {
  if (fileName === './index.js') return

  let moduleName = fileName.split('/')[1]
  moduleName = moduleName[0].toUpperCase() + moduleName.substring(1)
  modules[moduleName] = requireModule(fileName).default
})

export default modules
