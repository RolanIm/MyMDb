from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import routers
from .views import EmailTokenObtainPairView, AuthorViewSet

router = routers.DefaultRouter()
router.register(r'users/(?P<username>[\w.@\+\-]+)|(me)',
                AuthorViewSet)

app_name = 'api_reviews'
urlpatterns = [
    path('v1/', include(router.urls)),
    # path(
    #     'v1/auth/token/',
    #     EmailTokenObtainPairView.as_view(),
    #     name='token_obtain_pair_view'
    # ),
]
