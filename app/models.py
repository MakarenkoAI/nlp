from django.db import models


class File(models.Model):
    text = models.CharField(max_length = 1000)
    file = models.FileField()
