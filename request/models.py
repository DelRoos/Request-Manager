from urllib import request
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
    
class RequestHistory(models.Model):
    request = models.ForeignKey(Template, on_delete = models.CASCADE, related_name="request_history")
    responsable = models.ForeignKey(User, on_delete = models.CASCADE, related_name="new_responsable")
    is_student = models.BooleanField(default=False)
    transfert_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.responsable} - {self.request.objet}"
    
class Comment(models.Model):
    request_history = models.ForeignKey(RequestHistory, on_delete = models.CASCADE, related_name="request_comment")
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="user_comment")
    content = models.TextField()

    def __str__(self):
        return self.content
    

class RequestImage(models.Model):
    image=models.ImageField(upload_to='images/')
    date = models.DateTimeField( auto_now_add=True)
    request = models.ForeignKey(Template, on_delete = models.CASCADE, related_name="request_image")

    class Meta:
        ordering=['-date']

    def __str__(self):
        return str(self.date)
    
    @property
    def image_url(self):    
        if self.image and hasattr(self.image, 'url'):        
            return self.image.url