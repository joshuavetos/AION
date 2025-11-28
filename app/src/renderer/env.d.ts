export {}

declare global {
  interface Window {
    aion: {
      analyzeFile: (path: string) => Promise<any>
    }
  }
}
