from django.db import models
from account.models import User

# Create your models here.

class Template(models.Model):
    examen = models.CharField(max_length = 10)
    note1 = models.CharField(max_length = 10)
    note2 = models.CharField(max_length = 10)
    commentaire = models.TextField()
    student = models.ForeignKey(User, on_delete = models.CASCADE, related_name="student_request")
    responsable = models.ForeignKey(User, on_delete = models.CASCADE, related_name="responsable_request")
    file = models.FileField()

    def __str__(self):
        return self.examen