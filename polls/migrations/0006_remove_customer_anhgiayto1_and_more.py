# Generated by Django 4.0.3 on 2022-04-26 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_alter_cam_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='anhgiayto1',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='anhgiayto2',
        ),
        migrations.AlterField(
            model_name='customer',
            name='anhbien',
            field=models.ImageField(blank=True, upload_to='static/image'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='anhxe',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
