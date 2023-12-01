from rest_framework import status, viewsets, views, mixins, filters
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import tokens, login

from reviews.models import Author, Category, Genre, Title, ADMIN
from .utils import send_email
from .serializers import (GetTokenSerializer,
                          AuthorSerializer,
                          SignupSerializer,
                          CategorySerializer,
                          GenreSerializer,
                          TitleSerializer)
from .permissions import IsAdminUser
from .viewsets import ListCreateDestroyViewSet


class GetTokenView(views.APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        username = validated_data.get('username')
        confirmation_code = validated_data.get('confirmation_code')

        try:
            user = Author.objects.get(username=username)
        except Author.DoesNotExist:
            error_data = {"username": f"User {username} does not exist."}
            return Response(error_data, status=status.HTTP_404_NOT_FOUND)
        is_token_confirmed = tokens.default_token_generator.check_token(
            user,
            token=confirmation_code
        )
        if is_token_confirmed:
            login(request, user)
            token = AccessToken.for_user(user)
            data = {"token": str(token)}
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
        if user.is_admin and user.role != ADMIN:
            user.role = ADMIN
            user.save()
        confirmation_code = tokens.default_token_generator.make_token(user)
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
    lookup_field = 'username'
    permission_classes = (IsAdminUser,)

    def get_object(self):
        if self.kwargs.get('username') == 'me':
            return self.request.user
        return super().get_object()

    def get_permissions(self):
        if (self.action in ('retrieve', 'partial_update')
                and self.kwargs.get('username') == 'me'):
            return (IsAuthenticated(),)
        return super().get_permissions()

    def partial_update(self, request, *args, **kwargs):
        if (not request.data.get('role') or
                isinstance(self.get_permissions()[0], IsAdminUser)):
            return super().partial_update(request, *args, **kwargs)
        error_msg = {
            "role": "You can't change your role."
        }
        return Response(data=error_msg, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object():
            error_msg = {"username": "You can't destroy yourself account."}
            return Response(data=error_msg,
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(self, request, *args, **kwargs)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category__slug', 'genre__slug', 'name', 'year')
    permission_classes = (IsAdminUser,)

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return (AllowAny(),)
        return super().get_permissions()

