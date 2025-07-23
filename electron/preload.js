const { contextBridge } = require('electron');
// Expose any needed Node functionality to the renderer
contextBridge.exposeInMainWorld('myAPI', {
  // Example: can expose a function to check for updates or communicate with main
});
