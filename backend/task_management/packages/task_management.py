from django.utils import timezone

from task_management.models import (
    Task,
    TaskProcess,
    TaskPriority,
)

from system_management.models import (
    User
)

from global_app import constants as constant


class TaskManagerPackage:

    def __init__(
        self,

        # Task
        title: str = None,
        task_id: int = None,
        due_date: str = None,
        status_id: int = None,
        priority_id: int = None,
        description: str = None,
        date_created: str = None,
        created_by_id: int = None,
        date_modified: str = None,
        assigned_to_id: int = None,

    ) -> None:

        self.title = title
        self.task_id = task_id
        self.due_date = due_date
        self.status_id = status_id
        self.priority_id = priority_id
        self.description = description
        self.date_created = date_created
        self.created_by_id = created_by_id
        self.date_modified = date_modified
        self.assigned_to_id = assigned_to_id

    def get_task_status(self) -> TaskProcess:

        try:

            status: TaskProcess = TaskProcess.objects.get(
                status = constant.PENDING
            )

        except TaskProcess.DoesNotExist:

            raise ValueError("Task status does not exist")

        return status

    def get_task_priority(self) -> TaskPriority:

        try:

            priority: TaskPriority = TaskPriority.objects.get(
                status = constant.MINOR
            )

        except TaskPriority.DoesNotExist:

            raise ValueError("Task priority does not exist")

        return priority

    def get_user_id(self) -> User:

        try:

            user: User = User.objects.get(
                id = self.assigned_to_id
            )

        except User.DoesNotExist:

            raise ValueError("User does not exist")

        return user

    def create_task(self) -> Task:

        user_id: User = self.get_user_id()
        status_id: TaskProcess = self.get_task_status()
        priority_id: TaskPriority = self.get_task_priority()

        task: Task = Task.objects.create(
            title = self.title,
            status_id = status_id.id,
            due_date = self.due_date,
            assigned_to_id = user_id.id,
            priority_id = priority_id.id,
            description = self.description,
            created_by_id = self.created_by_id,
        )

        if not task:

            raise ValueError("Task could not be created")

        return task

    def get_task(self) -> Task:

        try:

            task: Task = Task.objects.get(
                id = self.task_id
            )

        except Task.DoesNotExist:

            raise ValueError("Task does not exist")

        return task

    def get_task_status_id(self) -> TaskProcess:

        try:

            status: TaskProcess = TaskProcess.objects.get(
                id = self.status_id
            )

        except TaskProcess.DoesNotExist:

            raise ValueError("Task status does not exist")

        return status

    def get_task_priority_id(self) -> TaskPriority:

        try:

            priority: TaskPriority = TaskPriority.objects.get(
                id = self.priority_id
            )

        except TaskPriority.DoesNotExist:

            raise ValueError("Task priority does not exist")

        return priority

    def edit_task(self) -> Task:

        task: Task = self.get_task()

        task.title = self.title
        task.description = self.description
        task.date_modified = timezone.now()
        task.due_date = self.due_date

        assigned_to_id: User = self.get_user_id()
        status_id: TaskProcess = self.get_task_status_id()
        priority_id: TaskPriority = self.get_task_priority_id()

        task.status_id = status_id.id
        task.priority_id = priority_id.id
        task.assigned_to_id = assigned_to_id.id

        task.save()

        return task

    def delete_task(self) -> None:

        task: Task = self.get_task()

        task.delete()

        return True

    def get_all_tasks(self) -> list[Task]:

        tasks: list[Task] = Task.objects.all()

        return tasks






