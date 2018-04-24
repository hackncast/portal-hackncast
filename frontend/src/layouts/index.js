const modules = {}
const requireModule = require.context('.', false, /\.vue$/)

requireModule.keys().forEach(name => {
  const registerName = name.replace('./', '').replace('.vue', '')
  modules[registerName] = requireModule(name).default
})

export default modules
