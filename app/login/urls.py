from django.urls import path

from app.login.views import LoginFormView, LogoutView, UserCreationView

urlpatterns = [
    path('', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registrar/', UserCreationView.as_view(), name='create_user'),
]
