# Generated by Django 2.1 on 2019-08-25 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_book_cover'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.RemoveField(
            model_name='book',
            name='title',
        ),
    ]
