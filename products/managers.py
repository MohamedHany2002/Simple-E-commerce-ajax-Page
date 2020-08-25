# from products.models import Category
from django.db import models

class CategoryManager(models.Manager):
    def get_parent_categories(self):
        # using select related to get Product and Category objects in one query (ORM optimization)

        parent_categories_ids = self.model.objects.exclude(parent_category__isnull=True).select_related('parent_category').values_list('parent_category',flat=True)
        parent_categories = self.model.objects.filter(id__in=parent_categories_ids)
        return parent_categories
