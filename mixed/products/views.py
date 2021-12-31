from django.shortcuts import render

# Create your views here.
def addProduct(request):
    template = "/product/add_product.html"
    context = {}
    return render(request, template, context)
