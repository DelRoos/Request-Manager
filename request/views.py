from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, Http404
from account.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import datetime
from django.conf import settings
from django import forms

from utils.functions import send_mail
from .models import RequestImage, Template, RequestHistory, Comment
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required



@login_required(login_url='/')
def emptyTemplate(request):
    currentdate = datetime.date.today()
    teacher = User.objects.filter(is_teacher=True)
    if request.GET == {}:
        
        return render(request,'empty_template/empty_request.html', context={
            "student": request.user,
            'current_date': currentdate,
            'teacher': teacher
        })
    else:
        # try except logic
        try:
            req = request.GET.get("req")
            template = Template.objects.get(student=request.user, pk=req)
            return render(request,'empty_template/empty_request.html', context={
                "student": request.user,
                'current_date': currentdate,
                'teacher': teacher,
                "template": template,
            })
        except Template.DoesNotExist:
            raise Http404("Vous ne pouvez pas accerdez a cette requette")

# Create your views here.
@login_required(login_url='/')
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





@login_required(login_url='/')
def EvaluationRequest(request):
    currentdate = datetime.date.today()
    teacher = User.objects.filter(is_teacher=True)
    # if request.GET == {}:
        
    return render(request,'request/evaluation-request.html', context={
        "student": request.user,
        'current_date':currentdate,
        'teacher':teacher
    })
    # else:

    #     try:
    #         req = request.GET.get("req")
    #         template = Template.objects.get(student=request.user, pk=req)
    #         return render(request,'request/evaluation-request.html', context={
    #             "student": request.user,
    #             'current_date': currentdate,
    #             'teacher': teacher,
    #             "template": template,
    #         })
    #     except Template.DoesNotExist:
    #         raise Http404("Vous ne pouvez pas accerdez a cette requette")





@login_required(login_url='/')
def UniqueRequest(request):
    currentdate = datetime.date.today()
    teacher = User.objects.filter(is_teacher=True)
    # if request.GET == {}:
        
    return render(request,'request/unique-request.html', context={
        "student": request.user,
        'current_date':currentdate,
        'teacher':teacher
    })
    # else:

    #     try:
    #         req = request.GET.get("req")
    #         template = Template.objects.get(student=request.user, pk=req)
    #         return render(request,'request/evaluation-request.html', context={
    #             "student": request.user,
    #             'current_date': currentdate,
    #             'teacher': teacher,
    #             "template": template,
    #         })
    #     except Template.DoesNotExist:
    #         raise Http404("Vous ne pouvez pas accerdez a cette requette")





    
@login_required(login_url='/')
@csrf_exempt
def operation_requete(request):
    exam = request.POST.get("examen")
    note1 = request.POST.get("note1")
    note2 = request.POST.get("note2")
    comment = request.POST.get("comment")
    resp = request.POST.get("responsable")
    asset = request.POST.get("asset")
    objet = request.POST.get("object")
    existant = request.POST.get("existant")
    
    print(f"Exam: {exam} | Note1: {note1} | Note2: {note2} | Comment: {comment} | Resp: {resp} | Objet: {objet}")
    
    teacher = User.objects.filter(pk=int(resp))[0]

    template = Template.objects.create(
        examen = exam, 
        note1 = note1,
        note2 = note2,
        describe = comment,
        existant = existant,
        student=request.user,
        responsable = teacher,
        asset = asset,
        objet = objet,
        publish_date = datetime.date.today()
    )

    
    
    return JsonResponse(
        {
            "id":f"{template.id}",
            "operation_result": f"{template.examen} - {template.note1} - {template.note2} -"
        }
    )
   
@login_required(login_url='/')    
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

@login_required(login_url='/')
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
    # send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
    
    send_mail(to_email=email, content=message, subject=subject)
    
    return redirect('account:studenttable')
    # return render(request, {'email':email})

@login_required(login_url='/')
def preview(request, id):
    
    try:
        template = Template.objects.filter(student=request.user, id=id)[0]
        images = template.request_image.all()
        
        # for item in images:
        #     print(item.image_url)
         
        # print(template.id)
       
        return render(request, 'request/preview.html', context={
            "template": template,
        })
    except Template.DoesNotExist:
        raise Http404("Vous ne pouvez pas accerdez a cette requette")
    
