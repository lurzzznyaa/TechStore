from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index_view, name='index'),
    path('item/<int:product_id>', views.product_detail_view, name='item')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
