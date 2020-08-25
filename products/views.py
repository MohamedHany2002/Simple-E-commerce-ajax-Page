from django.shortcuts import render,get_object_or_404,reverse
from .models import Product,Category
from .decorators import ajax_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q
from django.db.models import Count


def home(request,category_slug=None):
    products = Product.objects.all()
    parent_categories = Category.objects.get_parent_categories()
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
    # recommeding similar products
    tags = product.tags.all()
    products = Product.objects.filter(tags__in=tags)
    similar_products = products.annotate(count=Count('tags')).order_by('-count').exclude(slug=slug)
    return render(request,'product_detail.html',{'product':product,'similar_products':similar_products})
    


def search(request):
    query = request.GET.get('q')
    products=Product.objects.filter(Q(title__icontains=query)|Q(description__icontains=query)|Q(tags__name__icontains=query))
    parent_categories = Category.objects.get_parent_categories()
    return render(request,'home.html',{'products':products,'parent_categories':parent_categories})



