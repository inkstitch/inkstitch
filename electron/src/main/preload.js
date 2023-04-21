const { contextBridge, ipcRenderer } = require ('electron')

contextBridge.exposeInMainWorld('inkstitchAPI', {
  savepdf: (pageSize) => { ipcRenderer.send('save-pdf', pageSize) },
  openpdf: (pageSize) => { ipcRenderer.send('open-pdf', pageSize) },
})
