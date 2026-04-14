import { Component, inject } from '@angular/core';
import { Router, RouterLink, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink],
  template: `
    <div class="layout">
      <header class="row" style="justify-content: space-between; margin-bottom: 1rem">
        <div>
          <strong>PolyStack Angular</strong>
          <span class="muted"> — AI Prompt Task Hub</span>
        </div>
        @if (token()) {
          <nav class="row">
            <a routerLink="/dashboard">Dashboard</a>
            <a routerLink="/executions">Executions</a>
            <button type="button" (click)="logout()">Logout</button>
          </nav>
        } @else {
          <nav class="row">
            <a routerLink="/login">Login</a>
            <a routerLink="/register">Register</a>
          </nav>
        }
      </header>
      <router-outlet />
    </div>
  `,
  styles: [
    `
      :host {
        font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
        color: #0f172a;
        background: #f8fafc;
      }
      .layout {
        max-width: 960px;
        margin: 0 auto;
        padding: 1.5rem;
      }
      .row {
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
        align-items: center;
      }
      a {
        color: #2563eb;
      }
      button {
        cursor: pointer;
        border: 1px solid #cbd5e1;
        background: #fff;
        border-radius: 8px;
        padding: 0.45rem 0.75rem;
      }
      .muted {
        color: #64748b;
        font-size: 0.9rem;
      }
    `,
  ],
})
export class AppComponent {
  private readonly router = inject(Router);

  token() {
    return !!localStorage.getItem('polystack_token');
  }

  logout() {
    localStorage.removeItem('polystack_token');
    this.router.navigateByUrl('/login');
  }
}
