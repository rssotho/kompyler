from django.utils import timezone

from task_management.models import ( 
    Team,
    TeamRoles,
    TeamMemberRole
)

from system_management.models import (
    User
)


class TeamManagerPackage:

    def __init__(
        self,
        # Team
        name: str = None,
        team_id: int = None,
        members: list = None,
        description: str = None,
        is_assigned: bool = None,
        created_by_id: int = None,

    ) -> None:

        self.name = name
        self.team_id = team_id
        self.members = members
        self.description = description
        self.is_assigned = is_assigned
        self.created_by_id = created_by_id

    def filter_members(self) -> list:

        if not self.members:

            return []

        members: list = []

        for member in self.members:

            try:

                user: User = User.objects.get(id = member)

                members.append(user)

            except User.DoesNotExist:

                raise ValueError(f"User with id {member} does not exist")

        return members

    def create_team(self) -> Team:

        members: list = self.filter_members()

        team: Team = Team.objects.create(
            name = self.name,
            description = self.description,
            is_assigned = self.is_assigned,
            created_by_id = self.created_by_id,
        )

        if not team:

            raise ValueError("Team was not created")

        if self.members:

            team.members.set(members)

        return team

    def get_team(self) -> Team:

        try:

            team: Team = Team.objects.get(
                id = self.team_id
            )

        except Team.DoesNotExist:

            raise ValueError("Team does not exist")

        return team

    def edit_team(self) -> Team:

        team: Team = self.get_team()

        team.name = self.name
        team.description = self.description

        if self.members is not None:

            members = self.filter_members()
            team.members.set(members)

        team.save()

        return team

    def delete_team(self) -> None:

        team: Team = self.get_team()

        if team.members.count() == 0:

            team.delete()

        else:

            raise ValueError("Cannot delete the team because it has members.")

        return True

    def view_all_teams(self) -> Team:

        team: Team = Team.objects.all()

        if not team:

            return {}

        return team




