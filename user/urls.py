from django.urls import path
from .views import SignupView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
]
