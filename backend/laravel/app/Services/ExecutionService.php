<?php

namespace App\Services;

use App\Models\Execution;
use App\Models\Task;

class ExecutionService
{
    public function listForUser(int $userId, ?int $taskId): array
    {
        $q = Execution::query()->where('user_id', $userId);
        if ($taskId !== null) {
            $q->where('task_id', $taskId);
        }

        $rows = $q->orderByDesc('created_at')->get();

        return [
            'items' => $rows->map(fn (Execution $e) => $this->toArray($e))->all(),
        ];
    }

    public function create(int $userId, array $data): array
    {
        $task = Task::where('user_id', $userId)->whereKey($data['task_id'])->first();
        if (! $task) {
            throw new \InvalidArgumentException('Task not found');
        }

        $ex = Execution::create([
            'task_id' => $task->id,
            'user_id' => $userId,
            'input_payload' => $data['input_payload'],
            'output_payload' => $data['output_payload'],
            'meta' => $data['meta'] ?? null,
            'created_at' => now(),
        ]);

        return $this->toArray($ex);
    }

    private function toArray(Execution $e): array
    {
        return [
            'id' => $e->id,
            'task_id' => $e->task_id,
            'user_id' => $e->user_id,
            'input_payload' => $e->input_payload,
            'output_payload' => $e->output_payload,
            'meta' => $e->meta,
            'created_at' => $e->created_at?->toIso8601String(),
        ];
    }
}
