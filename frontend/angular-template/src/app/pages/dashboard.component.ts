import { Component, inject, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ApiService } from '../services/api.service';

type Task = {
  id: number;
  title: string;
  prompt_body: string;
  is_reusable: boolean;
};

@Component({
  standalone: true,
  imports: [RouterLink],
  template: `
    <div>
      <div class="row" style="justify-content: space-between; margin-bottom: 1rem">
        <h2 style="margin: 0">Tasks</h2>
        <a routerLink="/tasks/new"><button class="primary" type="button">New task</button></a>
      </div>
      @if (loading) {
        <p class="muted">Loading…</p>
      }
      @if (err) {
        <p class="error">{{ err }}</p>
      }
      @if (!loading && !items.length) {
        <div class="card muted">No tasks yet.</div>
      }
      @for (t of items; track t.id) {
        <div class="card">
          <div class="row" style="justify-content: space-between">
            <div>
              <strong>{{ t.title }}</strong>
              @if (t.is_reusable) {
                <span class="muted"> · reusable</span>
              }
            </div>
            <div class="row">
              <a [routerLink]="['/tasks', t.id]">Edit</a>
              <button type="button" (click)="remove(t.id)">Delete</button>
            </div>
          </div>
          <p class="muted" style="margin: 0.5rem 0 0; white-space: pre-wrap">
            {{ (t.prompt_body || '').slice(0, 200) }}{{ (t.prompt_body || '').length > 200 ? '…' : '' }}
          </p>
        </div>
      }
    </div>
  `,
  styles: [
    `
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
      button.primary {
        background: #2563eb;
        color: #fff;
        border-color: #2563eb;
      }
      .muted {
        color: #64748b;
        font-size: 0.9rem;
      }
      .error {
        color: #b91c1c;
      }
      .card {
        background: #fff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
      }
    `,
  ],
})
export class DashboardComponent implements OnInit {
  private readonly api = inject(ApiService);

  items: Task[] = [];
  loading = true;
  err = '';

  ngOnInit() {
    this.load();
  }

  load() {
    this.loading = true;
    this.err = '';
    this.api.get<{ items: Task[] }>('/tasks').subscribe({
      next: (d) => {
        this.items = d.items || [];
        this.loading = false;
      },
      error: (e: Error) => {
        this.err = e.message || 'Failed to load tasks';
        this.loading = false;
      },
    });
  }

  remove(id: number) {
    if (!confirm('Delete this task?')) return;
    this.api.delete<null>(`/tasks/${id}`).subscribe({
      next: () => this.load(),
      error: (e: Error) => (this.err = e.message || 'Delete failed'),
    });
  }
}
