from rest_framework import serializers

from reviews.models import Author
from reviews.validators import UnicodeUsernameValidator, validate_username

USERNAME_VALIDATORS = [UnicodeUsernameValidator, validate_username]


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150,
                                     required=True,
                                     validators=USERNAME_VALIDATORS)
    confirmation_code = serializers.CharField(max_length=255)


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150,
                                     required=True,
                                     validators=USERNAME_VALIDATORS)
    email = serializers.EmailField(required=True, max_length=254)


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        required_fields = ('email', 'username')
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    @staticmethod
    def validate_username(value):
        return validate_username(value)
