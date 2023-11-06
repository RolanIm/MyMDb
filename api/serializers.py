from rest_framework import serializers
from reviews.models import Author


class GetTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        required_fields = ('username', 'confirmation_code')
        fields = ('username', 'confirmation_code')


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        required_fields = ('email', 'username')
        fields = ('email', 'username')


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
