from django.db import models

# Create your models here.
class Equity(models.Model):
    name = models.CharField(default="Ticker",max_length=50)
    ticker = models.CharField(max_length=50)
    description = models.TextField(default="No Description",max_length=1000)
    def __str__(self):
        return self.name

