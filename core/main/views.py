from django.db.models import Avg
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaulttags import comment

from .forms import ProductCreateForm, ProductChangeForm
from .models import Product, Rating, RatingAnswer


def index_view(request):
    products = Product.objects.filter(is_active=True)

    return render(request, 'main/index.html', {'products': products})

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_update_form = ProductChangeForm(instance=product)
    similar_products = Product.objects.filter(category=product.category).exclude(id=product_id)
    product_comments = Rating.objects.filter(product=product)

    rating_avg = product_comments.aggregate(Avg('count'))['count__avg']

    return render(request,
                  'main/product_detail.html',
                  {'product': product,
                   'similar_products': similar_products,
                   'product_update_form': product_update_form,
                   'product_comments': product_comments,
                   'rating_avg': rating_avg,
                   })

def product_create_view(request):
    if not request.user.is_authenticated:
        raise Http404()
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            product_object = form.save(commit=False)
            product_object.user = request.user
            product_object.save()

            return redirect('index')

    form = ProductCreateForm()
    return render(request, 'main/product_create.html', {'form': form})

def product_change_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductChangeForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('item', product_id=product.id)


def rating_create_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        count = int(request.POST.get('count', ''))

        rating = Rating(
            user=request.user,
            product=product,
            count=count,
            comment=comment
        )
        rating.save()
        return redirect('item', product_id=rating.product.id)

def rating_answer_view(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id)

    if rating.product.user != request.user:
        return redirect('item', product_id=rating.product.id)

    if request.method == 'POST':
        comment = request.POST.get('comment', '')

        RatingAnswer(
            user=request.user,
            rating=rating,
            comment=comment
        ).save()
        return redirect('item', product_id=rating.product.id)
