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
from django.contrib import messages
import datetime

# Create your views here.

def NoteRequest(request):
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
            template = Template.objects.get(student=request.user, pk=req)
            return render(request,'request/note-request.html', context={
                "student": request.user,
                'current_date': currentdate,
                'teacher': teacher,
                "template": template,
            })
        except Template.DoesNotExist:
            raise Http404("Vous ne pouvez pas accerdez a cette requette")
    



@csrf_exempt
def operation_requete(request):
    exam = request.POST.get("examen")
    note1 = request.POST.get("note1")
    note2 = request.POST.get("note2")
    comment = request.POST.get("commentaire")
    resp = request.POST.get("responsable")
    asset = request.POST.get("asset")
    objet = request.POST.get("object")

    teacher = User.objects.filter(pk=int(resp))[0]

    template = Template.objects.create(
        examen = exam, 
        note1 = note1,
        note2 = note2,
        commentaire = comment,
        student=request.user,
        responsable = teacher,
        asset = asset,
        objet = objet,
        publish_date = datetime.date.today()
    )
    return JsonResponse(
        {
            "id":f"{template.id}",
            "operation_result": f"{template.examen} - {template.note1} - {template.note2} - {template.commentaire} -"
        }
    )
    
@csrf_exempt
def operation_edit_requete(request, id):
    exam = request.POST.get("examen")
    note1 = request.POST.get("note1")
    note2 = request.POST.get("note2")
    comment = request.POST.get("commentaire")
    resp = request.POST.get("responsable")
    asset = request.POST.get("asset")
    objet = request.POST.get("object")
        
    teacher = User.objects.filter(pk=int(resp))[0]


  
    try:
        template = Template.objects.get(student=request.user, pk=id)
        
        if template.status != "loading":
            return JsonResponse(
                    {
                        "error": "Cette requete ne peut plus etre modifier car elle a deja ete publier"
                    }
                )
            
        template.examen = exam
        template.note1 = note1
        template.note2 = note2
        template.commentaire = comment
        template.responsale = teacher
        template.asset = asset
        template.objet = objet
        template.publish_date = datetime.date.today()
        
        template.save()
        
        return JsonResponse(
            {
                "id":f"{template.id}",
                "operation_result": f"{template.examen} - {template.note1} - {template.note2} - {template.commentaire} -"
            }
        )
        
    except Template.DoesNotExist:
        raise Http404("Vous ne pouvez pas accerdez a cette requette")

def notification(request, id):
    template = get_object_or_404(Template, pk = id)
    template.status = "pending"
    template.save()
    
    subject = f'Nouvelle requete etudiant {template.student.filiere}-{template.student.niveau}'
    message = f"Vous avez recu une requete de l'etudiant {template.student.last_name} {template.student.first_name} en {template.student.filiere}-{template.student.niveau}. Concernant un probleme de {template.objet}"
   
    email = template.responsable.email
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
    return redirect('account:studenttable')
    return render(request, {'email':email})


def preview(request, id):
    template = get_object_or_404(Template, pk = id)
    examen = template.examen,
    note1 = template.note1,
    note2 = template.note2,
    commentaire = template.commentaire,
    responsable = template.responsable,
    asset = template.asset

    currentdate = datetime.date.today()
    return render(request, "request/preview.html", {
        'template': template,
    })


    
# Detail d'une requete    
def detail_request(request, id):
    template = get_object_or_404(Template, pk = id)
    
    return render(request, "request/preview.html", {
        'template': template,
    })
    
# Delete request 
def delete_template(request, template_id):
    template = Template.objects.get(pk=template_id)
    template.delete()
    messages.info(request, 'Template successfully delete')
    return redirect('index')


def edit(request, id = None):
    currentdate = datetime.date.today()
    teacher = User.objects.filter(is_teacher=True)
    try:
        template = Template.objects.get(student=request.user, pk=id, status="loading")
        # print(template.id)
       
        return render(request, 'request/note-request.html', context={
            "student": request.user,
            'current_date':currentdate,
            'teacher':teacher,
            "template": template,
        })
    except Template.DoesNotExist:
        raise Http404("Vous ne pouvez pas accerdez a cette requette")
        