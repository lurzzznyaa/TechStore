from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index_view, name='index'),
    path('item/<int:product_id>', views.product_detail_view, name='item'),
    path('product/create', views.product_create_view, name='product_create'),
    path('product/change/<int:product_id>', views.product_change_view, name='product_change'),
    path('rating/create/<int:product_id>', views.rating_create_view, name='rating_create'),
    path('rating-answer/create/<int:rating_id>', views.rating_answer_view, name='rating_answer_create'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
