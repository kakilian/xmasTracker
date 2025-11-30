from django.db import models

# Create your models here.


class SavedGift(models.Model):
    reciepient_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price_range = models.CharField(max_length=50)
    gift_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} for {self.reciepient_name}"
