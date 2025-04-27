from rest_framework.decorators import (
    api_view,
)

from global_app import constants as constant
from global_app.roles_required import roles_required

from task_management.services.task_management import TaskManagerService
from task_management.services.team_management import TeamManagerService

@api_view(['POST'])
@roles_required(
    constant.SYSTEM_ADMIN,
)
def create_task(request):

    response = TaskManagerService(
        request = request
    ).create_task()

    return response


@api_view(['GET'])
@roles_required(
    constant.SYSTEM_ADMIN,
)
def edit_task(request):

    response = TaskManagerService(
        request = request
    ).edit_task()

    return response


@api_view(['DELETE'])
@roles_required(
    constant.SYSTEM_ADMIN,
)
def delete_task(request):

    response = TaskManagerService(
        request = request
    ).delete_task()

    return response


@api_view(['GET'])
@roles_required(
    constant.CUSTOMER,
    constant.SYSTEM_ADMIN,
)
def get_all_tasks(request):

    response = TaskManagerService(
        request = request
    ).get_all_tasks()

    return response


@api_view(['GET'])
@roles_required(
    constant.SYSTEM_ADMIN,
)
def get_task(request):

    response = TaskManagerService(
        request = request
    ).get_task()

    return response


@api_view(['POST'])
@roles_required(
    constant.SYSTEM_ADMIN,
)
def create_team(request):

    response = TeamManagerService(
        request = request
    ).create_team()

    return response


@api_view(['GET'])
@roles_required(
    constant.SYSTEM_ADMIN,
)
def edit_team(request):

    response = TeamManagerService(
        request = request
    ).edit_team()

    return response


@api_view(['DELETE'])
@roles_required(
    constant.SYSTEM_ADMIN,
)
def delete_team(request):

    response = TeamManagerService(
        request = request
    ).delete_team()

    return response


@api_view(['GET'])
@roles_required(
    constant.CUSTOMER,
    constant.SYSTEM_ADMIN,
)
def view_team(request):

    response = TeamManagerService(
        request = request
    ).view_team()

    return response



@api_view(['GET'])
@roles_required(
    constant.CUSTOMER,
    constant.SYSTEM_ADMIN,
)
def view_all_teams(request):

    response = TeamManagerService(
        request = request
    ).view_all_teams()

    return response





















