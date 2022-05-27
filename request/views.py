from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, Http404
from account.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import datetime
from django.conf import settings
from django.core.mail import send_mail
from django import forms
from .models import Template, RequestHistory, Comment
from django.contrib import messages
import datetime
from django.db.models import Q
from django.urls import reverse

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
    
    
    request_history = RequestHistory.objects.create(
        request = template,
        responsable = template.responsable,
        is_student = False
    )
    
    subject = f'Nouvelle requete etudiant {template.student.filiere}-{template.student.niveau}'
    message = f"Vous avez recu une requete de l'etudiant {template.student.last_name} {template.student.first_name} en {template.student.filiere}-{template.student.niveau}. Concernant un probleme de {template.objet}"
   
    email = template.responsable.email
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
    return redirect('account:studenttable')
    return render(request, {'email':email})

def preview(request, id):
    
    try:
        template = Template.objects.filter(student=request.user, id=id)[0]
        # print(template.id)
       
        return render(request, 'request/preview.html', context={
            "template": template,
        })
    except Template.DoesNotExist:
        raise Http404("Vous ne pouvez pas accerdez a cette requette")
    
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

def follow(request, id):
    try:
        templates = Template.objects.filter((Q(responsable=request.user) | Q(student=request.user)) & Q(id = id))[0]
        list_history = RequestHistory.objects.filter(request=templates)
        

        return render(request, 'request/follow.html', context={
            "histories": list_history,
            "user": request.user,
            "template": templates,
            "history": list_history.last(),
        })
    except Template.DoesNotExist:
        raise Http404("Vous ne pouvez pas accerdez a cette requette")
    

@csrf_exempt
def post_comment(request):
    try:    
        content = request.POST.get("content")
        req_id = request.POST.get("req")
        user = request.user
        template_id = request.POST.get("template")

        print(req_id)
  
        request_history = RequestHistory.objects.get(id=req_id)
        
        comment = Comment.objects.create(
            content=content,
            request_history = request_history,
            user = user
        )
        
        print(comment.content)

        # return redirect('follow', kwargs={'id': template_id})
        return JsonResponse(
            {
                "id":f"{comment.id}",
            }
        )
    except Exception as excp:
        print(excp)
        raise Http404("Vous ne pouvez pas accerdez a cette requette")
    

@csrf_exempt
def change_state(request):
    try:    
        req_id = request.POST.get("req")
        template_id = request.POST.get("template")
        
        user = request.user
        
        request_history = RequestHistory.objects.get(id=req_id)
        template = Template.objects.get(id=template_id)
        
        if user.is_teacher:
            request_history.is_student = True
            
            subject = f"Reponse de {user.first_name} {user.last_name} pour la requete {template.objet} "
            message = f"L'enseignant {user.first_name} {user.last_name} a repondu a votre requete "
        
            email = user.email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        else:
            
            request_history.is_student = True
            
            subject = f"Reponse de {user.first_name} {user.last_name} pour la requete {template.objet} "
            message = f"L'etudiant {user.first_name} {user.last_name} a repondu a votre requete "
        
            email = user.email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            request_history.is_student = False

        request_history.save()            
        
        # return redirect('follow', kwargs={'id': template_id})
        return JsonResponse(
            {
                "id":f"{request_history.id}",
            }
        )
    except Exception as excp:
        print(excp)
        raise Http404("Vous ne pouvez pas accerdez a cette requette")
    


@csrf_exempt
def transfert_request(request):
    try:
        
        template_id = request.POST.get("template")
        to_teach_id = request.POST.get("to_teacher")
        user = request.user
        
        template = Template.objects.get(id=template_id)
        to_teacher = request.user
        
        
        request_history = RequestHistory.objects.create(
            request = template,
            responsable = to_teacher,
        )
        
        subject = "Requete transferer"
        message = f"M.{user.first_name} {user.last_name} Vous a transferez une requete de l'etudiant {template.student.last_name} {template.student.first_name} en {template.student.filiere}-{template.student.niveau}. Concernant un probleme de {template.objet}"
    
        email = to_teacher.email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        # return redirect('account:teacher')

        return JsonResponse(
            {
                "id":f"{request_history.id}",
            }
        )
    except Template.DoesNotExist:
        raise Http404("Vous ne pouvez pas accerdez a cette requette")
