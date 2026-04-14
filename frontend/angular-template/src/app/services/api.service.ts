import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

type Envelope<T> = {
  success: boolean;
  message: string;
  data: T;
  error: { code: number; details: unknown } | null;
};

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly http = inject(HttpClient);
  private readonly base = `${environment.apiBase.replace(/\/$/, '')}/api`;

  private unwrap<T>(): (source: Observable<Envelope<T>>) => Observable<T> {
    return map((res) => {
      if (!res || res.success !== true) {
        throw new Error((res as Envelope<unknown>)?.message || 'Request failed');
      }
      return res.data;
    });
  }

  post<T>(path: string, body: unknown): Observable<T> {
    return this.http.post<Envelope<T>>(`${this.base}${path}`, body).pipe(this.unwrap<T>());
  }

  get<T>(path: string, params?: Record<string, string | number | undefined>): Observable<T> {
    let url = `${this.base}${path}`;
    if (params) {
      const qs = new URLSearchParams();
      for (const [k, v] of Object.entries(params)) {
        if (v === undefined || v === '') continue;
        qs.set(k, String(v));
      }
      const q = qs.toString();
      if (q) url += `?${q}`;
    }
    return this.http.get<Envelope<T>>(url).pipe(this.unwrap<T>());
  }

  put<T>(path: string, body: unknown): Observable<T> {
    return this.http.put<Envelope<T>>(`${this.base}${path}`, body).pipe(this.unwrap<T>());
  }

  delete<T>(path: string): Observable<T> {
    return this.http.delete<Envelope<T>>(`${this.base}${path}`).pipe(this.unwrap<T>());
  }
}
