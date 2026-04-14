import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../services/api.service';

@Component({
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <div class="card" style="max-width: 420px">
      <h2>Login</h2>
      <form [formGroup]="form" (ngSubmit)="submit()">
        <div style="margin-bottom: 0.75rem">
          <label>Email</label>
          <input formControlName="email" type="email" autocomplete="username" />
        </div>
        <div style="margin-bottom: 0.75rem">
          <label>Password</label>
          <input formControlName="password" type="password" autocomplete="current-password" />
        </div>
        @if (err) {
          <p class="error">{{ err }}</p>
        }
        <button class="primary" type="submit">Sign in</button>
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
      input {
        width: 100%;
        padding: 0.5rem 0.6rem;
        border-radius: 8px;
        border: 1px solid #cbd5e1;
      }
      .error {
        color: #b91c1c;
        font-size: 0.9rem;
      }
      button.primary {
        background: #2563eb;
        color: #fff;
        border: 1px solid #2563eb;
        border-radius: 8px;
        padding: 0.45rem 0.75rem;
        cursor: pointer;
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
export class LoginComponent {
  private readonly fb = inject(FormBuilder);
  private readonly api = inject(ApiService);
  private readonly router = inject(Router);

  err = '';

  form = this.fb.nonNullable.group({
    email: [''],
    password: [''],
  });

  submit() {
    this.err = '';
    this.api
      .post<{ user: unknown; tokens: { access_token: string; token_type: string } }>('/auth/login', this.form.getRawValue())
      .subscribe({
        next: (d) => {
          localStorage.setItem('polystack_token', d.tokens.access_token);
          this.router.navigateByUrl('/dashboard');
        },
        error: (e: Error) => {
          this.err = e.message || 'Login failed';
        },
      });
  }
}
