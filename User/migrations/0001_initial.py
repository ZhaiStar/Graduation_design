# Generated by Django 3.0.2 on 2020-04-20 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('name', models.TextField()),
                ('price', models.FloatField()),
                ('color', models.CharField(max_length=16)),
                ('size', models.CharField(max_length=16)),
                ('number', models.IntegerField()),
                ('picture', models.TextField()),
                ('total', models.FloatField()),
                ('cloth_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=32)),
                ('name', models.CharField(default='123', max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=32)),
                ('address', models.TextField(blank=True, null=True)),
                ('identity', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver', models.CharField(max_length=64)),
                ('address', models.TextField(blank=True, null=True)),
                ('post_number', models.CharField(blank=True, max_length=32, null=True)),
                ('phone', models.CharField(max_length=32)),
                ('state', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.User')),
            ],
        ),
        migrations.CreateModel(
            name='PayOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=32)),
                ('order_time', models.DateTimeField(auto_now=True)),
                ('order_total', models.FloatField(default=0)),
                ('order_state', models.IntegerField(default=0)),
                ('order_address', models.TextField()),
                ('order_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.User')),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_name', models.TextField()),
                ('goods_number', models.IntegerField()),
                ('goods_price', models.FloatField()),
                ('goods_total', models.FloatField(default=0)),
                ('goods_picture', models.TextField()),
                ('goods_color', models.CharField(max_length=32)),
                ('goods_size', models.CharField(max_length=32)),
                ('cart_id', models.IntegerField(blank=True, null=True)),
                ('cloth_id', models.IntegerField(blank=True, null=True)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.PayOrder')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_id', models.IntegerField()),
                ('goods_name', models.TextField()),
                ('goods_price', models.CharField(max_length=16)),
                ('goods_picture', models.TextField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.User')),
            ],
        ),
    ]
