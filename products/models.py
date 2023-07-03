from django.db import models
from accounts.models import User


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='image_of_products')
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.title}'