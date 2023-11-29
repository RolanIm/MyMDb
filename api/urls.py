from django.urls import path, include
from rest_framework import routers
from .views import (GetTokenView, AuthorViewSet, SignupView,
                    CategoryViewSet, GenreViewSet)

router = routers.DefaultRouter()
router.register(r'users', AuthorViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)

app_name = 'api_reviews'
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignupView.as_view()),
    path('v1/auth/token/', GetTokenView.as_view())
]
