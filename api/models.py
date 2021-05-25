from django.db import models


# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=10, unique=True, null=False)
    desc = models.CharField(max_length=30, null=False)

