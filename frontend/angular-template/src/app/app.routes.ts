import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'dashboard' },
  {
    path: 'login',
    loadComponent: () => import('./pages/login.component').then((m) => m.LoginComponent),
  },
  {
    path: 'register',
    loadComponent: () => import('./pages/register.component').then((m) => m.RegisterComponent),
  },
  {
    path: 'dashboard',
    canActivate: [authGuard],
    loadComponent: () => import('./pages/dashboard.component').then((m) => m.DashboardComponent),
  },
  {
    path: 'tasks/new',
    canActivate: [authGuard],
    loadComponent: () => import('./pages/task-edit.component').then((m) => m.TaskEditComponent),
  },
  {
    path: 'tasks/:id',
    canActivate: [authGuard],
    loadComponent: () => import('./pages/task-edit.component').then((m) => m.TaskEditComponent),
  },
  {
    path: 'executions',
    canActivate: [authGuard],
    loadComponent: () => import('./pages/executions.component').then((m) => m.ExecutionsComponent),
  },
];
