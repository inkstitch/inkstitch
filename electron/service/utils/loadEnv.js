'use strict'

const path = require('path')
const dotenv = require('dotenv')
const dotenvExpand = require('dotenv-expand')
const { error } = require('./logger')

module.exports = function loadEnv(mode) {
  const basePath = path.resolve(process.cwd(), `.env${mode ? `.${mode}` : ``}`)
  const localPath = `${basePath}.local`

  const load = (envPath) => {
    try {
      const env = dotenv.config({ path: envPath, debug: process.env.DEBUG })
      dotenvExpand.expand(env)
    } catch (err) {
      // only ignore error if file is not found
      if (err.toString().indexOf('ENOENT') < 0) {
        error(err)
      }
    }
  }

  load(localPath)
  load(basePath)

  // by default, NODE_ENV and BABEL_ENV are set to "development" unless mode
  // is production or test. However the value in .env files will take higher
  // priority.
  if (mode) {
    const defaultNodeEnv = mode === 'production' || mode === 'test' ? mode : 'development'
    if (process.env.NODE_ENV == null) {
      process.env.NODE_ENV = defaultNodeEnv
    }
    if (process.env.BABEL_ENV == null) {
      process.env.BABEL_ENV = defaultNodeEnv
    }
  }
}
