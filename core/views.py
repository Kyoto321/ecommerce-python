from django.shortcuts import render
from store.models import Product

# Create your views here.
def indexpage(request):
    products = Product.objects.filter(status=Product.ACTIVE)[0:6]
    return render(request, 'core/indexpage.html', {
        'products': products
    })

def about(request):
    return render(request, 'core/about.html')