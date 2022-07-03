from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User
from .resources import UserResource
from tablib import Dataset
from request.models import Template, RequestHistory, Comment
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import login_required


@login_required(login_url='/')
def teacher(request):
    templates = Template.objects.filter()
    requests = []
    # print(templates)
    
    
    for template in templates:
        list_history = RequestHistory.objects.filter(request=template).last()
        # print(list_history.responsable.username)
        if list_history is not None:
            if list_history.responsable.id == request.user.id:
                print(list_history.responsable.username)
                requests.append(template)
        
    return render(request, 'teacher.html', {'templates': requests})


@login_required(login_url='/')
def student(request):
    return render(request,'student.html')


@login_required(login_url='/')
def studenttable(request):
    template = Template.objects.filter(student=request.user.id)
    if not template.exists():
        return redirect('account:student')
        
    return render(request,'student-table.html', {'template':template})


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            userSch = User.objects.get(email=email)
            print(userSch)
        except:
            userSch = None

        print(userSch)

        if userSch == None:
            messages.error(request, 'Utilisateur non trouvé !')
            return render(request, 'index.html')
        else:
            username = userSch.username
            user = authenticate(
                request, username=username, password=password)
        if user is not None and user.is_teacher:
            login(request, user)
            return redirect('account:teacher')
        elif user is not None and user.is_student:
            login(request, user)
            if Template.objects.filter(student=user).exists():
                return redirect('account:studenttable')
            else:
                return redirect('account:student')
        else:
            messages.error(request, 'Incorrect Email OR password')

    context = {}
    return render(request, 'index.html', context)


def simple_upload(request):
    if request.method == 'POST':
        user_resource = UserResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())
        result = user_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            user_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'accoiunt/simple_upload.html')