import { app, BrowserWindow, ipcMain, dialog, shell } from 'electron';
const process = require('process');
const fs = require('fs');
const path = require('path')
const tmp = require('tmp')

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow;

const createWindow = () => {
  if (process.argv[1] == ".") {
	  // we were run in development mode with `electron . <url>`
	  process.argv.shift();
	  var isDev = true;
  }
  
  var url = process.argv[1];
  process.argv.shift();

  
  if (url.indexOf("://") == -1) {
	  url = `file://${__dirname}/${url}`;
  }

	
  mainWindow = new BrowserWindow({show: false,
	                              icon: path.join(__dirname, 'assets/icons/png/512x512.png'),
	                              webPreferences: {nodeIntegration: true}});
  mainWindow.once('ready-to-show', () => {
	  mainWindow.show()
	  mainWindow.maximize();
	  if (isDev)
    	    mainWindow.webContents.openDevTools()
  })

  
  mainWindow.loadURL(url);

  //mainWindow.webContents.openDevTools();
  
  // Emitted when the window is closed.
  mainWindow.on('closed', () => {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    mainWindow = null;
  });
};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow);

// Quit when all windows are closed.
app.on('window-all-closed', () => {
    app.quit();
});

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
