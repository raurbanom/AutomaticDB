from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic


# Create your views here.
def base(request):
    return render(request, 'base.html')


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

# class AboutView(generic.TemplateView):
#     template_name = "about.html"



