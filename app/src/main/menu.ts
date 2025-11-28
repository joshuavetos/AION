import { Menu } from 'electron'

const template: Electron.MenuItemConstructorOptions[] = [
  {
    label: 'File',
    submenu: [{ role: 'quit' }]
  },
  {
    label: 'View',
    submenu: [{ role: 'reload' }, { role: 'toggledevtools' }]
  }
]

Menu.setApplicationMenu(Menu.buildFromTemplate(template))
