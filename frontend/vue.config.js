const path = require('path');
const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    devtool: 'source-map',
    resolve: {
      alias: {
        'my-library-management-system': path.resolve(__dirname, 'src/')
      }
    }
  }
})
