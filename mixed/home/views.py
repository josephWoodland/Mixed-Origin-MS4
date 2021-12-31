from django.shortcuts import render

# Create your views here.


def home(request):
    """
    View to return the home page
    """
    template = "home/home.html"
    context = {}
    return render(request, template, context)
