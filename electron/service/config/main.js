'use strict'

const CaseSensitivePathsPlugin = require('case-sensitive-paths-webpack-plugin')
const config = require('../project.config')

const resolveClientEnv = require('../utils/resolveClientEnv')
const paths = require('../utils/paths')
const { merge } = require('webpack-merge')
const TerserPlugin = require('terser-webpack-plugin')
const cssWebpackConfig = require('./css')
const terserOptions = require('./terserOptions')
const isProd = process.env.NODE_ENV === 'production'

module.exports = merge(cssWebpackConfig, {
  context: process.cwd(),
    mode: 'production',
  entry: {
    main: './src/main/index.js',
    preload: './src/main/preload.js',
  },
  
  node: {
    __dirname: false,
  },
  
  optimization: {
    minimize: true,
    minimizer: [new TerserPlugin(terserOptions())],
    moduleIds: 'named',
  },
  target: ['electron-main'],

  output: {
    path: paths.resolve(config.outputDir),
    publicPath: config.dev.publicPath,
    filename: '[name].js',
  },

  resolve: {
    alias: {
      '@': paths.resolve('src'),
    },
    extensions: ['.ts', '.tsx', '.js', '.jsx', '.vue', '.json', 'html', 'ejs'],
  },

  plugins: [
    new CaseSensitivePathsPlugin(),
  ],

  module: {
    noParse: /^(vue|vue-router)$/,

    rules: [
      // ts
      {
        test: /\.tsx?$/,
        use: [
          'thread-loader',
          'babel-loader',
          {
            loader: 'ts-loader',
            options: {
              transpileOnly: true,
              appendTsSuffixTo: ['\\.vue$'],
              happyPackMode: true,
            },
          },
        ],
      },
    ],
  },
}
)