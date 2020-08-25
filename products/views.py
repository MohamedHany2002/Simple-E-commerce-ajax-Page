from django.shortcuts import render,get_object_or_404,reverse
from .models import Product,Category
from .decorators import ajax_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers



def home(request,category_slug=None):
    products = Product.objects.all()
    # using select related to get Product and Category objects in one query (ORM optimization)
    parent_categories_ids = Category.objects.exclude(parent_category__isnull=True).select_related('parent_category').values_list('parent_category',flat=True)
    parent_categories = Category.objects.filter(id__in=parent_categories_ids)
    sub_categories=None
    if category_slug :
        category = get_object_or_404(Category,slug=category_slug)
        sub_categories = category.child_categories.all()
        products = products.filter(category__in=sub_categories)
    return render(request,"home.html",{'parent_categories':parent_categories,'products':products,'sub_categories':sub_categories})

@ajax_required
@require_POST
@csrf_exempt
def ajax_category_view(request):
    category_slug=request.POST['slug']
    category = get_object_or_404(Category,slug=category_slug)
    # select related to get Product and Category objects in one query 
    products = Product.objects.filter(category=category).select_related('category')
    qs_json = serializers.serialize('json', list(products))
    categories_ids = products.values_list('category')
    categories_qs = Category.objects.filter(id__in=categories_ids)
    categories = serializers.serialize('json',list(categories_qs))
    return JsonResponse({'products':qs_json,'categories':categories})



def product_detail(request,slug):
    product = get_object_or_404(Product,slug=slug)
    return render(request,'product_detail.html',{'product':product})
    
