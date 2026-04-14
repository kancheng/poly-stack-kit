<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Support\ApiResponse;
use App\Services\AuthService;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\ValidationException;

class AuthController extends Controller
{
    public function register(Request $request, AuthService $auth): \Illuminate\Http\JsonResponse
    {
        $v = Validator::make($request->all(), [
            'email' => 'required|email',
            'password' => 'required|min:8',
            'name' => 'required|string|max:120',
        ]);
        if ($v->fails()) {
            return ApiResponse::fail('Validation error', 400, $v->errors(), 422);
        }

        try {
            $data = $auth->register(
                $v->validated()['email'],
                $v->validated()['password'],
                $v->validated()['name'],
            );

            return ApiResponse::ok($data, 'Created', 201);
        } catch (ValidationException $e) {
            return ApiResponse::fail('Validation error', 400, $e->errors(), 400);
        }
    }

    public function login(Request $request, AuthService $auth): \Illuminate\Http\JsonResponse
    {
        $v = Validator::make($request->all(), [
            'email' => 'required|email',
            'password' => 'required',
        ]);
        if ($v->fails()) {
            return ApiResponse::fail('Validation error', 400, $v->errors(), 422);
        }

        try {
            $data = $auth->login($v->validated()['email'], $v->validated()['password']);

            return ApiResponse::ok($data);
        } catch (ValidationException $e) {
            return ApiResponse::fail('Invalid credentials', 401, $e->errors(), 401);
        }
    }

    public function me(Request $request): \Illuminate\Http\JsonResponse
    {
        $u = $request->user();
        $data = [
            'id' => $u->id,
            'email' => $u->email,
            'name' => $u->name,
            'created_at' => $u->created_at?->toIso8601String(),
        ];

        return ApiResponse::ok($data);
    }
}
