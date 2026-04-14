<template>
  <div class="layout">
    <header class="row" style="justify-content: space-between; margin-bottom: 1rem">
      <div>
        <strong>PolyStack Vue</strong>
        <span class="muted"> — AI Prompt Task Hub</span>
      </div>
      <nav v-if="token" class="row">
        <router-link to="/dashboard">Dashboard</router-link>
        <router-link to="/executions">Executions</router-link>
        <button type="button" @click="logout">Logout</button>
      </nav>
      <nav v-else class="row">
        <router-link to="/login">Login</router-link>
        <router-link to="/register">Register</router-link>
      </nav>
    </header>
    <router-view />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const token = computed(() => localStorage.getItem('polystack_token'));

function logout() {
  localStorage.removeItem('polystack_token');
  router.push('/login');
}
</script>
