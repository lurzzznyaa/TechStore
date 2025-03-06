from django import forms
from .models import Product, Rating, RatingAnswer


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'title',
            'category',
            'main_image',
            'images',
            'description',
            'price',
        )

class ProductChangeForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'title',
            'category',
            'main_image',
            'images',
            'description',
            'price',
        )