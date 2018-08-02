const BACKEND = process.env.BACKEND ? process.env.BACKEND : 'http://localhost:8000'
const proxyOpts = { target: BACKEND, ws: true, changeOrigin: true }

console.log('PROXYING', proxyOpts)

module.exports = {
  baseUrl: '/admin/',
  devServer: {
    disableHostCheck: true,
    proxy: {
      '/api': proxyOpts,
      '/media': proxyOpts,
      '/static': proxyOpts
    }
  }
}
