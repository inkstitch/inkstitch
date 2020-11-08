'use strict'

import {app, BrowserWindow, ipcMain, dialog, shell} from 'electron'
var fs = require('fs');
var path = require('path');
var tmp = require('tmp');

const url = require('url')

/**
 * Set `__static` path to static files in production
 * https://simulatedgreg.gitbooks.io/electron-vue/content/en/using-static-assets.html
 */
if (process.env.NODE_ENV === 'development') {
  // we were run as electron --inspect=5858 path/to/main.js <args>
  // so get rid of the first two args
  console.log("args " + process.argv)
  process.argv.shift()
  process.argv.shift()
} else {
  global.__static = path.join(__dirname, '/static').replace(/\\/g, '\\\\')
}

let mainWindow

var target = process.argv[1] || "";
var targetURL = url.parse(target)
var winURL = null;

// Print PDF will give us a full URL to a flask server, bypassing Vue entirely.
// Eventually this will be migrated to Vue.
if (targetURL.protocol) {
  winURL = target
} else {
  if (process.env.NODE_ENV === 'development') {
    winURL = `http://localhost:9080/?${targetURL.query || ""}#${targetURL.pathname || ""}`
  } else {
    winURL = `file://${__dirname}/index.html?${targetURL.query || ""}#${targetURL.pathname || ""}`;
  }
}

function createWindow() {
  /**
   * Initial window options
   */
  mainWindow = new BrowserWindow({
    height: 563,
    useContentSize: true,
    width: 1000,
    webPreferences: {nodeIntegration: true}
  })

  mainWindow.loadURL(winURL)
  mainWindow.maximize()

  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

app.on('ready', createWindow)

app.on('window-all-closed', () => {
    app.quit()
})

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})

ipcMain.on('save-pdf', function (event, pageSize) {
    mainWindow.webContents.printToPDF({"pageSize": pageSize}, function(error, data) {
        dialog.showSaveDialog(mainWindow, {"defaultPath": "inkstitch.pdf"}, function(filename, bookmark) {
            if (typeof filename !== 'undefined')
                fs.writeFileSync(filename, data, 'utf-8');
        })
    })
})

ipcMain.on('open-pdf', function (event, pageSize) {
    mainWindow.webContents.printToPDF({"pageSize": pageSize}, function(error, data) {
        tmp.file({keep: true, discardDescriptor: true}, function(err, path, fd, cleanupCallback) {
            fs.writeFileSync(path, data, 'utf-8');
            shell.openItem(path);
        })
    })
})


/**
 * Auto Updater
 *
 * Uncomment the following code below and install `electron-updater` to
 * support auto updating. Code Signing with a valid certificate is required.
 * https://simulatedgreg.gitbooks.io/electron-vue/content/en/using-electron-builder.html#auto-updating
 */

/*
import { autoUpdater } from 'electron-updater'

autoUpdater.on('update-downloaded', () => {
  autoUpdater.quitAndInstall()
})

app.on('ready', () => {
  if (process.env.NODE_ENV === 'production') autoUpdater.checkForUpdates()
})
 */
