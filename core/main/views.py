from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Avg
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from .filters import ProductListFilter
from .forms import ProductCreateForm, ProductChangeForm
from .models import Product, Rating, RatingAnswer, PaymentMethod, PaymentRequest, Category, Payment

MyUser = get_user_model()

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

    if product.user != request.user:
        return redirect('item', product_id=product.id)

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


def user_profile_view(request, user_id):
    user = get_object_or_404(MyUser, id=user_id)
    payment_requests = PaymentRequest.objects.filter(product__user=user, status='in_processing').order_by('-id')[:3]

    return render(request,
                  'main/user_profile.html',
                  {
                    'user': user, 'payment_requests': payment_requests})


def product_payment_create(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    seller_payment_methods = PaymentMethod.objects.filter(user=product.user)

    quantity = request.GET.get('quantity', 0)
    try:
        quantity = int(quantity)
    except ValueError:
        quantity = 0

    total_price = product.price * Decimal(quantity)

    if request.method == 'POST':
        check = request.FILES.get('check', '')

        order = PaymentRequest(
            user=request.user,
            product=product,
            total_price=total_price,
            quantity=quantity,
            check_image=check
        )
        order.save()

        return redirect('item', product.id)

    return render(
        request,
        'main/product_payment.html',
        {
            'product': product,
            'seller_payment_methods': seller_payment_methods,
            'quantity': quantity,
            'total_price': total_price
        }
    )

def otp_enable_view(request):
    if request.method == "POST":
        if request.POST.get("is_otp_enabled") == "on":
            is_enabled = True
        else:
            is_enabled = False
        request.user.is_otp_enabled = is_enabled
        request.user.save()
        return redirect("user_profile")

    return redirect("user_profile")

def product_list_view(request):
    queryset = Product.objects.filter(is_active=True)

    if 'product_search' in request.GET:
        products_search = request.GET['product_search']
        queryset = queryset.filter(title__icontains=products_search)

    products = ProductListFilter(request.GET, queryset=queryset)
    paginator = Paginator(products.qs, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/product_list.html', {'page_obj': page_obj})

def payment_requests_list_view(request):
    payment_requests = PaymentRequest.objects.filter(product__user=request.user).order_by('-id')

    return render(request, 'main/payment_requests.html', {'payment_requests': payment_requests})

def payment_request_change_view(request, payment_request_id):
    payment_request = get_object_or_404(PaymentRequest, id=payment_request_id)

    if request.method == 'POST':
        payment_request.status = request.POST.get('status', 'in_processing')
        payment_request.save()

        if payment_request.status == 'accepted':
            payment = Payment(
                user=payment_request.user,
                product=payment_request.product.title,
                total_price=payment_request.total_price,
                check_image=payment_request.check_image,
                quantity=payment_request.quantity
            )

            payment.save()


    return redirect('payment_requests_list')

def accepted_requests_view(request):
    accepted_requests = Payment.objects.all()

    total = 0

    for i in accepted_requests:
        total += i.total_price

    return render(request, 'main/accepted_requests.html', {'accepted_requests': accepted_requests, 'total': total})