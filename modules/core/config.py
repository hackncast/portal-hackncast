from django.apps import AppConfig
from django.db.models.signals import pre_save

from . import signals


class CoreConfig(AppConfig):
    name = 'modules.core'

    def ready(self):
        from django.contrib.auth.models import User
        pre_save.connect(signals.password_changed, sender=User)
