import json
from rest_framework import status
from rest_framework.response import Response

from task_management.packages.task_management import TaskManagerPackage
from task_management.serializer.base_serializer import (
    GetTaskSerializer,
    EditTaskSerializer,
    CreateTaskSerializer,
    DeleteTaskSerializer,
)
from task_management.serializer.model_serializer import (
    GetAllTaskModelSerializer
)


class TaskManagerService:
    """
    Task Manager Service
    """

    def __init__(
        self,
        request = None,
        ) -> None:

        self.request = request

    def create_task(self):

        user = self.request.user
        data = self.request.data

        serialiazer: CreateTaskSerializer = CreateTaskSerializer(
            data = data
        )

        if not serialiazer.is_valid():

            response_data = json.dumps({
                'status': 'error',
                'message': 'Invalid data to API',
                'data': serialiazer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data: dict = serialiazer.validated_data
        title: str = validated_data.get('title')
        due_date: str = validated_data.get('due_date')
        description: str = validated_data.get('description')
        priority_id: int = validated_data.get('priority_id')
        assigned_to_id: int = validated_data.get('assigned_to_id')

        try:

            TaskManagerPackage(
                title = title,
                due_date = due_date,
                created_by_id = user.id,
                description = description,
                priority_id = priority_id,
                assigned_to_id = assigned_to_id
            ).create_task()

            response_data = json.dumps({
                'status': 'success',
                'message': 'Task created successfully',
                'data': serialiazer.data
            })
            return Response(response_data, status=status.HTTP_201_CREATED)

        except ValueError as error:

            response_data = json.dumps({
                'status': 'error',
                'message': str(error),
                'data': {}
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to create task, please try again',
                'data': str(error)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def edit_task(self):

        data = self.request.data

        serialiazer: EditTaskSerializer = EditTaskSerializer(
            data = data
        )

        if not serialiazer.is_valid():

            response_data = json.dumps({
                'status': 'error',
                'message': 'Invalid data to API',
                'data': serialiazer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data: dict = serialiazer.validated_data
        title: str = validated_data.get('title')
        task_id: int = validated_data.get('task_id')
        due_date: str = validated_data.get('due_date')
        status_id: int = validated_data.get('status_id')
        description: str = validated_data.get('description')
        priority_id: int = validated_data.get('priority_id')
        assigned_to_id: int = validated_data.get('assigned_to_id')

        try:

            TaskManagerPackage(
                title = title,
                task_id = task_id,
                due_date = due_date,
                status_id = status_id,
                description = description,
                priority_id = priority_id,
                assigned_to_id = assigned_to_id
            ).edit_task()

            response_data = json.dumps({
                'status': 'success',
                'message': 'Task updated successfully',
                'data': serialiazer.data
            })
            return Response(response_data, status=status.HTTP_201_CREATED)

        except ValueError as error:

            response_data = json.dumps({
                'status': 'error',
                'message': str(error),
                'data': {}
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to update task, please try again',
                'data': str(error)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def delete_task(self):

        data = self.request.data

        serialiazer: DeleteTaskSerializer = DeleteTaskSerializer(
            data = data
        )

        if not serialiazer.is_valid():

            response_data = json.dumps({
                'status': 'error',
                'message': 'Invalid data to API',
                'data': serialiazer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data: dict = serialiazer.validated_data
        task_id: int = validated_data.get('task_id')

        try:

            TaskManagerPackage(
                task_id = task_id,
            ).delete_task()

            response_data = json.dumps({
                'status': 'success',
                'message': 'Task deleted successfully',
                'data': serialiazer.data
            })
            return Response(response_data, status=status.HTTP_200_OK)

        except ValueError as error:

            response_data = json.dumps({
                'status': 'error',
                'message': str(error),
                'data': {}
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to delete task, please try again',
                'data': str(error)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def get_all_tasks(self):

        try:

            tasks = TaskManagerPackage(

            ).get_all_tasks()

            model_serializer: GetAllTaskModelSerializer = GetAllTaskModelSerializer(
                tasks,
                many = True
            )

            response_data = json.dumps({
                'status': 'success',
                'message': 'Tasks retrieved successfully',
                'data': model_serializer.data
            })
            return Response(response_data, status=status.HTTP_200_OK)

        except ValueError as error:

            response_data = json.dumps({
                'status': 'error',
                'message': str(error),
                'data': {}
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to retrieve tasks, please try again',
                'data': str(error)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def get_task(self):

        data = self.request.data

        serialiazer: GetTaskSerializer = GetTaskSerializer(
            data = data
        )

        if not serialiazer.is_valid():

            response_data = json.dumps({
                'status': 'error',
                'message': 'Invalid data to API',
                'data': serialiazer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data: dict = serialiazer.validated_data
        task_id: int = validated_data.get('task_id')

        try:

            task = TaskManagerPackage(
                task_id = task_id,
            ).get_task()

            model_serializer: GetAllTaskModelSerializer = GetAllTaskModelSerializer(
                task,
                many = False
            )

            response_data = json.dumps({
                'status': 'success',
                'message': 'Task retrieved successfully',
                'data': model_serializer.data
            })
            return Response(response_data, status=status.HTTP_200_OK)

        except ValueError as error:

            response_data = json.dumps({
                'status': 'error',
                'message': str(error),
                'data': {}
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to retrieve tasks, please try again',
                'data': str(error)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)






















