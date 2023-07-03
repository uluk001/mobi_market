from django.db import models
from accounts.models import User
from products.models import Product

class FavoriteProducts(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)