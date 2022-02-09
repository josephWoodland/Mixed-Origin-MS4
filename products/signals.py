from itertools import product
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save
from django.utils.text import slugify
from .models import Product


def create_product_slug(sender, instance, created, **kwargs):
    product = get_object_or_404(Product, id=instance.id)
    slug = product.slug

    if created:
        if slug is None:
            id = product.id.hex
            id_splice = id[0:8]
            name = slugify(product.name)
            slug_str = f'{id_splice}-{name}'

            Product.objects.filter(id=instance.id).update(slug=slug_str)


post_save.connect(create_product_slug, sender=Product)
