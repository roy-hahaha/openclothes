from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='store_images/')  # Store images in the 'store_images' directory

    def __str__(self):
        return self.name