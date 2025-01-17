# Generated by Django 5.0.6 on 2024-07-01 12:10

import coffeapp.models
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admins',
            fields=[
                ('username', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ('-username',),
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('order_id', models.IntegerField(db_index=True, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('username', models.CharField(db_index=True, max_length=255)),
                ('products', models.CharField(max_length=255)),
                ('purchase_amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('type', models.BinaryField(db_index=True, max_length=1)),
            ],
            options={
                'ordering': ('-order_id',),
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.IntegerField(db_column='id', db_index=True, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('name', models.CharField(db_index=True, max_length=255, unique=True)),
                ('sugar', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('coffee', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('flour', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('chocolate', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('vertical', models.BinaryField(db_index=True, max_length=10)),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.IntegerField(db_column='id', primary_key=True, serialize=False, unique=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('name', models.CharField(max_length=255, unique=True)),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('username', models.CharField(db_index=True, max_length=255, primary_key=True, serialize=False, unique=True)),
                ('full_name', models.CharField(db_index=True, max_length=255)),
                ('email', models.EmailField(db_index=True, max_length=255, unique=True)),
                ('password', models.CharField(max_length=255, unique=True)),
                ('phone_number', models.BigIntegerField(db_index=True, unique=True, validators=[django.core.validators.MinValueValidator(10000000000), django.core.validators.MaxValueValidator(99999999999), coffeapp.models.validate_phone_number])),
            ],
            options={
                'ordering': ('-username',),
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Orders_Products',
            fields=[
                ('id', models.IntegerField(db_column='id', db_index=True, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('orders_order_id', models.ForeignKey(db_column='order_id', on_delete=django.db.models.deletion.CASCADE, to='coffeapp.orders')),
                ('products_id', models.ForeignKey(db_column='products_id', on_delete=django.db.models.deletion.CASCADE, to='coffeapp.products')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Users_Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orders_order_id', models.ForeignKey(db_column='order_id', on_delete=django.db.models.deletion.CASCADE, to='coffeapp.orders')),
                ('users_username', models.ForeignKey(db_column='username', on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='coffeapp.users')),
            ],
            options={
                'ordering': ('-users_username',),
            },
        ),
    ]
