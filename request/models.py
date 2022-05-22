from django.db import models
from account.models import User

# Create your models here.

class Template(models.Model):
    STATE = [
        ('loading', 'En redaction'),
        ('pending', 'En attente'),
        ('traitement', 'En traitement'),
        ('end', 'Terminer'),
    ]
    
    OBJET = [
        ('1', 'Rectification de note'),
    ]
    
    objet = models.CharField(max_length = 3, choices=OBJET,)
    commentaire = models.TextField()
    student = models.ForeignKey(User, on_delete = models.CASCADE, related_name="student_request")
    responsable = models.ForeignKey(User, on_delete = models.CASCADE, related_name="responsable_request")
    publish_date = models.DateField()
    status = models.CharField(
        max_length=12,
        choices=STATE,
        default="loading",
    )
    
    asset = models.FileField(blank = True, null=True)
    note1 = models.CharField(max_length = 10, blank = True, null=True)
    note2 = models.CharField(max_length = 10, blank = True, null=True)
    examen = models.CharField(max_length = 10, blank = True, null=True)

    def __str__(self):
        return self.examen