from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    is_new = models.BooleanField()
    is_discounted = models.BooleanField()
    slug = models.SlugField()
    category = models.ForeignKey('shop.Category', on_delete=models.CASCADE)
    brand = models.ForeignKey('shop.Brand', on_delete=models.CASCADE)
    thumb = models.ImageField(default='default.png')


    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'shop_products'



class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'shop_categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'shop_brands'
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

class Slide(models.Model):
   image = models.ImageField(default='default.jpg')

class Meta:
    verbose_name = 'Slide'
    verbose_name_plural = 'Slides'
    db_table = 'shop_slides'

class CartItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title
    
    def total_price(self):
        return self.product.price * self.quantity
    
    class Meta:
        db_table = 'shop_cart_items'
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone = models.IntegerField()
    total_price = models.IntegerField

    def __str__(self):
        return f'Order #{self.pk}'
    
    class Meta:
        db_table = 'shop_orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderProduct(models.Model):
    order = models.ForeignKey('shop.Order', on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    amount = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return f"{self.product} x{self.amount} - {self.order.customer.username}"

    class Meta:
        db_table = 'shop_orders_products'
        verbose_name = 'Order Product'
        verbose_name_plural = 'Order Products'