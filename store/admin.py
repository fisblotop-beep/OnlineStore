from django.contrib import admin

from .models import Item, ItemTag


# =========================
# КАТЕГОРИИ
# =========================

@admin.register(ItemTag)
class ItemTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# =========================
# ТОВАРЫ
# =========================

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price',
        'old_price',
        'is_available',
        'pub_date',
    )

    list_filter = (
        'is_available',
        'tags',
    )

    search_fields = (
        'title',
        'description',
    )

    prepopulated_fields = {
        'slug': ('title',)
    }

    list_editable = (
        'price',
        'old_price',
        'is_available',
    )

    readonly_fields = (
        'pub_date',
    )

    fieldsets = (
        ('Основная информация', {
            'fields': (
                'title',
                'slug',
                'description',
                'image',
            )
        }),
        ('Цены', {
            'fields': (
                'price',
                'old_price',
            )
        }),
        ('Категории', {
            'fields': (
                'tags',
            )
        }),
        ('Дополнительно', {
            'fields': (
                'is_available',
                'pub_date',
            )
        }),
    )
