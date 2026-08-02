from django.urls import path
from .views import SignupView, LoginView, ProfileView,UserList,UserByUserNameView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('profile/', ProfileView.as_view()),
    path('username/<str:username>/', UserByUserNameView.as_view(),name="user-by-username"),
    path('userList/', UserList.as_view()),
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
]