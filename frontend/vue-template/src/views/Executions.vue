<template>
  <div>
    <h2>Executions</h2>
    <div class="row" style="margin-bottom: 0.75rem">
      <label style="margin: 0">Filter task id</label>
      <input v-model.number="taskFilter" type="number" min="1" style="max-width: 120px" @change="load" />
      <button type="button" @click="load">Apply</button>
    </div>
    <p v-if="loading" class="muted">Loading…</p>
    <p v-if="err" class="error">{{ err }}</p>
    <div v-if="!loading && !items.length" class="card muted">No executions.</div>
    <div v-for="e in items" :key="e.id" class="card">
      <div class="muted">#{{ e.id }} · task {{ e.task_id }} · {{ e.created_at }}</div>
      <p><strong>Input</strong></p>
      <pre style="white-space: pre-wrap; margin: 0 0 0.5rem">{{ e.input_payload }}</pre>
      <p><strong>Output</strong></p>
      <pre style="white-space: pre-wrap; margin: 0">{{ e.output_payload }}</pre>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { api, unwrap } from '../api';

const items = ref([]);
const loading = ref(true);
const err = ref('');
const taskFilter = ref(null);

async function load() {
  loading.value = true;
  err.value = '';
  try {
    const params = {};
    if (taskFilter.value) params.task_id = taskFilter.value;
    const res = await api.get('/executions', { params });
    const data = unwrap(res);
    items.value = data.items || [];
  } catch (e) {
    err.value = e.message || 'Failed to load';
  } finally {
    loading.value = false;
  }
}

onMounted(load);
</script>
