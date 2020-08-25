
import random
import string
from django.utils.text import slugify


def randomSlugGenerator(size=10):
    chars=string.ascii_lowercase+string.digits+string.ascii_uppercase
    return ''.join([random.choice(chars) for _ in range(size)])


def uniqueSlugGenerator(instance):
    generated_slug=randomSlugGenerator()
    klass=instance.__class__
    if klass == 'Product':
        generated_slug=slugify(instance.title[:10])+'-'+generated_slug
    elif klass=='Category':
        generated_slug=slugify(instance.name[:10])+'-'+generated_slug
    qs=klass.objects.filter(slug=generated_slug)    
    if qs.exists():
        uniqueSlugGenerator(instance)
    else:
        return generated_slug
    