from django.shortcuts import get_object_or_404, render

from .models import Item, ItemTag
from .paginator import paginator


def store(request):
    """
    Главная страница магазина
    """
    items = Item.objects.filter(is_available=True)

    context = {
        'page_obj': paginator(request, items, 9),
        'range': [*range(1, 7)],
    }
    return render(request, 'store/main_page.html', context)


def item_details(request, item_slug):
    """
    Страница товара
    """
    item = get_object_or_404(Item, slug=item_slug)
    return render(request, 'store/item_details.html', {'item': item})


def tag_details(request, slug):
    """
    Товары по категории
    """
    tag = get_object_or_404(ItemTag, slug=slug)
    items = Item.objects.filter(tags__in=[tag])

    context = {
        'tag': tag,
        'page_obj': paginator(request, items, 3),
    }
    return render(request, 'store/tag_details.html', context)


def tag_list(request):
    """
    Список категорий
    """
    tags = ItemTag.objects.all()
    context = {
        'page_obj': paginator(request, tags, 6),
    }
    return render(request, 'store/tag_list.html', context)
