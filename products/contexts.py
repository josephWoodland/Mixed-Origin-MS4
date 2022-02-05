from .models import Tag, Product
from django.db.models import Q


def tag_products(request):
    products = Product.objects.all()
    tags_obj = Tag.objects.values("name")

    tags = []
    tag_list = []

    for tag in tags_obj:
        tag = str(list(tag.values()))
        tag = tag[2:-2]
        tags.append(tag)

    for tag in tags:
        tag_name = Tag.objects.filter(name__icontains=tag)
        products = Product.objects.distinct().filter(Q(tags__in=tag_name))

        if len(products) > 0:
            tag_list.append(products[0])

    tag_products = list(zip(tags, tag_list))

    context = {
        "tag_products": tag_products,
    }

    return context
