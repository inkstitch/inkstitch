'use strict'
const prefixRE = /^VUE_APP_/

module.exports = function resolveClientEnv(options, raw) {
  process.env.PUBLIC_PATH = options.publicPath

  if (raw) {
    return env
  }

}