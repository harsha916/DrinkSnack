# Generated by Django 4.0.6 on 2022-08-22 10:01

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('DrinkSnackApp', '0003_delete_orderdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('items', models.CharField(max_length=200)),
                ('quantity', models.IntegerField(blank=True, null=True)),
            ],
            managers=[
                ('variable', django.db.models.manager.Manager()),
            ],
        ),
    ]
