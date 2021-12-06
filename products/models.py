from django.db import models

# Create your models here.


class Product_Category(models.Model):
    name = models.CharField(max_length=30)
    display_name = models.CharField(max_length=30)


    def __str__(self):
        return self.display_name



class Artist(models.Model):
    name = models.CharField(max_length=30)
    display_name = models.CharField(max_length=30)
    artist_description = models.TextField(max_length=250, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True, max_length=1000)
    image = models.ImageField(null=True, blank=True)
    artist_key = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.display_name


class Product(models.Model):
    product_category = models.ForeignKey('Product_Category', null=True, on_delete=models.SET_NULL)
    artist = models.ForeignKey('Artist', null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.DecimalField(max_digits=4, decimal_places=2)
    image_url = models.URLField(null=True, blank=True, max_length=1000)
    image = models.ImageField(null=True, blank=True)
    product_key = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.name
