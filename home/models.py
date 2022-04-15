from django.db import models

# Create your models here.
class Testimonials(models.Model):
    title = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    describe = models.CharField(max_length=500)
    profile = models.ImageField(upload_to="profiles")

    def __str__(self):
        return self.title + self.name + self.describe
    