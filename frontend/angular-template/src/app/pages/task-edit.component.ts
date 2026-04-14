import { Component, inject, OnInit } from '@angular/core';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { ApiService } from '../services/api.service';

@Component({
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  template: `
    <div class="card">
      <h2>{{ isNew ? 'New task' : 'Edit task' }}</h2>
      <form [formGroup]="form" (ngSubmit)="save()">
        <div style="margin-bottom: 0.75rem">
          <label>Title</label>
          <input formControlName="title" />
        </div>
        <div style="margin-bottom: 0.75rem">
          <label>Prompt body</label>
          <textarea rows="8" formControlName="prompt_body"></textarea>
        </div>
        <div style="margin-bottom: 0.75rem">
          <label>Description</label>
          <textarea rows="3" formControlName="description"></textarea>
        </div>
        <label class="row" style="gap: 0.5rem; margin-bottom: 0.75rem">
          <input type="checkbox" formControlName="is_reusable" />
          Reusable prompt
        </label>
        @if (err) {
          <p class="error">{{ err }}</p>
        }
        <button class="primary" type="submit">Save</button>
        <a routerLink="/dashboard" style="margin-left: 0.5rem">Cancel</a>
      </form>
    </div>
  `,
  styles: [
    `
      label {
        display: block;
        font-size: 0.85rem;
        margin-bottom: 0.25rem;
        color: #334155;
      }
      input,
      textarea {
        width: 100%;
        padding: 0.5rem 0.6rem;
        border-radius: 8px;
        border: 1px solid #cbd5e1;
      }
      .row {
        display: flex;
        align-items: center;
      }
      a {
        color: #2563eb;
      }
      button.primary {
        background: #2563eb;
        color: #fff;
        border: 1px solid #2563eb;
        border-radius: 8px;
        padding: 0.45rem 0.75rem;
        cursor: pointer;
      }
      .error {
        color: #b91c1c;
      }
      .card {
        background: #fff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem 1.25rem;
      }
    `,
  ],
})
export class TaskEditComponent implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly api = inject(ApiService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  err = '';
  isNew = false;

  form = this.fb.nonNullable.group({
    title: [''],
    prompt_body: [''],
    description: [''],
    is_reusable: [true],
  });

  ngOnInit() {
    this.isNew = this.router.url.endsWith('/tasks/new');
    if (this.isNew) return;
    const id = this.route.snapshot.paramMap.get('id');
    if (!id) {
      this.err = 'Missing task id';
      return;
    }
    this.api
      .get<{ title: string; prompt_body: string; description: string | null; is_reusable: boolean }>(`/tasks/${id}`)
      .subscribe({
        next: (t) => {
          this.form.patchValue({
            title: t.title,
            prompt_body: t.prompt_body,
            description: t.description || '',
            is_reusable: !!t.is_reusable,
          });
        },
        error: (e: Error) => (this.err = e.message || 'Load failed'),
      });
  }

  save() {
    this.err = '';
    const raw = this.form.getRawValue();
    if (this.isNew) {
      this.api.post<{ id: number }>('/tasks', raw).subscribe({
        next: (t) => this.router.navigateByUrl(`/tasks/${t.id}`),
        error: (e: Error) => (this.err = e.message || 'Save failed'),
      });
    } else {
      const id = this.route.snapshot.paramMap.get('id');
      this.api.put(`/tasks/${id}`, raw).subscribe({
        next: () => this.router.navigateByUrl('/dashboard'),
        error: (e: Error) => (this.err = e.message || 'Save failed'),
      });
    }
  }
}
