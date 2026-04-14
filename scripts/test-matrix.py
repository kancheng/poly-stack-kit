#!/usr/bin/env python3
"""
PolyStack 3x3 combination smoke test.

Tests all frontend/backend combinations against backend APIs:
1) POST /api/auth/login
2) GET  /api/auth/me (with Bearer token)

Usage:
  python scripts/test-matrix.py
  python scripts/test-matrix.py --email demo@polystack.local --password password
  python scripts/test-matrix.py --backend django=http://127.0.0.1:8000 --backend laravel=http://127.0.0.1:8100 --backend flask=http://127.0.0.1:8200
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass


FRONTENDS = ("vue", "react", "angular")

DEFAULT_BACKENDS = {
    "django": "http://127.0.0.1:8000",
    "laravel": "http://127.0.0.1:8100",
    "flask": "http://127.0.0.1:8200",
}


@dataclass
class TestResult:
    frontend: str
    backend: str
    backend_url: str
    ok: bool
    detail: str


def request_json(method: str, url: str, payload: dict | None = None, headers: dict | None = None) -> tuple[int, dict]:
    body = None
    req_headers = {"Content-Type": "application/json"}
    if headers:
        req_headers.update(headers)
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(url, data=body, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            text = resp.read().decode("utf-8")
            data = json.loads(text) if text else {}
            return resp.status, data
    except urllib.error.HTTPError as e:
        text = e.read().decode("utf-8")
        data = {}
        if text:
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                data = {"raw": text}
        return e.code, data
    except urllib.error.URLError as e:
        return 0, {"message": f"connection error: {e.reason}"}


def login_and_me(base_url: str, email: str, password: str) -> tuple[bool, str]:
    base = base_url.rstrip("/")
    login_status, login_data = request_json(
        "POST",
        f"{base}/api/auth/login",
        payload={"email": email, "password": password},
    )
    if login_status != 200 or login_data.get("success") is not True:
        return False, f"login failed ({login_status}): {login_data.get('message', 'unknown error')}"

    token = (
        login_data.get("data", {})
        .get("tokens", {})
        .get("access_token")
    )
    if not token:
        return False, "login succeeded but access_token missing"

    me_status, me_data = request_json(
        "GET",
        f"{base}/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    if me_status != 200 or me_data.get("success") is not True:
        return False, f"auth/me failed ({me_status}): {me_data.get('message', 'unknown error')}"

    user = me_data.get("data", {})
    user_email = user.get("email")
    if not user_email:
        return False, "auth/me succeeded but user email missing"

    return True, f"ok ({user_email})"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run 3x3 frontend/backend smoke tests")
    p.add_argument("--email", default="demo@polystack.local", help="login email")
    p.add_argument("--password", default="password", help="login password")
    p.add_argument(
        "--backend",
        action="append",
        default=[],
        help="override backend URL, format: name=url (name: django|laravel|flask)",
    )
    return p.parse_args()


def resolve_backends(overrides: list[str]) -> dict[str, str]:
    backends = dict(DEFAULT_BACKENDS)
    for item in overrides:
        if "=" not in item:
            raise ValueError(f"invalid --backend '{item}', expected name=url")
        name, url = item.split("=", 1)
        name = name.strip().lower()
        url = url.strip()
        if name not in backends:
            raise ValueError(f"unknown backend '{name}', expected one of: {', '.join(backends.keys())}")
        if not url.startswith("http://") and not url.startswith("https://"):
            raise ValueError(f"backend URL must start with http:// or https:// ({url})")
        backends[name] = url
    return backends


def main() -> int:
    args = parse_args()
    try:
        backends = resolve_backends(args.backend)
    except ValueError as e:
        print(f"error: {e}")
        return 2

    results: list[TestResult] = []
    for fe in FRONTENDS:
        for be, be_url in backends.items():
            ok, detail = login_and_me(be_url, args.email, args.password)
            results.append(TestResult(fe, be, be_url, ok, detail))

    print("=== PolyStack 3x3 Matrix Test ===")
    print(f"email={args.email}")
    print("")

    pass_count = 0
    for r in results:
        status = "PASS" if r.ok else "FAIL"
        if r.ok:
            pass_count += 1
        print(f"[{status}] FE={r.frontend:<7} BE={r.backend:<7} URL={r.backend_url} -> {r.detail}")

    total = len(results)
    print("")
    print(f"Result: {pass_count}/{total} passed")
    return 0 if pass_count == total else 1


if __name__ == "__main__":
    sys.exit(main())

