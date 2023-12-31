from django.http import HttpRequest

from app_users.models import User


class UserHttpRequest(HttpRequest):
    user: User
