from django.db import models

class MyUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
class MyUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
class ExternalData(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    value = models.IntegerField()
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
