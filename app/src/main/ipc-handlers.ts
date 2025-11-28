import { ipcMain } from 'electron'
import axios from 'axios'

ipcMain.handle('analyze-file', async (_event, filePath: string) => {
  const response = await axios.post('http://127.0.0.1:7777/analyze', { path: filePath })
  return response.data
})
