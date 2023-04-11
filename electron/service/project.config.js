'use strict'

module.exports = {
    // orginal was dist
  outputDir: 'dist/electron',

  dev: {
    publicPath: '/',
    port: 8080,
  },

  build: {
      // orginal was /
    publicPath: './',
  },
}
