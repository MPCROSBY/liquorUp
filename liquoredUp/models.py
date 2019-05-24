from django.db import models

# Create your models here.
from django.db.models import CASCADE


class Product(models.Model):
    name = models.CharField(max_length=128)
    desc = models.CharField(max_length=500)

    def __str__(self):
        return str(self.name)


class Competitor(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return str(self.name)

class PriceList(models.Model):
    product_fk = models.ForeignKey(Product, on_delete=CASCADE)
    price = models.FloatField()
    timestamp = models.DateTimeField()
    comp_fk = models.ForeignKey(Competitor, on_delete=CASCADE)

    def __str__(self):
        return str(self.comp_fk.name) + ' ' + str(self.product_fk.name)

