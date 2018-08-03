const BASE_URL = process.env.BASE_URL ? process.env.BASE_URL : undefined
const BACKEND = process.env.BACKEND ? process.env.BACKEND : 'http://localhost:8000'
const proxyOpts = { target: BACKEND, ws: true, changeOrigin: true }

console.log('PROXYING', proxyOpts)

module.exports = {
  baseUrl: BASE_URL,
  devServer: {
    disableHostCheck: true,
    proxy: {
      '/api': proxyOpts,
      '/media': proxyOpts,
      '/static': proxyOpts
    }
  }
}
