'use strict'

const loadEnv = require('../utils/loadEnv')
loadEnv()
loadEnv('production')

const rm = require('rimraf')
const webpack = require('webpack')

const { error, done } = require('../utils/logger')
const { logWithSpinner, stopSpinner } = require('../utils/spinner')
const paths = require('../utils/paths')
// build renderer first
const webpackConfig = require('../config/renderer')
const config = require('../project.config')

logWithSpinner('Building for production...')

rm(paths.resolve(config.outputDir), (err) => {
  if (err) throw err

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
})
