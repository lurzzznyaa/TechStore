# Generated by Django 5.1.6 on 2025-02-27 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='main_image',
            field=models.ImageField(default=1, upload_to='media/main_covers', verbose_name='Главное фото'),
            preserve_default=False,
        ),
    ]
