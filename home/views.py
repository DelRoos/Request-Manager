from django.shortcuts import render
from .models import Testimonials

# Create your views here.
def home(request):
    testimonials = Testimonials.objects.all()
    return render(request, "index.html", {"datas": testimonials})