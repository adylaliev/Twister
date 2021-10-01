# Generated by Django 3.2.7 on 2021-10-01 08:49

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('twister', '0002_auto_20211001_1426'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Product',
            new_name='Publication',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='product',
            new_name='publication',
        ),
    ]
