import os

from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_default_user(sender, **kwargs):
    from django.contrib.auth import get_user_model

    email = os.environ.get('DEFAULT_USER_EMAIL')
    password = os.environ.get('DEFAULT_USER_PASSWORD')
    if not email or not password:
        return
    User = get_user_model()
    if not User.objects.filter(email=email).exists():
        user = User.objects.create_superuser(email=email, password=password)
        user.name = os.environ.get('DEFAULT_USER_NAME', 'Admin')
        user.save()


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_core'

    def ready(self):
        post_migrate.connect(create_default_user, sender=self)
