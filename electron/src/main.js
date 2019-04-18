import { app, BrowserWindow, ipcMain, dialog } from 'electron';
var fs = require('fs');
var path = require('path')
var tmp = require('tmp')

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow;

const createWindow = () => {
  // Create the browser window.
  mainWindow = new BrowserWindow({icon: path.join(__dirname, 'assets/icons/png/512x512.png')});

  mainWindow.maximize();

  // and load the index.html of the app.
  if (process.argv[1] == ".") {
	  // run in development mode with `electron . <url>`
	  var url = process.argv[2];
  } else {
	  var url = process.argv[1];
  }
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

ipcMain.on('print', function (event, pageSize) {
	mainWindow.webContents.printToPDF({"pageSize": pageSize}, function(error, data) {
		dialog.showSaveDialog(mainWindow, {"defaultPath": "inkstitch.pdf"}, function(filename, bookmark) {
			if (typeof filename !== 'undefined')
				fs.writeFileSync(filename, data, 'utf-8');
		})
	})
})