import { Component, inject, OnInit } from '@angular/core';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

type Execution = {
  id: number;
  task_id: number;
  input_payload: string;
  output_payload: string;
  created_at: string;
};

@Component({
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <div>
      <h2>Executions</h2>
      <form class="row" style="margin-bottom: 0.75rem" [formGroup]="form" (ngSubmit)="load()">
        <label style="margin: 0">Filter task id</label>
        <input style="max-width: 120px" type="number" min="1" formControlName="taskId" />
        <button type="submit">Apply</button>
      </form>
      @if (loading) {
        <p class="muted">Loading…</p>
      }
      @if (err) {
        <p class="error">{{ err }}</p>
      }
      @if (!loading && !items.length) {
        <div class="card muted">No executions.</div>
      }
      @for (e of items; track e.id) {
        <div class="card">
          <div class="muted">#{{ e.id }} · task {{ e.task_id }} · {{ e.created_at }}</div>
          <p><strong>Input</strong></p>
          <pre style="margin: 0 0 0.5rem">{{ e.input_payload }}</pre>
          <p><strong>Output</strong></p>
          <pre style="margin: 0">{{ e.output_payload }}</pre>
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
      input {
        padding: 0.5rem 0.6rem;
        border-radius: 8px;
        border: 1px solid #cbd5e1;
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
      pre {
        white-space: pre-wrap;
      }
    `,
  ],
})
export class ExecutionsComponent implements OnInit {
  private readonly api = inject(ApiService);
  private readonly fb = inject(FormBuilder);

  items: Execution[] = [];
  loading = true;
  err = '';

  form = this.fb.nonNullable.group({ taskId: [''] });

  ngOnInit() {
    this.load();
  }

  load() {
    this.loading = true;
    this.err = '';
    const tid = this.form.controls.taskId.value;
    const params: Record<string, string | number | undefined> = {};
    if (tid) params['task_id'] = Number(tid);
    this.api.get<{ items: Execution[] }>('/executions', params).subscribe({
      next: (d) => {
        this.items = d.items || [];
        this.loading = false;
      },
      error: (e: Error) => {
        this.err = e.message || 'Failed to load';
        this.loading = false;
      },
    });
  }
}
