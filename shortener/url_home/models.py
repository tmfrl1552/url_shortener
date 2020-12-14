from django.db import models

# Create your models here.
class Url(models.Model):
    key = models.IntegerField()
    origin_url = models.URLField()
    shorten_url = models.TextField(default='')

    class Meta:
        db_table = 'url'