from pydoc import describe
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
    
    objet = models.CharField(max_length = 255,)
    describe = models.TextField(blank=True, null=True)
    existant = models.IntegerField(default=0)
    student = models.ForeignKey(User, on_delete = models.CASCADE, related_name="student_request")
    responsable = models.ForeignKey(User, on_delete = models.CASCADE, related_name="responsable_request")
    publish_date = models.DateField()
    status = models.CharField(
        max_length=12,
        choices=STATE,
        default="loading",
    )
    state = models.BooleanField(default=False)
    asset = models.FileField(blank = True, null=True)
    note1 = models.CharField(max_length = 10, blank = True, null=True)
    note2 = models.CharField(max_length = 10, blank = True, null=True)
    examen = models.CharField(max_length = 10, blank = True, null=True)
    ue = models.CharField(max_length = 50, blank = True, null=True)

    def __str__(self):
        return self.objet
    
class RequestHistory(models.Model):
    request = models.ForeignKey(Template, on_delete = models.CASCADE, related_name="request_history")
    responsable = models.ForeignKey(User, on_delete = models.CASCADE, related_name="new_responsable")
    is_student = models.BooleanField(default=False)
    transfert_date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.responsable}"
    
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
    describe = models.CharField(max_length = 300, blank=True, null=True)

    class Meta:
        ordering=['-date']

    def __str__(self):
        return f"{self.request.objet}"
    
    @property
    def image_url(self):    
        if self.image and hasattr(self.image, 'url'):        
            return self.image.url