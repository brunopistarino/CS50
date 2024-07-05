from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"
    

class Listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    starting_bid = models.FloatField()
    image = models.URLField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="listing_category")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    closed = models.BooleanField(default=False)
    current_price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.category}) posted by {self.user}"

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listing_comments")
    comment = models.TextField()

    def __str__(self):
        return f"{self.user} in {self.listing}: {self.comment}"

class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_watchlist")
    listing = models.ManyToManyField(Listings, blank=True, related_name="listing_watchlist")

    def __str__(self):
        return f"{self.user}'s watchlist"

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    bid = models.FloatField()

    def __str__(self):
        return f"{self.user} bid {self.bid} for {self.listing}"