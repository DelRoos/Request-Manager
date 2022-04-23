from django.contrib import admin
from django.urls import path
from import_export.admin import ImportExportModelAdmin
from django import forms
from django.shortcuts import render
from .models import User
from .resources import UserResource
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password



class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class UserAdmin(admin.ModelAdmin):
    # list_display = ('password','username', 'first_name', 'last_name' ,'email','is_student')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)
            
            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data:
                print('sdc')
                print(x)
                print('xvcbjkjhjjj')
                fields = x.split(";")
                print(fields)

                if fields[0] == "":
                    break
                
                hashed_pwd = make_password(fields[0])
                # check_password(fields[0],hashed_pwd) 
                 
                created = User.objects.update_or_create(
                    password = hashed_pwd,
                    username = fields[1],
                    first_name = fields[2],
                    last_name = fields[3],
                    email = fields[-1],
                    )
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)



# @admin.register(User)
# class UserAdmin(ImportExportModelAdmin):
#     list_display = ('password','username', 'first_name', 'last_name' ,'email','is_student')
#     resource_class = UserResource



# admin.site.register(customer, CustomerAdmin)
admin.site.register(User, UserAdmin)