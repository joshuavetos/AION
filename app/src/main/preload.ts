import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('aion', {
  analyzeFile: (filePath: string) => ipcRenderer.invoke('analyze-file', filePath)
})
