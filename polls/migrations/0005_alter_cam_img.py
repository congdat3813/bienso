# Generated by Django 4.0.3 on 2022-04-25 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_remove_customer_pwd_remove_customer_username_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cam',
            name='img',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]