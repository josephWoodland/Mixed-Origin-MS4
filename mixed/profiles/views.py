from re import template
from django.shortcuts import render

# Create your views here.


def userProfile(request):
    template = "profiles/profile.html"
    context ={

    }
    return render(request, template, context)
