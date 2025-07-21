const { app, BrowserWindow, dialog, shell } = require('electron')
const Store = require('electron-store')
const path = require('path')

const store = new Store()

function createWindow () {
  const bounds = store.get('windowBounds') || { width: 1400, height: 900 }
  const win = new BrowserWindow({
    width: bounds.width,
    height: bounds.height,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  })

  // Persist window size
  win.on('resize', () => {
    store.set('windowBounds', win.getBounds())
  })

  // On first run, ask where backend is
  let backendUrl = store.get('backendUrl')
  if (!backendUrl) {
    backendUrl = 'http://localhost:5173'
    store.set('backendUrl', backendUrl)
  }

  win.loadURL(backendUrl)

  win.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url)
    return { action: 'deny' }
  })
}

app.whenReady().then(() => {
  createWindow()

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})
