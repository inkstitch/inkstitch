'use strict'

const path = require('path')

// gen absolute path
exports.resolve = (...args) => path.posix.join(process.cwd(), ...args)
