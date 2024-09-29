from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True, blank=True)  # Allow null categories
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    # image_url = models.URLField()  # Store the URL/path of the image
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_trending = models.BooleanField(default=False)  # New field for trending products

    def __str__(self):
        return self.name



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('credit_card', 'Credit Card'),
            ('paypal', 'PayPal'),
            ('cash_on_delivery', 'Cash on Delivery')
        ],
        default='cash_on_delivery'
    )
    shipping_address = models.TextField()  # This allows free text input

    created_at = models.DateTimeField(auto_now_add=True)
      # Add this line to link to the user who placed the order

    def __str__(self):
        return f"Order for {self.product.name} - {self.quantity} units"



class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you want to associate cart items with users
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"