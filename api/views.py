from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import get_template
from django.shortcuts import get_object_or_404

from reviews.models import Author
from MyMDb.settings import EMAIL_HOST_USER
from .serializers import EmailTokenObtainPairSerializer, AuthorSerializer
from .permissions import IsAdminUser, IsSuperuser


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

    # @action(detailt=False, methods=['get',])
    # def signup(self, request):
    #     user = self.Author.objects.get_or_create()
    #     confirmation_token = default_token_generator.make_token(request.user)
    #     data = {'confirmation_token': confirmation_token}
    #     message = get_template('templates/email_confirmation.txt').render(data)
    #     send_mail(    ),

    #         subject='Please confirm email.',
    #         message=message,
    #         from_email=EMAIL_HOST_USER,
    #         recipient_list=['email'],
    #         fail_silently=False
    #     )


class AuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    permission_classes = (IsAdminUser,)

    def get_object(self):
        desired_username = self.kwargs.get('username')
        if desired_username:
            return self.queryset.get_object_or_404(username=desired_username)
        else:
            return self.queryset.get(user=self.request.user)

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
