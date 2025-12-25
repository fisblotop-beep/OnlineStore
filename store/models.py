from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase


# =========================
# КАТЕГОРИЯ (ТЕГ)
# =========================

class ItemTag(TagBase):
    image = models.ImageField(
        upload_to='categories/',
        verbose_name='Изображение',
        blank=True
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
    )

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.name


# =========================
# ПРОМЕЖУТОЧНАЯ МОДЕЛЬ TAGGIT
# =========================

class TaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(
        ItemTag,
        on_delete=models.CASCADE,
        related_name='tagged_items',  # ← ВАЖНО: уникальное имя
        verbose_name='Категория',
    )


# =========================
# ТОВАР
# =========================

class Item(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='URL'
    )

    description = models.TextField(
        verbose_name='Описание'
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Цена'
    )

    old_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Старая цена',
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to='items/',
        verbose_name='Изображение',
        blank=True
    )

    is_available = models.BooleanField(
        default=True,
        verbose_name='В наличии'
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    tags = TaggableManager(
        through=TaggedItem,
        verbose_name='Категории',
        blank=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('store:item_detail', args=[self.slug])
