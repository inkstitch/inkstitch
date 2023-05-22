/*
 * Authors: see git history
 *
 * Copyright (c) 2010 Authors
 * Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
 *
 */

'use strict'

const path = require('path')
const fs = require('fs')
const tmp = require('tmp')
const url = require('url')
const { app, BrowserWindow, ipcMain, dialog, shell, Menu} = require('electron')
// url for printPDF flask server which is used in development and production mode

var port = process.env.FLASKPORT
const printPdfUrl = `http://127.0.0.1:${port}/`

const isDev = process.env.BABEL_ENV === 'development'

var target = null
// Finds this url in the argv array and sets to target value
if (process.argv.includes(printPdfUrl)) {
    target = printPdfUrl
} else {
    target = process.argv[1] || "";
}
var targetURL = url.parse(target)
var winURL = null

// Eventually this will be migrated to Vue.
if (targetURL.protocol) {
    winURL = target
} else {
    winURL = `file://${__dirname}/index.html?${targetURL.query || ""}#${targetURL.pathname || ""}`
}

function createWindow() {
    const mainWindow = new BrowserWindow({
        useContentSize: true,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: false,
            contextIsolation: true,
        },
    })
    if (isDev) {
        // printPDF in development mode will have dev tools activated
        // Vuejs parts of Ink/Stich will not and dev tools must be accessed though the menu of electron window
        mainWindow.loadURL(winURL)
        mainWindow.webContents.openDevTools()
    } else {
        mainWindow.loadURL(winURL)
    }
    // This will remove the menu from the release, in dev mode the menu is available.
    if(process.platform === "darwin" && !isDev) {
        Menu.setApplicationMenu(Menu.buildFromTemplate([]));
    } if(process.platform === "win32" || process.platform === "linux" && !isDev) {
        mainWindow.removeMenu();
    }
    mainWindow.maximize()
    // save to PDF
    ipcMain.on('save-pdf', (event, pageSize) => {
      const webContents = event.sender
      const win = BrowserWindow.fromWebContents(webContents)
      const saveOpt = {
        title: "Save PDF",
        defaultPath: "Inkstitch.pdf",
        bookmark: "true",
      }
      win.webContents.printToPDF({}).then(pageSize => {
         dialog.showSaveDialog(saveOpt).then(filename => {
           const { filePath } = filename;
           fs.writeFileSync(filePath, pageSize, (error) => {
             if (error) {
               throw error
             }
             console.log(`Wrote PDF successfully to ${pdfPath}`)
          })
        }).catch(error => {
        console.log(`Failed to write PDF to ${pdfPath}: `, error)
        })
      })
    })
    // openPDF
    ipcMain.on('open-pdf', (event, pageSize) => {
      const webContents = event.sender
      const win = BrowserWindow.fromWebContents(webContents)
      win.webContents.printToPDF({}).then(pageSize => {
        tmp.file({keep: true, discardDescriptor: true}, function(err, path, fd, cleanupCallback) {
                fs.writeFileSync(path, pageSize, 'utf-8');
                shell.openPath(path);
            })
        })
    })
}

app.whenReady().then(() => {
    createWindow()
    app.on('activate', () => {
        if(BrowserWindow.getAllWindows().length === 0)  {
            createWindow()
        }
    })
})

app.on('window-all-closed', () => {
    app.quit()
})
