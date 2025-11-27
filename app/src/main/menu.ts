import { Menu, MenuItemConstructorOptions, shell } from "electron";

export function createAppMenu(): void {
  const template: MenuItemConstructorOptions[] = [
    {
      label: "AION",
      submenu: [
        {
          label: "GitHub",
          click: () => shell.openExternal("https://github.com"),
        },
        { role: "quit", label: "Quit" },
      ],
    },
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}
