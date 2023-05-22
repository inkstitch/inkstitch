'use strict'

const loadEnv = require('../utils/loadEnv')
loadEnv()
loadEnv('development')
const chalk = require('chalk')
const webpack = require('webpack')
const WebpackDevServer = require('webpack-dev-server')
const { info } = require('../utils/logger')
const getLocalIP = require('../utils/getLocalIP')
const devWebpackConfig = require('../config/dev')
const devServerOptions = devWebpackConfig.devServer
const { spawn } = require('node:child_process')
const electron = require('electron')
const path = require('path')
const url = require('url')
const fs = require('fs');

let electronProcess = null
let manualRestart = false
// disable warnings in browser console
process.env['ELECTRON_DISABLE_SECURITY_WARNINGS'] = 'false'

const protocol = devServerOptions.https ? 'https' : 'http'
const host = devServerOptions.host || '0.0.0.0'
const port = devServerOptions.port || 8080

// older code that sets the url for the path I would assume
var parseArg = process.argv[2] || ""
var yarnArg = url.parse(parseArg)

function resetPort() {
  let resetData = { "_comment1": "port should not be declared when commiting" }
  fs.writeFileSync(path.join(__dirname, "../../src/lib/flaskserverport.json"),  JSON.stringify(resetData), 'utf8')
  console.log("Resetting the flaskport")
}

function startElectron(webpackport) {
var wbport = webpackport
  // this sends url to proper position
  process.argv.shift()
  process.argv.shift()
  // get URL from PrintPDF
  // checks if url is http
  if (yarnArg.protocol) {
    var args = [
          '--inspect=5858',
          path.join(__dirname, '../../dist/electron/main.js')
      ].concat(process.argv)
  } else {
      var args = [
          '--inspect=5858',
          `http://0.0.0.0:${wbport}/#${process.argv}`
      ].concat(process.argv)
  }
  // detect yarn or npm and process commandline args accordingly
  if (process.env.npm_execpath.endsWith('yarn.js')) {
        args = args.concat(process.argv.slice(3))
     } else if (process.env.npm_execpath.endsWith('npm-cli.js')) {
        args = args.concat(process.argv.slice(2))
     }
    electronProcess = spawn(electron, args)
    electronProcess.on('close', () => {
    if (!manualRestart) {
        process.exit()
    } else {
        process.kill(electronProcess.pid)
    }
    resetPort()
  })
  electronProcess.on('exit', () => {
    resetPort()
  })
}

info('Starting development server...')
const compiler = webpack(devWebpackConfig)
const server = new WebpackDevServer(devServerOptions, compiler)

compiler.hooks.done.tap('serve', (stats) => {
  console.log()
  console.log()
  console.log(`App running at:`)
  console.log(`  - Local:   ${chalk.cyan(`${protocol}://${host}:${port}`)}`)
  console.log(`  - Network: ${chalk.cyan(`${protocol}://${getLocalIP()}:${port}`)}`)
  console.log()

 // allows livereload for webpack devserver to work without multiple instances of electron
 if (electronProcess) {
     manualRestart = true
  } else {
    manualRestart = false
     // starts nodejs electron commandline browser
     startElectron(devServerOptions.port)
    } 
})

server.start(port, host, (err) => {
  if (err) {
    process.exit(0)
  }
})
