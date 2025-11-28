<template>
  <div class="app">
    <header class="hero">
      <h1>AION Desktop</h1>
      <p class="subtitle">Epistemic Firewall — Dark, precise, and verifiable.</p>
    </header>

    <section class="workspace">
      <div
        class="drop-zone"
        @dragover.prevent
        @drop.prevent="handleDrop"
      >
        <p class="drop-text">Drag & Drop a .txt file to audit</p>
        <p class="hint">Path is sent via IPC to the daemon on port 7777.</p>
        <button class="select-btn" @click="triggerFileDialog">Browse Files</button>
        <input
          ref="fileInput"
          type="file"
          accept=".txt"
          class="hidden"
          @change="onFileSelected"
        />
      </div>

      <div class="results" v-if="analysis">
        <div class="score-card">
          <div class="score-circle">
            <span class="score-value">{{ analysis.integrity_score }}</span>
            <span class="score-label">Integrity</span>
          </div>
          <div class="entropy">
            <div class="entropy-header">
              <span>Entropy</span>
              <span class="entropy-value">{{ analysis.entropy.toFixed(2) }}</span>
            </div>
            <div class="entropy-bar">
              <div
                class="entropy-fill"
                :style="{ width: entropyPercent + '%', background: entropyColor }"
              ></div>
            </div>
          </div>
        </div>

        <div class="panel">
          <h2>Contradictions</h2>
          <ul v-if="analysis.contradictions.length" class="list">
            <li v-for="(item, index) in analysis.contradictions" :key="index">{{ item }}</li>
          </ul>
          <p v-else class="empty">No contradictions detected.</p>
        </div>

        <div class="panel">
          <h2>Receipt</h2>
          <pre class="receipt">{{ formattedReceipt }}</pre>
          <button class="export-btn" @click="exportReceipt">Export Forensic Receipt</button>
        </div>
      </div>
    </section>
  </div>
</template>

<script lang="ts" setup>
import { ipcRenderer } from "electron";
import { computed, ref } from "vue";

interface AnalyzeResult {
  integrity_score: number;
  entropy: number;
  contradictions: string[];
  receipt: {
    hash: string;
    merkle_root: string;
    signature: string;
  };
}

const analysis = ref<AnalyzeResult | null>(null);
const fileInput = ref<HTMLInputElement | null>(null);

const formattedReceipt = computed(() => {
  if (!analysis.value) return "";
  return JSON.stringify(analysis.value.receipt, null, 2);
});

const entropyPercent = computed(() => {
  if (!analysis.value) return 0;
  return Math.min(100, Math.round(analysis.value.entropy * 20));
});

const entropyColor = computed(() => {
  const pct = entropyPercent.value;
  if (pct < 35) return "#3dd68c";
  if (pct < 70) return "#f6c344";
  return "#e54b4b";
});

function triggerFileDialog() {
  fileInput.value?.click();
}

function onFileSelected(event: Event) {
  const target = event.target as HTMLInputElement;
  if (!target.files?.length) return;
  const file = target.files[0];
  sendFile(file.path);
}

function handleDrop(event: DragEvent) {
  const file = event.dataTransfer?.files?.[0];
  if (file) {
    sendFile((file as any).path ?? file.name);
  }
}

async function sendFile(path: string) {
  if (!path) return;
  try {
    const response = await ipcRenderer.invoke("analyze-file", path);
    analysis.value = response as AnalyzeResult;
  } catch (error: any) {
    alert(`Failed to analyze file: ${error.message ?? error}`);
  }
}

function exportReceipt() {
  if (!analysis.value) return;
  const blob = new Blob([JSON.stringify(analysis.value, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "aion-forensic-receipt.json";
  anchor.click();
  URL.revokeObjectURL(url);
}
</script>

<style scoped>
.app {
  background: radial-gradient(circle at 20% 20%, rgba(229, 75, 75, 0.08), #050508 50%);
  color: #f8f8fa;
  min-height: 100vh;
  font-family: "Inter", "SF Pro Display", system-ui, -apple-system, sans-serif;
  padding: 24px 32px 48px;
}

.hero {
  text-align: left;
  margin-bottom: 20px;
}

.hero h1 {
  font-size: 32px;
  margin: 0;
  letter-spacing: 0.5px;
}

.subtitle {
  margin-top: 8px;
  color: #9ea3b0;
}

.workspace {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

.drop-zone {
  border: 2px dashed rgba(229, 75, 75, 0.6);
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  background: rgba(12, 12, 16, 0.8);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
}

.drop-text {
  font-size: 18px;
  margin: 0 0 8px;
}

.hint {
  color: #9ea3b0;
  margin-bottom: 16px;
}

.select-btn,
.export-btn {
  background: #e54b4b;
  border: none;
  padding: 12px 20px;
  color: #fff;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s ease;
}

.select-btn:hover,
.export-btn:hover {
  background: #f76767;
}

.hidden {
  display: none;
}

.results {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 16px;
}

.score-card {
  background: linear-gradient(135deg, rgba(229, 75, 75, 0.9), rgba(12, 12, 16, 0.9));
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.45);
}

.score-circle {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  border: 6px solid rgba(255, 255, 255, 0.15);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.05), rgba(5, 5, 8, 0.8));
}

.score-value {
  font-size: 56px;
  font-weight: 800;
}

.score-label {
  color: #cfd3df;
  letter-spacing: 1px;
}

.entropy {
  margin-top: 12px;
}

.entropy-header {
  display: flex;
  justify-content: space-between;
  color: #cfd3df;
  margin-bottom: 8px;
}

.entropy-bar {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  height: 12px;
}

.entropy-fill {
  height: 100%;
  border-radius: 10px;
  transition: width 0.3s ease, background 0.3s ease;
}

.panel {
  background: rgba(12, 12, 16, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.35);
}

.panel h2 {
  margin-top: 0;
  margin-bottom: 12px;
}

.list {
  list-style: decimal inside;
  padding: 0;
  margin: 0;
  color: #f2f2f5;
  line-height: 1.5;
}

.empty {
  color: #9ea3b0;
}

.receipt {
  background: rgba(0, 0, 0, 0.4);
  padding: 12px;
  border-radius: 10px;
  color: #dcdde5;
  overflow-x: auto;
  font-size: 13px;
}

@media (min-width: 1024px) {
  .workspace {
    grid-template-columns: 1fr;
  }
}
</style>
