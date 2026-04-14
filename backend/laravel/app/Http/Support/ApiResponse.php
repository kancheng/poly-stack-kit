<?php

namespace App\Http\Support;

use Illuminate\Http\JsonResponse;

class ApiResponse
{
    public static function ok(mixed $data = null, string $message = 'OK', int $status = 200): JsonResponse
    {
        return response()->json([
            'success' => true,
            'message' => $message,
            'data' => $data,
            'error' => null,
        ], $status);
    }

    public static function fail(string $message, int $code, mixed $details = null, ?int $status = null): JsonResponse
    {
        $http = $status ?? $code;

        return response()->json([
            'success' => false,
            'message' => $message,
            'data' => null,
            'error' => [
                'code' => $code,
                'details' => $details,
            ],
        ], $http);
    }
}
