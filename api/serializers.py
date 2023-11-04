from typing import Dict, Any
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from reviews.models import Author


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer,
                                     serializers.ModelSerializer):

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        pass


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        required_fields = ('email', 'username')
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')

    @staticmethod
    def validate_username(value):
        if value == 'me':
            raise serializers.ValidationError(
                "Username field can't equals 'me'."
            )
        return value
