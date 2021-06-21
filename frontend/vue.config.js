module.exports = {
  devServer: {
    proxy: 'http://backend:8000'
  },
  transpileDependencies: [
    'vuetify'
  ]
}
