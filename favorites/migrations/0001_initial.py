# Generated by Django 4.2.5 on 2023-09-27 06:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteProducts',
            fields=[
                ('id',
                 models.BigAutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('created_at',
                 models.DateTimeField(
                     auto_now_add=True)),
                ('product',
                 models.ForeignKey(
                     on_delete=django.db.models.deletion.CASCADE,
                     to='products.product')),
                ('user',
                 models.ForeignKey(
                     on_delete=django.db.models.deletion.CASCADE,
                     to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
