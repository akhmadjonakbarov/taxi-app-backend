# Generated by Django 4.1.5 on 2023-01-20 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=12)),
                ('from_where', models.CharField(max_length=250)),
                ('to_where', models.CharField(max_length=250)),
                ('leaving_time', models.DateTimeField()),
                ('service_price', models.FloatField()),
                ('car_type', models.CharField(max_length=250)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]