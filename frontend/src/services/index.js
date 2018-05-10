const modules = {}
const requireModule = require.context('.', false, /\.js$/)

requireModule.keys().forEach(fileName => {
  if (fileName === './index.js') return

  const moduleName = fileName.split('/')[1].replace('.js', '')
  modules[moduleName] = requireModule(fileName).default
})

export default modules
