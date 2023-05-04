require('dotenv').config({ path: path.join(__dirname, '.env') });
const path = require('path');
const { autoUpdater } = require("electron-updater");
const { app, BrowserWindow, globalShortcut, screen } = require('electron');

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    frame: false, // Make the window borderless
    show: false, // Initially hide the window
    webPreferences: { preload: path.join(__dirname, 'preload.js') }
  });

  win.loadURL(`${process.env.BACKEND_URL}`);
  return win;
}

function checkForUpdates() {
  autoUpdater.checkForUpdatesAndNotify();
}

app.whenReady().then(() => {
  const win = createWindow();
  let isToggled = false;

  const bringToFrontAndCenter = () => {
    isToggled = !isToggled;
  
    if (isToggled) {
      const cursorPos = screen.getCursorScreenPoint();
      const currentDisplay = screen.getDisplayNearestPoint(cursorPos);
      const { width, height } = currentDisplay.workAreaSize;
      const { x, y } = currentDisplay.bounds;
  
      const xPos = x + Math.round((width - 800) / 2);
      const yPos = y + Math.round((height - 600) / 2);
  
      win.setPosition(xPos, yPos);
      win.setAlwaysOnTop(true);
      win.show();
    } else {
      win.setAlwaysOnTop(false);
      win.hide();
    }
  };
  
  
  

  globalShortcut.register('CommandOrControl+K', bringToFrontAndCenter);

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
      checkForUpdates();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('will-quit', () => {
  // Unregister the shortcut to avoid memory leaks
  globalShortcut.unregisterAll();
});
