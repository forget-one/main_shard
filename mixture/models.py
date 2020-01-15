from django.db import models
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

def gen_slug(s, e):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '_' + str(e)


class Hashtag(models.Model):
    title           = models.CharField(verbose_name='Назва', max_length=50)
    slug            = models.SlugField(verbose_name='URL',blank=True, null=True, unique=True)

    
    def __str__(self):
        return f'{self.title}'
    
    def save(self, *args, **kwargs):
        if self.slug == None or self.slug.replace(' ', '') == '':
            self.slug = gen_slug(self.title, Hashtag.objects.all().last().id)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name        = '#Хештеги'
        verbose_name_plural = '#Хештеги'

class Category(models.Model):
    title           = models.CharField(verbose_name='Назва',max_length=50)
    slug            = models.SlugField(verbose_name='URL',blank=True, null=True, unique=True)


    def save(self, *args, **kwargs):
        if self.slug == None or self.slug.replace(' ', '') == '':
            self.slug = gen_slug(self.title, Category.objects.all().last().id)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("category", kwargs={"slug": self.slug})

    class Meta:
        verbose_name        = 'Категорія'
        verbose_name_plural = 'Категорії'
    
    

class Product(models.Model):
    title           = models.CharField(verbose_name='Назва',max_length=50)
    slug            = models.SlugField(verbose_name='URL',blank=True, unique=True)
    image           = models.ImageField(verbose_name='Зображення',upload_to='images/', blank=True, null=True, default=None)
    description     = models.TextField(verbose_name='Опис',)
    price           = models.FloatField(verbose_name='Ціна',)
    discount_price  = models.FloatField(verbose_name='Ціна з урахуванням знижки',blank=True, null=True)
    category        = models.ForeignKey(Category, verbose_name='Категорія', related_name='category', on_delete=models.CASCADE)
    hashtag         = models.ManyToManyField(Hashtag, verbose_name='#Хештеги')
    created         = models.DateTimeField(verbose_name='Створено', auto_now=True, blank=True)


    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if self.slug == None or self.slug.replace(' ', '') == '':
            self.slug = gen_slug(self.title, Hashtag.objects.all().last().id)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug}) 

    class Meta:
        verbose_name        = 'Продукт'
        verbose_name_plural = 'Продукти'
        ordering            = ['-created']

    
class Cart(models.Model):
    ordered         = models.BooleanField(verbose_name='Замовлено?',default=False)
    ordered_date    = models.DateTimeField(verbose_name='Дата замовлення',auto_now_add=True, blank=True, null=True)


    def __str__(self):
        return f'{self.id}'
    
    class Meta:
        verbose_name        = 'Кошик'
        verbose_name_plural = 'Кошики користувачів'


class CartItem(models.Model):
    cart            = models.ForeignKey(Cart, verbose_name='Кошик №', related_name='cart', null=True, on_delete=models.CASCADE)
    product         = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE, default=None)
    ordered         = models.BooleanField(verbose_name='Статус',default=False)
    count           = models.PositiveIntegerField(verbose_name='Кількість',default=1)


    def __str__(self):
        return f'{self.product.title} {self.count} {self.cart}'

    def get_total_item_price(self):
        return self.count * self.product.price

    def get_total_item_discount_price(self):
        return self.count * self.product.discount_price

    def get_total_clear_price(self):
        if self.product.discount_price:
            return self.get_total_item_discount_price()
        else:
            return self.get_total_item_price()

    def get_money_saved(self):
        return self.get_total_item_price() - self.get_total_item_discount_price()

    class Meta:
        verbose_name        = 'Продукт в заказі'
        verbose_name_plural = 'Продукти в заказі'

