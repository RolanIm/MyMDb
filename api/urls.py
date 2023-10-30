from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import routers


router = routers.DefaultRouter()
# router.register()

app_name = 'api_reviews'
urlpatterns = [
    # path('v1/auth/signup', )
    path(
        'v1/auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
]
