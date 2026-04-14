<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Support\ApiResponse;
use App\Services\RatingService;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class RatingController extends Controller
{
    public function index(Request $request, RatingService $ratings): \Illuminate\Http\JsonResponse
    {
        $exId = $request->query('execution_id');
        $eid = $exId !== null ? (int) $exId : null;

        $data = $ratings->listForUser((int) $request->user()->id, $eid);

        return ApiResponse::ok($data);
    }

    public function store(Request $request, RatingService $ratings): \Illuminate\Http\JsonResponse
    {
        $v = Validator::make($request->all(), [
            'execution_id' => 'required|integer',
            'score' => 'required|integer|min:1|max:5',
            'comment' => 'nullable|string',
        ]);
        if ($v->fails()) {
            return ApiResponse::fail('Validation error', 400, $v->errors(), 422);
        }

        try {
            $data = $ratings->create((int) $request->user()->id, $v->validated());

            return ApiResponse::ok($data, 'Created', 201);
        } catch (\InvalidArgumentException $e) {
            return ApiResponse::fail($e->getMessage(), 400, $e->getMessage(), 400);
        }
    }
}
