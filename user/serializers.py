from rest_framework import serializers

from user.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={
            "input_type": "password"
        },
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password"
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
