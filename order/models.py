from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        db_table = 'client'
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    multiple = models.IntegerField(null=True)
    class Meta:
        db_table = 'product'
    def __str__(self):
        return self.name

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'order'

    @property
    def total(self):
        return sum(item.total for item in self.items.all())

    @property
    def quantity_sum(self):
        return sum(item.quantity for item in self.items.all())

class Item(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'item'

    @property
    def total(self):
        return self.price * self.quantity

    @property
    def profitability(self):
        from lib.order import OrderHelper

        order_helper = OrderHelper()
        return order_helper.get_profitability(self.price, self.product.price)
