from django.contrib.auth.models import AbstractUser
from django.db import models

class ClientUser(AbstractUser):
    invite_code = models.CharField(max_length=6, blank=True, null=True)
    other_code = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.username


