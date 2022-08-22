from django.db import models

# Create your models here.

class UserDetails(models.Model):
    username = models.CharField(max_length=20,primary_key=True)
    username.primary_key
    password = models.CharField(max_length=20)
    Wallet = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.username
    variable = models.Manager()
    objects = models.Manager()


class OrderDetails(models.Model):
    name = models.CharField(max_length=200)
    items = models.CharField(max_length=200)
    quantity = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.name
    variable = models.Manager()
    objects = models.Manager()