# Detail d'une requete  
@login_required(login_url='/')  
def detail_request(request, id):
    template = get_object_or_404(Template, pk = id)
    
    return render(request, "request/preview.html", {
        'template': template,
    })
    
# Delete request 
@login_required(login_url='/')
def delete_template(request, template_id):
    template = Template.objects.get(pk=template_id)
    template.delete()
    messages.info(request, 'Template successfully delete')
    return redirect('index')

@login_required(login_url='/')
def edit(request, id = None):
    currentdate = datetime.date.today()
    teacher = User.objects.filter(is_teacher=True)
    try:
        template = Template.objects.get(student=request.user, pk=id, status="loading")
        # print(template.id)
       
        return render(request, 'edit_template/edit.html', context={
            "student": request.user,
            'current_date':currentdate,
            'teacher':teacher,
            "template": template,
        })
    except Template.DoesNotExist:
        raise Http404("Vous ne pouvez pas accerdez a cette requette")

@login_required(login_url='/')
def follow(request, id):
    try:
        teachers = User.objects.filter(is_teacher=True)
        templates = Template.objects.filter(id = id)[0]
        list_history = RequestHistory.objects.filter(request=templates)
        print(templates.request_image.all())

        return render(request, 'request/follow.html', context={
            "histories": list_history,
            "user": request.user,
            "template": templates,
            "history": list_history.last(),
            'teachers':teachers
        })
    except Template.DoesNotExist:
        raise Http404("Vous ne pouvez pas accerdez a cette requette")
    
@login_required(login_url='/')
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
    
@login_required(login_url='/')
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
            # send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            send_mail(to_email=email, content=message, subject=subject)
            
        else:
            
            request_history.is_student = True
            
            subject = f"Reponse de {user.first_name} {user.last_name} pour la requete {template.objet} "
            message = f"L'etudiant {user.first_name} {user.last_name} a repondu a votre requete "
        
            email = user.email
            # send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            send_mail(to_email=email, content=message, subject=subject)
            
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
   
@login_required(login_url='/')
@csrf_exempt
def end_request(request, id):
    try:    
        
        user = request.user
        
        # request_history = RequestHistory.objects.get(id=req_id)
        template = Template.objects.get(id=id)
        
        if user.is_teacher:
            subject = f"Fin de la requete"
            message = f"Le responsable {user.first_name} {user.last_name} a mis fin a votre requete "
            template.state = True
            template.save()
        
            email = user.email
            # send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            send_mail(to_email=email, content=message, subject=subject)
        

        # return redirect('follow', kwargs={'id': template_id})
        return JsonResponse(
            {
                "id":f"{id}",
            }
        )
    except Exception as excp:
        print(excp)
        raise Http404("Vous ne pouvez pas accerdez a cette requette")
    
 

@login_required(login_url='/')
@csrf_exempt
def transfert_request(request):
    try:
        
        template_id = request.POST.get("template")
        to_teach_id = request.POST.get("to_teacher")
        reason = request.POST.get("reason")
        user = request.user
        
        template = Template.objects.get(id=template_id)
        to_teacher = User.objects.get(id = to_teach_id)
        
        
        request_history = RequestHistory.objects.create(
            request = template,
            responsable = to_teacher,
            reason=reason,
        )
        
        subject = "Requete transferer"
        message = f"M.{user.first_name} {user.last_name} Vous a transferez une requete de l'etudiant {template.student.last_name} {template.student.first_name} en {template.student.filiere}-{template.student.niveau}. Concernant un probleme de {template.objet}"
    
        email = to_teacher.email
        send_mail(to_email=email, content=message, subject=subject)
        
        # send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        # return redirect('account:teacher')

        return JsonResponse(
            {
                "id":f"{request_history.id}",
            }
        )
    except Template.DoesNotExist:
        raise Http404("Vous ne pouvez pas accerdez a cette requette")


def file_upload(request):
    if request.method == 'POST':
        my_file=request.FILES.get('file[]')
        request_id=int(request.GET.get('request'))
        request = Template.objects.get(pk=request_id)
        

        print(f" ==========>{my_file}")
        image = RequestImage.objects.create(image=my_file, request=request)
        return JsonResponse(
            {
                "id":f"{image.image}",
            }
        )
    return JsonResponse({'post':'fasle'})