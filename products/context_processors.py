
from .models import Category

def get_side_categories(request):
    parent_categories = Category.objects.get_parent_categories()
    return{'parent_categories':parent_categories}