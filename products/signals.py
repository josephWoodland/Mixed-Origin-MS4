from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save
from django.utils.text import slugify
from .models import Product


def create_product_slug(sender, instance, created, **kwargs):
    """Singal that creates a slug by using the slugify method
    on tha name and adding it to 8 chars form the UUID

    Args:
        instance (Class): Uses the creation of a Product instance to trigger the signal
    """
    product = get_object_or_404(Product, id=instance.id)
    slug = product.slug

    if created:
        if slug is None or len(slug) < 5:
            id = product.id.hex
            id_splice = id[0:8]
            name = slugify(product.name)
            slug_str = f"{id_splice}-{name}"

            Product.objects.filter(id=instance.id).update(slug=slug_str)


post_save.connect(create_product_slug, sender=Product)
