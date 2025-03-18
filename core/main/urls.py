from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index_view, name='index'),
    path('item/<int:product_id>/', views.product_detail_view, name='item'),
    path('product/create/', views.product_create_view, name='product_create'),
    path('product/change/<int:product_id>/', views.product_change_view, name='product_change'),
    path('product/<int:product_id>/payment/create/', views.product_payment_create, name='product_payment_create'),
    path('catalog/', views.product_list_view, name='catalog'),

    path('rating/create/<int:product_id>/', views.rating_create_view, name='rating_create'),
    path('rating-answer/create/<int:rating_id>/', views.rating_answer_view, name='rating_answer_create'),

    path('profile/<int:user_id>/', views.user_profile_view, name='user_profile'),
    path('payment_requests/', views.payment_requests_list_view, name='payment_requests_list'),
    path('accepted_requests/', views.accepted_requests_view, name='accepted_requests'),
    path('payment_request/<int:payment_request_id>/change/', views.payment_request_change_view, name='payment_request_change_status'),
    path('otp_enable/', views.otp_enable_view, name='otp_enable_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
