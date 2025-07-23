const { app, BrowserWindow } = require('electron');
const path = require('path');
// Auto-launch backend server (if packaged as part of app)
const { spawn } = require('child_process');

let mainWindow;
let backendProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  });
  // Load the frontend (in dev, local server; in prod, local file)
  if (process.env.ELECTRON_DEV) {
    mainWindow.loadURL('http://localhost:3000');
  } else {
    mainWindow.loadFile(path.join(__dirname, '../frontend/index.html'));
  }
}

function startBackend() {
  // In packaged app, spawn the Python backend (assuming it's bundled or installed)
  // For example, using a bundled Python or running uvicorn.
  try {
    backendProcess = spawn('uvicorn', ['backend.main:app', '--host', '127.0.0.1', '--port', '8000']);
    backendProcess.stdout.on('data', data => console.log(`BACKEND: ${data}`));
    backendProcess.stderr.on('data', data => console.error(`BACKEND ERR: ${data}`));
  } catch (e) {
    console.error("Failed to start backend:", e);
  }
}

app.whenReady().then(() => {
  if (!process.env.ELECTRON_DEV) {
    startBackend();
  }
  createWindow();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

// Gracefully quit backend process on exit
app.on('window-all-closed', () => {
  if (backendProcess) backendProcess.kill();
  if (process.platform !== 'darwin') app.quit();
});
