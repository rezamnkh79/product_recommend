from django.urls import path

from users.views.login_view import LoginView
from users.views.user_view import UserView

urlpatterns = [
    path('/', UserView.as_view(), name='users'),
    path('login/', LoginView.as_view(), name='login'),

]
