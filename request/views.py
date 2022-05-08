from django.shortcuts import render
from account.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import datetime
from  . import models
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.

def NoteRequest(request):
    print(request.user)
    currentdate = datetime.date.today()
    teacher = User.objects.filter(is_teacher=True)
    return render(request,'request/note-request.html', context={
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'matricule': request.user.matricule,
        'email': request.user.email,
        'niveau': request.user.niveau,
        'filiere': request.user.filiere,
        'telephone': request.user.phone,
        'current_date':currentdate,
        'teacher':teacher
    })


@csrf_exempt
def operation_requete(request):
    a = request.POST.get("examen")
    b = request.POST.get("note1")
    c = request.POST.get("note2")
    d = request.POST.get("commentaire")

    template = models.Template.objects.create(
        examen = a, 
        note1 = b,
        note2 = c,
        commentaire = d
    )
    # account_sid = 'AC25fffecc0550d63d0eb20cd5793236b3'
    # auth_token = '4d01a37db834e77914780908a65492dc'
    # client = Client(account_sid, auth_token)

    # message = client.messages.create(
    #     body=f"Votre a bien été enregistré et envoyé",
    #     from_='+19378264862',
    #     to='+237697161353'
    # )

    # print(message.sid)
   
    # select_option = request.POST.get('options')
    # if select_option:
    #     subject = 'Notification'
    #     message = 'Une requête est en attente'
    #     email = select_option.email
    #     send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

    return JsonResponse({"operation_result": f"{template.examen} - {template.note1} - {template.note2} - {template.commentaire}"})


def notification(request):
    if request.method == 'POST':
        subject = 'Notification'
        message = 'Une requête est en attente \n lien de la plateforme: http://delroos.pythonanywhere.com/'
        email = request.POST.get('email')
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        return render(request, 'request/email_sent.html', {'email':email})