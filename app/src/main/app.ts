import { app, BrowserWindow } from 'electron'
import path from 'path'

import './ipc-handlers'
import './menu'

const createWindow = async () => {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    backgroundColor: '#090909',
    webPreferences: {
      preload: path.join(__dirname, 'preload.ts'),
      contextIsolation: true,
      nodeIntegration: false
    }
  })

  const devServerUrl = process.env.VITE_DEV_SERVER_URL || 'http://localhost:5173'
  await win.loadURL(devServerUrl)
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
})
