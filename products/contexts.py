from .models import Tag


def tag_list(request):

    tags_obj = Tag.objects.values("name")

    tags = []

    for tag in tags_obj:
        tag = str(list(tag.values()))
        tag = tag[2:-2]
        tags.append(tag)

    context = {
        "tags": tags,
    }

    return context
