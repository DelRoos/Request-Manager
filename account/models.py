from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    is_jury= models.BooleanField('Is jury', default=False)
    is_teacher = models.BooleanField('Is teacher', default=False)
    is_student = models.BooleanField('Is student', default=False)
    matricule = models.CharField(max_length=7)
    filiere = models.CharField(max_length=15)
    niveau = models.CharField(max_length=3)
    phone = models.CharField(max_length=9)
    
    
    def __str__(self):
        if self.is_student :
            return f"{self.last_name}".capitalize() + f" {self.username} {self.filiere} - {self.niveau}"
        else :
            return "M. "+f"{self.last_name}".capitalize() + f" {self.username}"
            