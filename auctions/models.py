from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"
    
class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to="images", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings", blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    watched = models.ManyToManyField(User, blank=True, related_name="watchlist")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Listing {self.id}: {self.title}, {self.price}"

class Bid(models.Model):
    bid = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.bid}"
    
class Comment(models.Model):
    text = models.CharField(max_length=256)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.user} printed ..."


