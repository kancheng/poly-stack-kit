<?php

namespace App\Services;

use App\Models\Execution;
use App\Models\Rating;

class RatingService
{
    public function listForUser(int $userId, ?int $executionId): array
    {
        $q = Rating::query()->where('user_id', $userId);
        if ($executionId !== null) {
            $q->where('execution_id', $executionId);
        }

        $rows = $q->orderByDesc('created_at')->get();

        return [
            'items' => $rows->map(fn (Rating $r) => $this->toArray($r))->all(),
        ];
    }

    public function create(int $userId, array $data): array
    {
        $ex = Execution::where('user_id', $userId)->whereKey($data['execution_id'])->first();
        if (! $ex) {
            throw new \InvalidArgumentException('Execution not found');
        }

        if (Rating::where('user_id', $userId)->where('execution_id', $data['execution_id'])->exists()) {
            throw new \InvalidArgumentException('Already rated this execution');
        }

        $r = Rating::create([
            'user_id' => $userId,
            'execution_id' => $data['execution_id'],
            'score' => $data['score'],
            'comment' => $data['comment'] ?? null,
            'created_at' => now(),
        ]);

        return $this->toArray($r);
    }

    private function toArray(Rating $r): array
    {
        return [
            'id' => $r->id,
            'user_id' => $r->user_id,
            'execution_id' => $r->execution_id,
            'score' => $r->score,
            'comment' => $r->comment,
            'created_at' => $r->created_at?->toIso8601String(),
        ];
    }
}
