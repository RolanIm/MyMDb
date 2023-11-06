from rest_framework import status, generics, views, viewsets
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from reviews.models import Author
from .utils import send_email
from .serializers import (GetTokenSerializer,
                          AuthorSerializer,
                          SignupSerializer)
from .permissions import IsAdminUser, IsSuperuser


class GetTokenView(generics.GenericAPIView):
    # TODO: create view
    # TODO: delete last migrations and confirmation_code field in Author model
    queryset = Author.objects.all()
    serializer_class = GetTokenSerializer
    permission_classes = (AllowAny,)

    # def post(self, request):
    #
    #     default_token_generator.check_token(
    #         user, token=request.data.get('confirmation_code')
    #     )


class SignupView(generics.GenericAPIView):
    queryset = Author.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_code = default_token_generator.make_token(user)
        data = {
            'username': user.username,
            'email': user.email,
            'confirm_token': confirmation_code
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
