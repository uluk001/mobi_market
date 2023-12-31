from django.db import models
from accounts.models import CustomUser


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    more_info = models.TextField(default='')
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='image_of_products')
    owner = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.title}'


class AdditionalImage(models.Model):
    image = models.ImageField(upload_to='image_of_products')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.product.title}'
