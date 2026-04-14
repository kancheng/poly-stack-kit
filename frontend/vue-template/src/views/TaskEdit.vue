<template>
  <div class="card">
    <h2>{{ isNew ? 'New task' : 'Edit task' }}</h2>
    <form @submit.prevent="save">
      <div style="margin-bottom: 0.75rem">
        <label>Title</label>
        <input v-model="form.title" required />
      </div>
      <div style="margin-bottom: 0.75rem">
        <label>Prompt body</label>
        <textarea v-model="form.prompt_body" rows="8" required></textarea>
      </div>
      <div style="margin-bottom: 0.75rem">
        <label>Description</label>
        <textarea v-model="form.description" rows="3"></textarea>
      </div>
      <label class="row" style="gap: 0.5rem; margin-bottom: 0.75rem">
        <input v-model="form.is_reusable" type="checkbox" />
        Reusable prompt
      </label>
      <p v-if="err" class="error">{{ err }}</p>
      <button class="primary" type="submit">Save</button>
      <router-link to="/dashboard" style="margin-left: 0.5rem">Cancel</router-link>
    </form>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { api, unwrap } from '../api';

const route = useRoute();
const router = useRouter();
const isNew = computed(() => route.path.endsWith('/new'));
const err = ref('');

const form = reactive({
  title: '',
  prompt_body: '',
  description: '',
  is_reusable: true,
});

async function load() {
  if (isNew.value) return;
  const res = await api.get(`/tasks/${route.params.id}`);
  const t = unwrap(res);
  form.title = t.title;
  form.prompt_body = t.prompt_body;
  form.description = t.description || '';
  form.is_reusable = !!t.is_reusable;
}

async function save() {
  err.value = '';
  try {
    if (isNew.value) {
      const res = await api.post('/tasks', { ...form });
      const t = unwrap(res);
      router.replace(`/tasks/${t.id}`);
    } else {
      await api.put(`/tasks/${route.params.id}`, { ...form });
      router.push('/dashboard');
    }
  } catch (e) {
    err.value = e.message || 'Save failed';
  }
}

onMounted(async () => {
  try {
    await load();
  } catch (e) {
    err.value = e.message || 'Load failed';
  }
});
</script>
