from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

# Create your models here.

class Product (models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    price = models.FloatField(validators=[MinValueValidator(0)])
    inventory = models.IntegerField(default=0,
                                    validators=[MinValueValidator(0)])
    hsn_code = models.CharField(max_length=8, blank=True)
    tax = models.FloatField(validators=[MinValueValidator(0)])


    def __str__ (self):
        return self.name

class Bills (models.Model):

    #constant
    COLLECTION = (
        ("1", '(CGST/SGST)'),
        ("2", '(IGST)'),
    )

    invoice_date = models.DateField(default=timezone.now())
    to = models.CharField(max_length=100)
    collection = models.CharField(max_length=100, choices=COLLECTION, blank=False, default=1)

    def tax(self):
        return sum([((x.price*x.quantity)*int(x.category)/100) for x in self.billedproducts_set.all()])

    def total(self):
        return sum([x.price*x.quantity for x in self.billedproducts_set.all()])
    def tax_dict(self):
        res = {
            "5" : 0,
            "12" : 0,
            "18" : 0,
            "28" : 0
        }
        for x in self.billedproducts_set.all():
            res[str(x.category)] += (x.price*x.category*x.quantity)/100
        return res
    def price_tax_dict(self):
        res = {
            "5" : 0,
            "12" : 0,
            "18" : 0,
            "28" : 0
        }
        for x in self.billedproducts_set.all():
            res[str(x.category)] += (x.price*x.quantity)
        return res
    def totalQuantity(self):
        return sum([int(x.quantity) for x in self.billedproducts_set.all()])
    def grandTotal(self):
        return sum([(x.price*x.quantity) + ((x.price*x.quantity)*int(x.category)/100) for x in self.billedproducts_set.all()])

class BilledProducts (models.Model):

    #constants
    CATEGORIES = (
        (5, 5),
        (12, 12),
        (18, 18),
        (28, 28),
    )

    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    price = models.FloatField()
    bill = models.ForeignKey(Bills)

    category = models.IntegerField(choices = CATEGORIES)
    hsn = models.CharField(max_length=10)

    def taxTotal(self):
        return ((self.price * self.quantity)*self.category)/100

    def total(self):
        return self.price * self.quantity

    def grandTotal(self):
        return self.price * self.quantity + ((self.price * self.quantity)*self.category)/100

    def __str__ (self):
        return self.name

class Tax(models.Model):
    tax = models.FloatField(default=0)

    def __str__(self):
        return self.tax



