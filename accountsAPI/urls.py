from django.urls import path
from . import views

# roote url api/
urlpatterns = [
    path("api-register/",views.RegisterUser.as_view()),
    path('api-login/', views.LoginView.as_view(), name='api-login'),
    path('users/', views.UserListAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailAPIView.as_view(), name='user-detail'),
    # path('company/',views , name=''),
    
]
