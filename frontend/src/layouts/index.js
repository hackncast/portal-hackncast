const modules = {}
const requireModule = require.context('.', false, /\.vue$/)

requireModule.keys().forEach(name => {
  const registerName = name.replace('./', '').replace('.vue', '')
  modules[registerName] = requireModule(name).default
})

export const meta = {
  'public': { layout: 'Public' },
  'publicMayAuth': { layout: 'Public', mayRequiresAuth: true },
  'dashboard': { layout: 'Dashboard', requiresAuth: true },
  'userProfile': { layout: 'UserProfile', requiresAuth: true }
}

export default modules
