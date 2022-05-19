from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, Http404
from account.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import datetime
from django.conf import settings
from django.core.mail import send_mail
from django import forms
from .models import Template

# Create your views here.

def NoteRequest(request):
    print(request.user)
    currentdate = datetime.date.today()
    teacher = User.objects.filter(is_teacher=True)
    if request.GET == {}:
        return render(request,'request/note-request.html', context={
            "student": request.user,
            'current_date':currentdate,
            'teacher':teacher
        })
    else:
        # try except logic
        try:
            req = request.GET.get("req")
            queryset = Template.objects.get(student=request.user, pk=req)
            return render(request,'request/note-request.html', context={
                "student": request.user,
            'current_date':currentdate,
                'teacher':teacher
            })
        except Template.DoesNotExist:
            raise Http404("Vous ne pouvez pas accerdez a cette requette")
    



@csrf_exempt
def operation_requete(request):
    a = request.POST.get("examen")
    b = request.POST.get("note1")
    c = request.POST.get("note2")
    d = request.POST.get("commentaire")
    e = request.POST.get("responsable")
    teacher = User.objects.filter(pk=int(e))[0]
    f = request.POST.get("file")

    if request.GET == {}:
        template = Template.objects.create(
            examen = a, 
            note1 = b,
            note2 = c,
            commentaire = d,
            student=request.user,
            responsable = teacher,
            file = f
        )
        return JsonResponse(
            {
                "id":f"{template.id}",
                "operation_result": f"{template.examen} - {template.note1} - {template.note2} - {template.commentaire} -"
            }
        )
    else:
        print("an request for all")
        try:
            req = request.GET.get("req")
            template = Template.objects.get(student=request.user, pk=req)
            
            return JsonResponse(
                {
                    "id":f"{template.id}",
                    "operation_result": f"{template.examen} - {template.note1} - {template.note2} - {template.commentaire} -"
                }
            )
        except Template.DoesNotExist:
            raise Http404("Vous ne pouvez pas accerdez a cette requette")
    


def notification(request):
    # if request.method == 'POST':
    #     subject = 'Notification'
    #     message = 'Une requête est en attente \n lien de la plateforme: http://delroos.pythonanywhere.com/'
    #     email = request.POST.get('email')
    #     send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
    #     return render(request, 'request/email_sent.html', {'email':email})
    subject = 'Notification'
    message = 'Une requête est en attente \n lien de la plateforme: http://delroos.pythonanywhere.com/'
    email = request.POST.get('user.email')
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
    return render(request, 'request/email_sent.html', {'email':email})


def preview(request, id):
    template = get_object_or_404(Template, pk = id)
    examen = template.examen,
    note1 = template.note1,
    note2 = template.note2,
    commentaire = template.commentaire,
    responsable = template.responsable,
    print(responsable)
    file = template.file

    currentdate = datetime.date.today()
    return render(request, "request/preview.html", {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'matricule': request.user.matricule,
        'email': request.user.email,
        'niveau': request.user.niveau,
        'filiere': request.user.filiere,
        'telephone': request.user.phone,
        'examen':examen, 
        'note1':note1,
        'note2':note2, 
        'commentaire':commentaire,
        'responsable':responsable,
        'file':file,
        'current_date':currentdate,
        'template': template,
    })


def delete_template(request, template_id):
    template = Template.objects.get(pk=template_id)
    template.delete()
    messages.info(request, 'Template successfully delete')
    return redirect('index')


def edit(request):
    currentdate = datetime.date.today()
    teacher = User.objects.filter(is_teacher=True)
    return render(request, 'request/note-request.html', context={
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