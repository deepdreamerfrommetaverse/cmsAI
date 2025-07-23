const { app } = require('electron');
const { autoUpdater } = require('electron-updater');

// Set up auto-update events
autoUpdater.on('update-available', () => {
  console.log('Update available');
});
autoUpdater.on('update-downloaded', () => {
  console.log('Update downloaded, will install now');
  autoUpdater.quitAndInstall();
});

// Check for updates on startup
function checkForUpdates() {
  autoUpdater.checkForUpdates().catch(err => console.error('Update check failed:', err));
}

module.exports = { checkForUpdates };
