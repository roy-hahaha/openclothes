from django.db import models
from django.conf import settings

class Store(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    store_name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='store_images/')  # Store images in the 'store_images' directory

    def __str__(self):
        return self.store_name
    
class Clothes(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='clothes_images/')  # Store images in the 'clothes_images' directory

    def __str__(self):
        return self.name
    

class Selfie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='selfie_images/')
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Selfie by {self.user.username} for {self.store.store_name}"