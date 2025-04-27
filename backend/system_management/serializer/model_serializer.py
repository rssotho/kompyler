from rest_framework import serializers

from system_management.models import (
    User,
    Profile,
)


class ViewProfileModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'id',
            'town',
            'race',
            'gender',
            'country',
            'province',
            'postal_code',
            'street_address',
        )


class ViewUserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'role',
            'email',
            'last_name',
            'first_name',
            'phone_number',
        )


class GetUserModelSerializer(serializers.ModelSerializer):

    role = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = (
            'id',
            'role',
            'email',
            'last_name',
            'first_name',
            'phone_number',
        )
    def get_role(self, obj):

        return obj.role.role if obj.role else None 








