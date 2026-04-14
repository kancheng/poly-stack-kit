import { createRouter, createWebHistory } from 'vue-router';
import Login from './views/Login.vue';
import Register from './views/Register.vue';
import Dashboard from './views/Dashboard.vue';
import TaskEdit from './views/TaskEdit.vue';
import Executions from './views/Executions.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/dashboard' },
    { path: '/login', component: Login },
    { path: '/register', component: Register },
    { path: '/dashboard', component: Dashboard, meta: { auth: true } },
    { path: '/tasks/new', component: TaskEdit, meta: { auth: true } },
    { path: '/tasks/:id', component: TaskEdit, meta: { auth: true } },
    { path: '/executions', component: Executions, meta: { auth: true } },
  ],
});

router.beforeEach((to) => {
  const token = localStorage.getItem('polystack_token');
  if (to.meta.auth && !token) return '/login';
  return true;
});

export default router;
