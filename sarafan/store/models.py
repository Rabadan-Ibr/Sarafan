from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.validators import MinValueValidator
from django.db import models
from PIL import Image

from sarafan.settings import MIDDLE_THUMBNAIL_SIZE, SMALL_THUMBNAIL_SIZE

User = get_user_model()


class CommonInfo(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=80)
    slug = models.SlugField(verbose_name='Slug-имя', unique=True)
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='store/image/',
    )

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        picture, path = self.image.storage, self.image.path
        super().delete(using, keep_parents)
        picture.delete(path)

    def __str__(self):
        return self.name


class Category(CommonInfo):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategory(CommonInfo):
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name='sub_categories',
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Product(CommonInfo):
    sub_category = models.ForeignKey(
        SubCategory,
        verbose_name='Подкатегория',
        on_delete=models.PROTECT,
        related_name='products',
    )
    middle_thumbnail = models.ImageField(
        verbose_name='Среднее изображение',
        editable=False,
        upload_to='store/image/',
        blank=True,
        null=True,
    )
    small_thumbnail = models.ImageField(
        verbose_name='Маленькое изображение',
        editable=False,
        upload_to='store/image/',
        blank=True,
        null=True,
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=9,
        decimal_places=2,
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def delete(self, using=None, keep_parents=False):
        middle, path_m = (
            self.middle_thumbnail.storage, self.middle_thumbnail.path
        )
        small, path_s = self.small_thumbnail.storage, self.small_thumbnail.path
        super().delete(using, keep_parents)
        middle.delete(path_m)
        small.delete(path_s)

    def create_thumbnail(self):
        im = Image.open(self.image)
        im.convert('RGB')
        im.thumbnail(MIDDLE_THUMBNAIL_SIZE)
        thumb_io = BytesIO()
        im.save(thumb_io, 'JPEG', quality=85)
        self.middle_thumbnail = File(
            thumb_io,
            name=self.image.name[:len(self.image.name)-4] + '_m.jpg',
        )
        im.thumbnail(SMALL_THUMBNAIL_SIZE)
        thumb_io = BytesIO()
        im.save(thumb_io, 'JPEG', quality=85)
        self.small_thumbnail = File(
            thumb_io,
            name=self.image.name[:len(self.image.name)-4] + '_s.jpg',
        )

    def save(self, *args, **kwargs):
        self.create_thumbnail()
        super().save(*args, **kwargs)


class ProductCart(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name='Продукт',
        on_delete=models.CASCADE,
        related_name='m2m_cart',
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='m2m_product'
    )
    amount = models.SmallIntegerField(
        verbose_name='Количество',
        validators=(MinValueValidator(limit_value=1),),
        default=1,
    )

    class Meta:
        verbose_name = 'Корзина'
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'user'],
                name='unique_user_product',
            ),
        ]

    def get_cost(self):
        return self.product.price * self.amount
