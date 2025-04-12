from django.db import models

from global_app import constants as constant


class TaskPriority(models.Model):
    
    status = models.CharField(
        max_length = 255
    )

    def __str__(self):
        return self.status


class TaskProcess(models.Model):

    status = models.CharField(
        max_length = 255
    )

    def __str__(self):
        return self.status


class Task(models.Model):

    title = models.CharField(
        max_length = 255
    )
    description = models.TextField()
    date_created = models.DateTimeField(
        auto_now_add = True
    )
    date_modified = models.DateTimeField(
        auto_now = True
    )
    due_date = models.DateTimeField(
        null = True,
        blank = True
    )
    status = models.ForeignKey(
        TaskProcess,
        on_delete = models.PROTECT,
        default = constant.PENDING,
    )
    priority = models.ForeignKey(
        TaskPriority,
        on_delete = models.PROTECT,
    )
    assigned_to = models.ForeignKey(
        'system_management.User',
        on_delete = models.PROTECT,
        null = True,
        blank = True
    )
    created_by = models.ForeignKey(
        'system_management.User',
        on_delete = models.PROTECT,
        related_name = 'created_tasks',
        null = True,
        blank = True
    )

    def __str__(self):
        return self.title


class Team(models.Model):

    name = models.CharField(
        max_length = 255
    )
    description = models.TextField()
    date_created = models.DateTimeField(
        auto_now_add = True
    )
    date_modified = models.DateTimeField(
        auto_now = True
    )
    members = models.ManyToManyField(
        'system_management.User',
        related_name = 'teams'
    )
    is_assigned = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        'system_management.User',
        on_delete=models.PROTECT,
        related_name='created_teams',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class TeamRoles(models.Model):

    name = models.CharField(
        max_length = 255
    )
    date_created = models.DateTimeField(
        auto_now_add = True
    )
    date_modified = models.DateTimeField(
        auto_now = True
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='roles'
    )

    def __str__(self):
        return self.name


class TeamMemberRole(models.Model):

    date_created = models.DateTimeField(
        auto_now_add = True
    )
    date_modified = models.DateTimeField(
        auto_now = True
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT
    )
    team_role = models.ForeignKey(
        TeamRoles,
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
    'system_management.User',
    on_delete=models.PROTECT
    )

    def __str__(self):

        return f"{self.team.name} - {self.team_role.name}"