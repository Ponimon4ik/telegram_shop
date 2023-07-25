from django.db import models

from tg_users.models import TgUser


class Category(models.Model):
    title = models.CharField(max_length=20)


class Subcategory(models.Model):
    title = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')


class Product(models.Model):
    title = models.CharField(max_length=20)
    picture = models.ImageField()
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products')
    price = models.PositiveIntegerField()
    description = models.TextField(max_length=100)
    quantity = models.PositiveIntegerField()


class City(models.Model):
    name = models.CharField(max_length=50)


class Order(models.Model):
    customer = models.ForeignKey(TgUser, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='orders')
    shipping_address = models.TextField()
    phone = models.CharField(max_length=12,)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_ordered = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity_ordered
        super().save(*args, **kwargs)
