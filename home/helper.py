from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from io import BytesIO
from django.core.files import File
from PIL import Image


def paginateProdcuts(request, products, results):
    """
    This function is for page pagination, can be accessed throughout the app
    """
    page = request.GET.get("page")
    paginator = Paginator(products, results)

    try:
        products = paginator.page(page)

    except PageNotAnInteger:
        page = 1
        products = paginator.page(page)

    except EmptyPage:
        page = paginator.num_pages
        products = paginator.page(page)

    leftIndex = int(page) - 4
    rightIndex = int(page) + 5

    if leftIndex < 1:
        leftIndex = 1

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, products, paginator


# def make_webp(image):
#     """Converts image to webp"""

#     im = Image.open(image)

#     im.convert('RGB')  # convert mode

#     name = str(im) + ".webp"  # create a BytesIO object

#     name = BytesIO()

#     im.save(name, 'webp')  # save image to BytesIO object

#     # create a django friendly File object
#     webp_image = File(im, name=name)

#     return webp_image
