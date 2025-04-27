from task_management.models import (
    Task,
    Team
)

from rest_framework import serializers


class GetAllTaskModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'due_date',
            'status_id',
            'description',
            'priority_id',
            'date_created',
            'created_by_id',
            'date_modified',
            'assigned_to_id',
        ]


class ViewTeamModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'members',
            'description',
        ]