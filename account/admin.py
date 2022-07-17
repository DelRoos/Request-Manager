from django.contrib import admin
from django.urls import path
from import_export.admin import ImportExportModelAdmin
from django import forms
from django.shortcuts import render

from utils.functions import send_mail
from .models import User
from .resources import UserResource
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password

from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import Group
import shortuuid


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class UserAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'is_student', 'is_teacher')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'Fichier invalide')
                return HttpResponseRedirect(request.path_info)
            
            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data:
                print('sdc')
                print(x)
                fields = x.split(";")
                print(fields)

                pass_word = fields[0]
                if pass_word == "":
                    pass_word = shortuuid.ShortUUID().random(length=8)
                
                hashed_pwd = make_password(pass_word)
                # check_password(fields[0],hashed_pwd)
                try:
                    created = User.objects.update_or_create(
                        password = hashed_pwd,
                        username = fields[1],
                        first_name = fields[2],
                        last_name = fields[3],
                        phone = fields[4],
                        matricule = fields[5],
                        filiere = fields[6],
                        niveau = fields[7],
                        email = fields[8],
                        is_student = f"{fields[-1]}".replace("\r", "") == "stud",
                        is_teacher = f"{fields[-1]}".replace("\r", "") == "eng",
                        )

                    print(f"{fields[-1]}")

                    html_template = 'register_email.html'
                    html_message = render_to_string(html_template, {"username": fields[1], "password": pass_word})
                    subject = 'Welcome to Request-Manager'
                    # email_from = settings.EMAIL_HOST_USER
                    email = [f"{fields[8]}".replace("\r", "")]
                    print(f"{email} =====> {html_message} =====> {subject}")
                    send_mail(to_email=email, content=str(html_message), subject=subject)
                except:
                    print("Erreur lors de la creation du compte")
                 


            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)


# admin.site.register(customer, CustomerAdmin)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
