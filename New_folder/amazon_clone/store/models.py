from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify

class Product(models.Model):
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    release_date = models.DateField()
    image_name = models.CharField(max_length=255, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.image_name:
            self.image_name = slugify(self.name)
        super().save(*args, **kwargs)
    
    # Your existing methods

    def __str__(self):
        return self.name

    def avg_rating(self):
        reviews = self.review_set.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0

    def review_count(self):
        return self.review_set.count()

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    author = models.CharField(max_length=255)
    body = models.TextField()
    release_date = models.DateField(default=timezone.now)
    release_time = models.TimeField(default=timezone.now)

    def __str__(self):
        return f"{self.author}'s review on {self.product.name}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username}'s cart item: {self.product.name}"

class Order(models.Model):
    STATUS_CHOICES = (
        ('Processing', 'Processing'),
        ('On its way', 'On its way'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Processing')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} × {self.product.name} in Order #{self.order.id}"