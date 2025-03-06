from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ProductCreateForm, ProductChangeForm
from .models import Product

def index_view(request):
    products = Product.objects.filter(is_active=True)

    return render(request, 'main/index.html', {'products': products})

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_update_form = ProductChangeForm(instance=product)
    similar_products = Product.objects.filter(category=product.category).exclude(id=product_id)

    return render(request,
                  'main/product_detail.html',
                  {'product': product, 'similar_products': similar_products, 'product_update_form': product_update_form})

def product_create_view(request):
    if not request.user.is_authenticated:
        raise Http404()
    if request.method == 'POST':
        form = ProductCreateForm(request.post, request.FILES)
        if form.is_valid():
            product_object = form.save(commit=False)
            product_object.user = request.user
            product_object.save()

            return redirect('index')

    form = ProductCreateForm()
    return render(request, 'main/product_create.html', {'form': form})

def product_change_view(request):
    ...


