from django.db import models

# Create your models here.
class Seller(models.Model):
    username = models.CharField(max_length=100)
    ebay_user_id = models.CharField(max_length=200, unique=True)
    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_at = models.DateTimeField()

    def __str__(self):
        return self.ebay_user_id
    
    