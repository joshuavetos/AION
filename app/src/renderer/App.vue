<script setup>
import { ref } from 'vue'
import axios from 'axios'

const rawPrompt = ref('')
const refinedPrompt = ref('')
const auditLog = ref([])
const score = ref(0)
const loading = ref(false)

const refine = async () => {
  loading.value = true
  try {
    const res = await axios.post('http://127.0.0.1:7777/refine', {
      raw_prompt: rawPrompt.value
    })
    refinedPrompt.value = res.data.refined
    auditLog.value = res.data.audit_log
    score.value = res.data.integrity_score
  } catch (e) {
    console.error(e)
  }
  loading.value = false
}
</script>

<template>
  <div class="container">
    <!-- Left: Slop Bucket -->
    <div class="panel input-panel">
      <h2>🗑️ Slop Bucket</h2>
      <textarea v-model="rawPrompt" placeholder="Paste your garbage prompt here..."></textarea>
      <button @click="refine" :disabled="loading">
        {{ loading ? 'Metabolizing...' : '🔥 Refine & Verify' }}
      </button>
    </div>

    <!-- Right: Gold Output -->
    <div class="panel output-panel">
      <div class="header">
        <h2>✨ Governed Prompt</h2>
        <div class="score" :class="{'high': score > 80, 'low': score < 50}">
          Integrity: {{ score }}%
        </div>
      </div>
      
      <div class="audit-log" v-if="auditLog.length">
        <div v-for="(log, i) in auditLog" :key="i" class="audit-item">
          ⚠️ {{ log }}
        </div>
      </div>

      <textarea readonly :value="refinedPrompt" placeholder="Waiting for input..."></textarea>
    </div>
  </div>
</template>

<style>
body { margin: 0; background: #111; color: #eee; font-family: sans-serif; }
.container { display: flex; height: 100vh; }
.panel { flex: 1; padding: 20px; display: flex; flex-direction: column; gap: 15px; }
.input-panel { border-right: 1px solid #333; }
textarea { 
  flex: 1; 
  background: #222; 
  border: 1px solid #444; 
  color: #fff; 
  padding: 15px; 
  resize: none; 
  font-family: monospace;
}
button {
  padding: 15px;
  background: #ff4400;
  border: none;
  color: white;
  font-weight: bold;
  cursor: pointer;
  font-size: 1.1rem;
}
button:hover { background: #ff6600; }
.audit-item { color: #ffcc00; font-size: 0.9rem; }
.score { font-weight: bold; }
.score.high { color: #00ff00; }
</style>
