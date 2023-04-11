'use strict'

const { merge } = require('webpack-merge')

const baseWebpackConfig = require('./base')
const cssWebpackConfig = require('./css')
const config = require('../project.config')
const { ProvidePlugin, DefinePlugin } = require('webpack')


module.exports = merge(baseWebpackConfig, cssWebpackConfig, {
    entry: {
    main: './src/renderer/main.js'
    },

  mode: 'development',

  devtool: 'eval-cheap-module-source-map',
    
  devServer: {
    watchFiles: ['src/**/*'],
    historyApiFallback: {
      rewrites: [{ from: /./, to: '/index.html' }],
    },
    devMiddleware: {
      publicPath: config.dev.publicPath,
    },
    open: false,
    host: '0.0.0.0',
    port: config.dev.port,
    liveReload: true,
  },

  infrastructureLogging: {
    level: 'warn',
  },

  stats: {
    assets: false,
    modules: false,
    errorDetails: false,
  },
})
