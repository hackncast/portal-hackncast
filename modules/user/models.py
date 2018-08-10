from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PasswordChanges(models.Model):
    user = models.ForeignKey(
        User, blank=False, null=False,
        on_delete=models.CASCADE,
        related_name="password_changes",
        related_query_name="password_change",
    )
    changed_at = models.DateTimeField(auto_now_add=True)
