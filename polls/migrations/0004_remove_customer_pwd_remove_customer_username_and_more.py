# Generated by Django 4.0.3 on 2022-04-25 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_alter_customer_anhbien_alter_customer_anhgiayto1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='pwd',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='username',
        ),
        migrations.RemoveField(
            model_name='parking',
            name='img',
        ),
        migrations.AlterField(
            model_name='cam',
            name='imgtime',
            field=models.DateTimeField(),
        ),
    ]
