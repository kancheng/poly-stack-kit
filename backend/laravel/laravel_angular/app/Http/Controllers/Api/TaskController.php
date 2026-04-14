<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Support\ApiResponse;
use App\Services\TaskService;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class TaskController extends Controller
{
    public function index(Request $request, TaskService $tasks): \Illuminate\Http\JsonResponse
    {
        $page = max(1, (int) $request->query('page', 1));
        $perPage = min(100, max(1, (int) $request->query('per_page', 20)));

        $data = $tasks->paginateForUser((int) $request->user()->id, $page, $perPage);

        return ApiResponse::ok($data);
    }

    public function store(Request $request, TaskService $tasks): \Illuminate\Http\JsonResponse
    {
        $v = Validator::make($request->all(), [
            'title' => 'required|string|max:255',
            'prompt_body' => 'required|string',
            'description' => 'nullable|string',
            'is_reusable' => 'boolean',
        ]);
        if ($v->fails()) {
            return ApiResponse::fail('Validation error', 400, $v->errors(), 422);
        }

        $data = $tasks->create((int) $request->user()->id, $v->validated());

        return ApiResponse::ok($data, 'Created', 201);
    }

    public function show(Request $request, TaskService $tasks, int $id): \Illuminate\Http\JsonResponse
    {
        $row = $tasks->findForUser((int) $request->user()->id, $id);
        if (! $row) {
            return ApiResponse::fail('Not found', 404, null, 404);
        }

        return ApiResponse::ok($row);
    }

    public function update(Request $request, TaskService $tasks, int $id): \Illuminate\Http\JsonResponse
    {
        $v = Validator::make($request->all(), [
            'title' => 'required|string|max:255',
            'prompt_body' => 'required|string',
            'description' => 'nullable|string',
            'is_reusable' => 'boolean',
        ]);
        if ($v->fails()) {
            return ApiResponse::fail('Validation error', 400, $v->errors(), 422);
        }

        $row = $tasks->update((int) $request->user()->id, $id, $v->validated());
        if (! $row) {
            return ApiResponse::fail('Not found', 404, null, 404);
        }

        return ApiResponse::ok($row);
    }

    public function destroy(Request $request, TaskService $tasks, int $id): \Illuminate\Http\JsonResponse
    {
        if (! $tasks->delete((int) $request->user()->id, $id)) {
            return ApiResponse::fail('Not found', 404, null, 404);
        }

        return ApiResponse::ok(null, 'Deleted');
    }
}
