<?php

namespace App\Services;

use App\Models\User;
use Illuminate\Validation\ValidationException;
use Tymon\JWTAuth\Facades\JWTAuth;

class AuthService
{
    public function register(string $email, string $password, string $name): array
    {
        $email = strtolower($email);
        if (User::where('email', $email)->exists()) {
            throw ValidationException::withMessages(['email' => ['Email already registered']]);
        }

        $user = User::create([
            'email' => $email,
            'password' => $password,
            'name' => $name,
        ]);

        $token = JWTAuth::fromUser($user);

        return [
            'user' => $this->formatUser($user),
            'tokens' => [
                'access_token' => $token,
                'token_type' => 'Bearer',
            ],
        ];
    }

    public function login(string $email, string $password): array
    {
        $email = strtolower($email);
        $token = JWTAuth::attempt(['email' => $email, 'password' => $password]);
        if (! $token) {
            throw ValidationException::withMessages(['email' => ['Invalid credentials']]);
        }

        $user = User::where('email', $email)->firstOrFail();

        return [
            'user' => $this->formatUser($user),
            'tokens' => [
                'access_token' => $token,
                'token_type' => 'Bearer',
            ],
        ];
    }

    private function formatUser(User $user): array
    {
        return [
            'id' => $user->id,
            'email' => $user->email,
            'name' => $user->name,
            'created_at' => $user->created_at?->toIso8601String(),
        ];
    }
}
