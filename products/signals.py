from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save
from django.utils.text import slugify
from PIL import Image
import PIL
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
        if slug is None:
            id = product.id.hex
            id_splice = id[0:8]
            name = slugify(product.name)
            slug_str = f"{id_splice}-{name}"

            Product.objects.filter(id=instance.id).update(slug=slug_str)


def update_image(sender, instance, created, **kwargs):
    """Singal that takes the saved product image, changes the
    size and file type.
    Args:
        instance (Class): Uses the creation of a Product instance to trigger the signal
    """
    product = get_object_or_404(Product, id=instance.id)
    img = product.image.path
    print("This is the uploaded image", img)
    image = Image.open(img)
    image.convert("RGB")
    image_name = img.split(".")[0]
    print(image_name)
    # image_name = image_split[0]
    print("This is the image name: ", image_name)
    img = image.save(f'{image_name}.webp', "webp")
    webp_image = img
    print("New image: ", img)

    Product.objects.filter(id=instance.id).update(image=webp_image)


post_save.connect(update_image, sender=Product)
