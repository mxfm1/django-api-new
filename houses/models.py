from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Residence(models.Model):
    identifier = models.CharField(max_length=100,unique=True,primary_key=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="houses",
        limit_choices_to={'is_superuser':False}
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_by"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
