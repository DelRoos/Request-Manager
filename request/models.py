from django.db import models

# Create your models here.

class Template(models.Model):
    examen = models.CharField(max_length = 10)
    note1 = models.CharField(max_length = 10)
    note2 = models.CharField(max_length = 10)
    commentaire = models.TextField()

    def __str__(self):
        return self.examen