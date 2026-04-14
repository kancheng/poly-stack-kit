<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Support\ApiResponse;
use App\Services\ExecutionService;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class ExecutionController extends Controller
{
    public function index(Request $request, ExecutionService $exec): \Illuminate\Http\JsonResponse
    {
        $taskId = $request->query('task_id');
        $tid = $taskId !== null ? (int) $taskId : null;

        $data = $exec->listForUser((int) $request->user()->id, $tid);

        return ApiResponse::ok($data);
    }

    public function store(Request $request, ExecutionService $exec): \Illuminate\Http\JsonResponse
    {
        $v = Validator::make($request->all(), [
            'task_id' => 'required|integer',
            'input_payload' => 'required|string',
            'output_payload' => 'required|string',
            'meta' => 'nullable|array',
        ]);
        if ($v->fails()) {
            return ApiResponse::fail('Validation error', 400, $v->errors(), 422);
        }

        try {
            $data = $exec->create((int) $request->user()->id, $v->validated());

            return ApiResponse::ok($data, 'Created', 201);
        } catch (\InvalidArgumentException $e) {
            return ApiResponse::fail($e->getMessage(), 400, $e->getMessage(), 400);
        }
    }
}
