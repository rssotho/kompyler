from rest_framework import serializers


class CreateTaskSerializer(serializers.Serializer):

    title = serializers.CharField(
        max_length = 255,
    )
    description = serializers.CharField()
    due_date = serializers.DateTimeField()
    priority_id = serializers.IntegerField()
    assigned_to_id = serializers.IntegerField()


class EditTaskSerializer(serializers.Serializer):

    title = serializers.CharField(
        max_length = 255,
    )
    task_id = serializers.IntegerField()
    description = serializers.CharField()
    due_date = serializers.DateTimeField()
    status_id = serializers.IntegerField()
    priority_id = serializers.IntegerField()
    assigned_to_id = serializers.IntegerField()


class DeleteTaskSerializer(serializers.Serializer):

    task_id = serializers.IntegerField()


class GetTaskSerializer(serializers.Serializer):

    task_id = serializers.IntegerField()


class CreateTeamSerializer(serializers.Serializer):

    name = serializers.CharField(
        max_length = 255,
    )
    members = serializers.ListField(
        child = serializers.IntegerField(),
        allow_empty = False,
        required = False
    )
    description = serializers.CharField()


class EditTeamSerializer(serializers.Serializer):

    team_id = serializers.IntegerField()
    name = serializers.CharField(
        max_length = 255
    )
    members = serializers.ListField(
        child = serializers.IntegerField(),
        allow_empty = True,
        required = False
    )
    description = serializers.CharField()


class DeleteTeamSerializer(serializers.Serializer):

    team_id = serializers.IntegerField()


class GetTeamSerializer(serializers.Serializer):

    team_id = serializers.IntegerField()



