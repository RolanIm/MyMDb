from rest_framework import status, viewsets, views
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator

from reviews.models import Author
from .utils import send_email
from .serializers import (GetTokenSerializer,
                          AuthorSerializer,
                          SignupSerializer)
from .permissions import IsAdminUser


class GetTokenView(views.APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        # TODO: Given token not valid for any token type.
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        username = validated_data.get('username')
        confirmation_code = validated_data.get('confirmation_code')

        try:
            user = Author.objects.get(username=username)
        except Author.DoesNotExist:
            error_data = {"username": "User does not exist."}
            return Response(error_data, status=status.HTTP_404_NOT_FOUND)

        is_token_confirmed = default_token_generator.check_token(
            user,
            token=confirmation_code
        )
        if is_token_confirmed:
            token = RefreshToken.for_user(user)
            data = {"username": username, "confirmation_code": token['jti']}
            return Response(data, status=status.HTTP_200_OK)

        error_data = {"confirmation_code": "Confirmation code is wrong."}
        return Response(error_data, status=status.HTTP_400_BAD_REQUEST)


class SignupView(views.APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username, email = serializer.data['username'], serializer.data['email']
        user, created = Author.objects.get_or_create(username=username,
                                                     email=email)
        confirmation_code = default_token_generator.make_token(user)
        data = {
            'username': user.username,
            'email': user.email,
            'confirmation_code': confirmation_code
        }
        send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsAdminUser,)

    def get_object(self):
        desired_username = self.kwargs.get('username')
        if desired_username:
            return get_object_or_404(self.queryset, username=desired_username)
        return self.request.user

    def get_permissions(self):
        if (self.action in ('retrieve', 'partial_update')
                and self.request.user == self.get_object()):
            return (IsAuthenticated(),)
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object():
            request.data["username"] = "You can't destroy yourself account."
            return Response(data=request.data, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(self, request, *args, **kwargs)
