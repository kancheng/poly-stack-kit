<?php

namespace App\Services;

use App\Models\Task;
use Illuminate\Contracts\Pagination\LengthAwarePaginator;

class TaskService
{
    public function paginateForUser(int $userId, int $page, int $perPage): array
    {
        /** @var LengthAwarePaginator $p */
        $p = Task::query()
            ->where('user_id', $userId)
            ->orderByDesc('created_at')
            ->paginate($perPage, ['*'], 'page', $page);

        return [
            'items' => $p->items() ? collect($p->items())->map(fn (Task $t) => $this->toArray($t))->all() : [],
            'page' => $p->currentPage(),
            'per_page' => $p->perPage(),
            'total' => $p->total(),
            'total_pages' => max(1, $p->lastPage()),
        ];
    }

    public function create(int $userId, array $data): array
    {
        $task = Task::create([
            'user_id' => $userId,
            'title' => $data['title'],
            'prompt_body' => $data['prompt_body'],
            'description' => $data['description'] ?? null,
            'is_reusable' => $data['is_reusable'] ?? true,
        ]);

        return $this->toArray($task);
    }

    public function findForUser(int $userId, int $taskId): ?array
    {
        $task = Task::where('user_id', $userId)->whereKey($taskId)->first();

        return $task ? $this->toArray($task) : null;
    }

    public function update(int $userId, int $taskId, array $data): ?array
    {
        $task = Task::where('user_id', $userId)->whereKey($taskId)->first();
        if (! $task) {
            return null;
        }

        $task->fill([
            'title' => $data['title'],
            'prompt_body' => $data['prompt_body'],
            'description' => $data['description'] ?? null,
            'is_reusable' => $data['is_reusable'] ?? true,
        ]);
        $task->save();

        return $this->toArray($task);
    }

    public function delete(int $userId, int $taskId): bool
    {
        $task = Task::where('user_id', $userId)->whereKey($taskId)->first();
        if (! $task) {
            return false;
        }

        $task->delete();

        return true;
    }

    private function toArray(Task $t): array
    {
        return [
            'id' => $t->id,
            'user_id' => $t->user_id,
            'title' => $t->title,
            'prompt_body' => $t->prompt_body,
            'description' => $t->description,
            'is_reusable' => (bool) $t->is_reusable,
            'created_at' => $t->created_at?->toIso8601String(),
            'updated_at' => $t->updated_at?->toIso8601String(),
        ];
    }
}
