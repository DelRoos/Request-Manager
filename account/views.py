from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User
from .resources import UserResource
from tablib import Dataset



# def index(request):
#     return render(request, 'index.html')


def jury(request):
    return render(request,'jury.html')



def teacher(request):
    return render(request,'teacher.html')



def student(request):
    return render(request,'student.html')





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



# def login_view(request):
#     form = LoginForm(request.POST or None)
#     msg = None
#     if request.method == 'POST':
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None and user.is_jury:
#                 login(request, user)
#                 return redirect('jurypage')
#             elif user is not None and user.is_teacher:
#                 login(request, user)
#                 return redirect('teacher')
#             elif user is not None and user.is_student:
#                 login(request, user)
#                 return redirect('student')
#             else:
#                 msg= 'invalid credentials'
#         else:
#             msg = 'error validating form'
#     return render(request, 'login.html', {'form': form, 'msg': msg})

def user_login(request):
    # if request.user.is_authenticated and user.is_jury:
    #     return redirect('jury')
    # elif request.user.is_authenticated and user.is_teacher:
    #     return redirect('teacher')
    # elif request.user.is_authenticated and user.is_student:
    #     return redirect('student')
    # else:
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
            return render(request, 'login.html')
        else:
            username = userSch.username
            user = authenticate(
                request, username=username, password=password)
        if user is not None and user.is_jury:
            login(request, user)
            return redirect('jury')
        elif user is not None and user.is_teacher:
            login(request, user)
            return redirect('teacher')
        elif user is not None and user.is_student:
            login(request, user)
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