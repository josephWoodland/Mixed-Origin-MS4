from django.shortcuts import render

# Create your views here.


def partners(request):
    template = "partners/partners.html"
    context = {}
    return render(request, template, context)
