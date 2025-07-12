from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=100)

    def __str__(self):
        return self.user.username


class Item(models.Model):
    TYPE_CHOICES = [
        ('swap', 'Swap'),
        ('redeem', 'Redeem'),
        ('sell', 'Sell'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('swapped', 'Swapped'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)
    size = models.CharField(max_length=10)
    condition = models.CharField(max_length=50)
    tags = models.CharField(max_length=200, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    price = models.PositiveIntegerField(null=True, blank=True)  # used for 'sell' and 'redeem'
    image = models.ImageField(upload_to='items/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SwapRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='received_swap_requests')  # User B's item
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    offered_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='offered_in_swaps')  # User A's item
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requester.username} offered {self.offered_item.title} → {self.item.title} ({self.status})"



class SellRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer.username} wants to buy {self.item.title} ({self.status})"
