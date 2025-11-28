<script setup lang="ts">
import { ref, computed } from 'vue'

type AionBridge = {
  analyzeFile: (path: string) => Promise<{
    integrity_score: number
    entropy: number
    contradictions: string[]
    receipt: { hash: string; merkle_root: string; signature: string }
  }>
}

const bridge = (window as unknown as { aion: AionBridge }).aion

const filePath = ref('')
const integrity = ref<number | null>(null)
const entropy = ref(0)
const contradictions = ref<string[]>([])
const receipt = ref<{ hash: string; merkle_root: string; signature: string } | null>(null)
const error = ref('')
const loading = ref(false)

const entropyColor = computed(() => {
  if (entropy.value < 0.5) return '#00c853'
  if (entropy.value < 1.5) return '#ffb300'
  return '#ff5252'
})

const handleDrop = async (event: DragEvent) => {
  event.preventDefault()
  const files = event.dataTransfer?.files
  if (!files || files.length === 0) return
  filePath.value = files[0].path
  await analyze()
}

const analyze = async () => {
  if (!filePath.value) return
  loading.value = true
  error.value = ''
  try {
    const result = await bridge.analyzeFile(filePath.value)
    integrity.value = result.integrity_score
    entropy.value = result.entropy
    contradictions.value = result.contradictions
    receipt.value = result.receipt
  } catch (err: unknown) {
    error.value = err instanceof Error ? err.message : 'Analysis failed'
    integrity.value = null
    entropy.value = 0
    contradictions.value = []
    receipt.value = null
  } finally {
    loading.value = false
  }
}

const preventDefaults = (event: DragEvent) => {
  event.preventDefault()
}

const exportReceipt = () => {
  if (!receipt.value) return
  const blob = new Blob([JSON.stringify(receipt.value, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = 'forensic-receipt.json'
  anchor.click()
  URL.revokeObjectURL(url)
}
</script>

<template>
  <div class="shell">
    <header>
      <div>
        <h1>The Epistemic Firewall</h1>
        <p>Drag a .txt file to analyze integrity, entropy, and contradictions.</p>
      </div>
      <button class="export" :disabled="!receipt" @click="exportReceipt">Export Forensic Receipt</button>
    </header>

    <main>
      <section
        class="dropzone"
        @drop="handleDrop"
        @dragover="preventDefaults"
        @dragenter="preventDefaults"
      >
        <p v-if="!filePath">Drop a .txt file here</p>
        <p v-else>Ready to analyze: {{ filePath }}</p>
        <button class="analyze" :disabled="!filePath || loading" @click="analyze">
          {{ loading ? 'Analyzing...' : 'Analyze File' }}
        </button>
        <p v-if="error" class="error">{{ error }}</p>
      </section>

      <section class="metrics">
        <div class="score">
          <div class="circle">
            <span v-if="integrity !== null">{{ integrity }}%</span>
            <span v-else>--</span>
          </div>
          <p>Integrity Score</p>
        </div>

        <div class="entropy">
          <div class="label">Entropy</div>
          <div class="bar">
            <div class="fill" :style="{ width: Math.min(entropy * 50, 100) + '%', background: entropyColor }"></div>
          </div>
          <div class="value">{{ entropy.toFixed(2) }}</div>
        </div>

        <div class="contradictions">
          <div class="label">Contradictions</div>
          <ul>
            <li v-if="contradictions.length === 0">No contradictions detected.</li>
            <li v-for="item in contradictions" :key="item">{{ item }}</li>
          </ul>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
.shell {
  background: radial-gradient(circle at 10% 20%, rgba(255, 0, 0, 0.08), transparent 40%),
    radial-gradient(circle at 90% 10%, rgba(255, 255, 255, 0.05), transparent 30%),
    #0c0c0f;
  color: #f5f5f5;
  min-height: 100vh;
  padding: 32px;
  font-family: 'Inter', system-ui, sans-serif;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

h1 {
  margin: 0;
  font-size: 28px;
}

p {
  margin: 6px 0 0;
  color: #c8c8d0;
}

main {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 20px;
}

.dropzone {
  border: 2px dashed #ff0044;
  border-radius: 16px;
  padding: 24px;
  background: rgba(255, 0, 68, 0.08);
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 220px;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.dropzone p {
  color: #fff;
}

button {
  border: none;
  cursor: pointer;
}

.analyze {
  background: linear-gradient(135deg, #ff1744, #ff6d00);
  color: #fff;
  padding: 12px 18px;
  border-radius: 12px;
  font-weight: 700;
  letter-spacing: 0.5px;
  transition: transform 0.1s ease, box-shadow 0.2s ease;
}

.analyze:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.analyze:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 25px rgba(255, 71, 87, 0.25);
}

.error {
  color: #ff8a80;
  font-size: 14px;
}

.metrics {
  background: #111118;
  border: 1px solid #1d1d24;
  border-radius: 16px;
  padding: 20px;
  display: grid;
  gap: 16px;
}

.score {
  display: flex;
  align-items: center;
  gap: 16px;
}

.circle {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  border: 4px solid #ff0044;
  display: grid;
  place-items: center;
  font-size: 22px;
  font-weight: 800;
  background: radial-gradient(circle at 50% 50%, rgba(255, 0, 68, 0.2), rgba(0, 0, 0, 0.7));
}

.entropy {
  display: grid;
  gap: 8px;
}

.label {
  text-transform: uppercase;
  font-size: 12px;
  color: #9fa1b5;
  letter-spacing: 1px;
}

.bar {
  height: 10px;
  background: #1d1d24;
  border-radius: 6px;
  overflow: hidden;
}

.fill {
  height: 100%;
  transition: width 0.2s ease;
}

.value {
  font-weight: 700;
}

.contradictions ul {
  margin: 0;
  padding-left: 16px;
  color: #e8e8f0;
  display: grid;
  gap: 6px;
}

.export {
  background: transparent;
  border: 1px solid #ff0044;
  color: #ff9fb0;
  padding: 10px 16px;
  border-radius: 12px;
}

.export:disabled {
  opacity: 0.5;
  border-color: #555;
  color: #777;
}

@media (max-width: 900px) {
  main {
    grid-template-columns: 1fr;
  }
}
</style>
