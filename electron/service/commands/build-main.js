'use strict'

const loadEnv = require('../utils/loadEnv')
loadEnv()
loadEnv('production')

const rm = require('rimraf')
const webpack = require('webpack')

const { error, done } = require('../utils/logger')
const { logWithSpinner, stopSpinner } = require('../utils/spinner')
const paths = require('../utils/paths')
// after renderer is built, main is next to build
const webpackConfig = require('../config/main')
const config = require('../project.config')

logWithSpinner('Building for production...')
// removed rm function to prevent the deletion of renderer
webpack(webpackConfig, (err, stats) => {
    stopSpinner(false)

    if (err) throw err

    process.stdout.write(
      stats.toString({
        colors: true,
        modules: false,
        children: false,
        chunks: false,
        chunkModules: false,
      }) + '\n\n'
    )

    if (stats.hasErrors()) {
      error('Build failed with errors.\n')
      process.exit(1)
    }

    done('Build complete.\n')
})

