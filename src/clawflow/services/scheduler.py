from __future__ import annotations

from collections import defaultdict, deque

from clawflow.domain.models import TaskNode


class Scheduler:
    def execution_layers(self, tasks: list[TaskNode]) -> list[list[TaskNode]]:
        task_map = {task.id: task for task in tasks}
        indegree = {task.id: len(task.dependencies) for task in tasks}
        dependents: dict[str, list[str]] = defaultdict(list)
        for task in tasks:
            for dependency in task.dependencies:
                dependents[dependency].append(task.id)

        queue = deque(sorted(task.id for task in tasks if indegree[task.id] == 0))
        layers: list[list[TaskNode]] = []

        while queue:
            current_layer_ids = list(queue)
            queue.clear()
            layers.append([task_map[task_id] for task_id in current_layer_ids])
            for task_id in current_layer_ids:
                for dependent_id in dependents[task_id]:
                    indegree[dependent_id] -= 1
                    if indegree[dependent_id] == 0:
                        queue.append(dependent_id)

        if sum(len(layer) for layer in layers) != len(tasks):
            raise ValueError("Task graph contains a cycle.")

        return layers

