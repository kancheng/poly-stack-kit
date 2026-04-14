<template>
  <div class="card" style="max-width: 420px">
    <h2>Register</h2>
    <form @submit.prevent="submit">
      <div style="margin-bottom: 0.75rem">
        <label>Name</label>
        <input v-model="name" required />
      </div>
      <div style="margin-bottom: 0.75rem">
        <label>Email</label>
        <input v-model="email" type="email" required autocomplete="email" />
      </div>
      <div style="margin-bottom: 0.75rem">
        <label>Password (min 8)</label>
        <input v-model="password" type="password" required minlength="8" autocomplete="new-password" />
      </div>
      <p v-if="err" class="error">{{ err }}</p>
      <button class="primary" type="submit">Create account</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { api, unwrap } from '../api';

const router = useRouter();
const name = ref('');
const email = ref('');
const password = ref('');
const err = ref('');

async function submit() {
  err.value = '';
  try {
    const res = await api.post('/auth/register', {
      name: name.value,
      email: email.value,
      password: password.value,
    });
    const data = unwrap(res);
    localStorage.setItem('polystack_token', data.tokens.access_token);
    router.push('/dashboard');
  } catch (e) {
    err.value = e.message || 'Register failed';
  }
}
</script>
