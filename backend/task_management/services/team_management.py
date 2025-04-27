import json
from rest_framework import status
from rest_framework.response import Response

from task_management.packages.team_management import TeamManagerPackage
from task_management.serializer.base_serializer import (
    GetTeamSerializer,
    EditTeamSerializer,
    CreateTeamSerializer,
    DeleteTeamSerializer,
)
from task_management.serializer.model_serializer import (
    ViewTeamModelSerializer
)


class TeamManagerService:

    def __init__(
        self,
        request = None,
    ) -> None:

        self.request = request

    def create_team(self):

        user = self.request.user
        data = self.request.data

        serialiazer: CreateTeamSerializer = CreateTeamSerializer(
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
        name: str = validated_data.get('name')
        members: list = validated_data.get('members')
        description: str = validated_data.get('description')

        try:

            TeamManagerPackage(
                name = name,
                members = members,
                is_assigned = True,
                description = description,
                created_by_id = user.id,
            ).create_team()

            response_data = json.dumps({
                'status': 'success',
                'message': 'Team created successfully',
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
                'message': 'Failed to create team',
                'data': str(error)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def edit_team(self):

        data = self.request.data

        serializer: EditTeamSerializer = EditTeamSerializer(
            data = data
        )

        if not serializer.is_valid():

            response_data = json.dumps({
                'status': 'error',
                'message': 'Invalid data to API',
                'data': serializer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data: dict = serializer.validated_data
        name: str = validated_data.get('name')
        team_id: int = validated_data.get('team_id')
        members: int = validated_data.get('members')
        description: str = validated_data.get('description')

        try:

            TeamManagerPackage(
                team_id=team_id,
                name=name,
                members=members,
                description=description,
            ).edit_team()

            response_data = json.dumps({
                'status': 'success',
                'message': 'Team updated successfully',
                'data': serializer.data
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
                'message': 'Failed to update team',
                'data': str(error)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def delete_team(self):

        data = self.request.data

        serializer: DeleteTeamSerializer = DeleteTeamSerializer(
            data = data
        )

        if not serializer.is_valid():

            response_data = json.dumps({
                'status': 'error',
                'message': 'Invalid data to API',
                'data': serializer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data: dict = serializer.validated_data
        team_id: int = validated_data.get("team_id")

        try:

            TeamManagerPackage(
                team_id = team_id
            ).delete_team()

            response_data = json.dumps({
                'status': 'success',
                'message': 'Team deleted successfully.',
                'data': serializer.data
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
                'message': 'Failed to delete team',
                'data': str(error)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def view_team(self):

        data = self.request.data

        serializer: GetTeamSerializer = GetTeamSerializer(
            data = data
        )

        if not serializer.is_valid():

            response_data = json.dumps({
                'status': 'error',
                'message': 'Invalid data to API',
                'data': serializer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data: dict = serializer.validated_data
        team_id: int = validated_data.get("team_id")

        try:

            team: TeamManagerPackage = TeamManagerPackage(
                team_id = team_id
            ).get_team()

            model_serializer: ViewTeamModelSerializer = ViewTeamModelSerializer(
                team,
                many = False
            )

            response_data = json.dumps({
                'status': 'success',
                'message': 'Team retrieved successfully.',
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
                'message': 'Failed to retrieved team',
                'data': str(error)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def view_all_teams(self):

        try:

            teams: TeamManagerPackage = TeamManagerPackage(
                team_id = None
            ).view_all_teams()

            model_serializer: ViewTeamModelSerializer = ViewTeamModelSerializer(
                teams,
                many = True
            )

            response_data = json.dumps({
                'status': 'success',
                'message': 'Teams retrieved successfully.',
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
                'message': 'Failed to retrieved team',
                'data': str(error)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)









