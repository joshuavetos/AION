import { ipcMain } from "electron";

async function postToDaemon(path: string) {
  const response = await fetch("http://127.0.0.1:7777/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ path }),
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`Daemon returned ${response.status}: ${detail}`);
  }

  return response.json();
}

export function registerIpcHandlers() {
  ipcMain.handle("analyze-file", async (_event, filePath: string) => {
    return postToDaemon(filePath);
  });
}
