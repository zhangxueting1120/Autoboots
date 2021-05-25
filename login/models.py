from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)
    password = models.CharField(max_length=32, null=False)
    email = models.EmailField(max_length=50, null=False)
    def __unicode__(self):
        return self.name
