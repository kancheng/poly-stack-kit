<template>
  <div>
    <div class="row" style="justify-content: space-between; margin-bottom: 1rem">
      <h2 style="margin: 0">Tasks</h2>
      <router-link to="/tasks/new"><button class="primary" type="button">New task</button></router-link>
    </div>
    <p v-if="loading" class="muted">Loading…</p>
    <p v-if="err" class="error">{{ err }}</p>
    <div v-if="!loading && !items.length" class="card muted">No tasks yet.</div>
    <div v-for="t in items" :key="t.id" class="card">
      <div class="row" style="justify-content: space-between">
        <div>
          <strong>{{ t.title }}</strong>
          <span class="muted" v-if="t.is_reusable"> · reusable</span>
        </div>
        <div class="row">
          <router-link :to="`/tasks/${t.id}`">Edit</router-link>
          <button type="button" @click="remove(t.id)">Delete</button>
        </div>
      </div>
      <p class="muted" style="margin: 0.5rem 0 0; white-space: pre-wrap">{{ t.prompt_body.slice(0, 200) }}{{ t.prompt_body.length > 200 ? '…' : '' }}</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { api, unwrap } from '../api';

const items = ref([]);
const loading = ref(true);
const err = ref('');

async function load() {
  loading.value = true;
  err.value = '';
  try {
    const res = await api.get('/tasks');
    const data = unwrap(res);
    items.value = data.items || [];
  } catch (e) {
    err.value = e.message || 'Failed to load tasks';
  } finally {
    loading.value = false;
  }
}

async function remove(id) {
  if (!confirm('Delete this task?')) return;
  try {
    await api.delete(`/tasks/${id}`);
    await load();
  } catch (e) {
    err.value = e.message || 'Delete failed';
  }
}

onMounted(load);
</script>
