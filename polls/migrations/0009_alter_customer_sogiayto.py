# Generated by Django 4.0.3 on 2022-04-26 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_alter_customer_anhxe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='sogiayto',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]