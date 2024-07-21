from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from weather.models import User, History


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.
    """
    class Meta:
        model = User
        fields = ("username", "password")

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения данных пользователя.
    """
    history = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "history")

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_history(self, obj):
        query = History.objects.filter(user=obj)
        history_dict = dict()
        for item in query:
            if item.city in history_dict.keys():
                history_dict[item.city] += 1
            else:
                history_dict[item.city] = 1
        return history_dict


class UserEditSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изменения данных пользователя.
    """

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")