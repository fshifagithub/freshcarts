# Generated by Django 5.1.6 on 2025-02-23 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecart', '0004_ecart_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='update_on',
            new_name='updated_on',
        ),
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
