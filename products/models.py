from django.db import models
from django.urls import reverse 
from .utils import uniqueSlugGenerator
from django.db.models.signals import pre_save,post_save
from .managers import CategoryManager




class Product(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    category = models.ForeignKey('Category' , on_delete=models.CASCADE,related_name='products')
    slug = models.SlugField(blank=True)
    image = models.ImageField(upload_to='images/',blank=True)
    price = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)



    class Meta:
        ordering = ('-created',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})



class Category(models.Model):
    name  = models.CharField(db_index=True,max_length=100)
    slug = models.SlugField(blank=True)
    parent_category = models.ForeignKey('self',null=True,blank=True ,related_name='child_categories', on_delete=models.CASCADE)
    objects = CategoryManager()

    class Meta:
        ordering=('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})

def save_slug(sender,**kwargs):
    if not kwargs['instance'].slug:
        kwargs['instance'].slug=uniqueSlugGenerator(kwargs['instance'])
        kwargs['instance'].save()
post_save.connect(save_slug,sender=Product)
post_save.connect(save_slug,sender=Category)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    product = models.ManyToManyField(Product,related_name='tags')

    def __str__(self):
        return self.name