'use strict'

const { DefinePlugin, EnvironmentPlugin } = require('webpack')
const { VueLoaderPlugin } = require('vue-loader')
const CaseSensitivePathsPlugin = require('case-sensitive-paths-webpack-plugin')
const HTMLPlugin = require('html-webpack-plugin')
const { VuetifyPlugin } = require('webpack-plugin-vuetify')

const resolveClientEnv = require('../utils/resolveClientEnv')
const paths = require('../utils/paths')

const config = require('../project.config')

const isProd = process.env.NODE_ENV === 'production'

module.exports = {
  context: process.cwd(),

  output: {
    path: paths.resolve(config.outputDir),
    publicPath: config.dev.publicPath,
    filename: '[name].js',
  },

  resolve: {
    alias: {
      '@': paths.resolve('src'),
    },
    extensions: ['.ts', '.tsx', '.js', '.jsx', '.vue', '.json', '.html', '.ejs'],
  },

  plugins: [
    new VueLoaderPlugin(),
    new EnvironmentPlugin(['NODE_ENV']),
    new CaseSensitivePathsPlugin(),
    new HTMLPlugin({ 
      template: paths.resolve('src/index.html'),
      templateParameters: {
        ...resolveClientEnv(
          { publicPath: isProd ? config.build.publicPath : config.dev.publicPath },
          false /* raw */
        ),
      },
    }),
    new VuetifyPlugin({ autoImport: true }),
    new DefinePlugin({
      // vue3 feature flags <http://link.vuejs.org/feature-flags>
      __VUE_OPTIONS_API__: 'true',
      __VUE_PROD_DEVTOOLS__: 'false',
      
      ...resolveClientEnv({
        publicPath: isProd ? config.build.publicPath : config.dev.publicPath,
      }),
    }),
  ],
  
  module: {
    noParse: /^(vue|vue-router)$/,

    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader',
      },
      // babel
      {
        test: /\.m?jsx?$/,
        exclude: (file) => {
          // always transpile js in vue files
          if (/\.vue\.jsx?$/.test(file)) {
            return false
          }
          // Don't transpile node_modules
          return /node_modules/.test(file)
        },
        use: ['thread-loader', 'babel-loader'],
      },

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

      // images
      {
        test: /\.(png|jpe?g|gif|webp)(\?.*)?$/,
        type: 'asset',
        generator: { filename: 'img/[contenthash:8][ext][query]' },
      },

      // do not base64-inline SVGs.
      // https://github.com/facebookincubator/create-react-app/pull/1180
      {
        test: /\.(svg)(\?.*)?$/,
        type: 'asset/resource',
        generator: { filename: 'img/[contenthash:8][ext][query]' },
      },

      // media
      {
        test: /\.(mp4|webm|ogg|mp3|wav|flac|aac)(\?.*)?$/,
        type: 'asset',
        generator: { filename: 'media/[contenthash:8][ext][query]' },
      },

      // fonts
      {
        test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/i,
        type: 'asset',
        generator: { filename: 'fonts/[contenthash:8][ext][query]' },
      },
    ],
  },
}
