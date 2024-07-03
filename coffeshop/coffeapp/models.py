from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    if len(str(value)) == 10:
        raise ValidationError('Phone number must be exactly 10 digits')

class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True, primary_key=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    phone_number = models.IntegerField(
        unique=True, null= True,
        validators=[validate_phone_number],db_index=True)
    USERNAME_FIELD= 'username'
    REQUIRED_FIELDS= []





class Users(models.Model):
    username = models.CharField(max_length=255, unique=True, primary_key=True, db_index=True)
    full_name = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    password = models.CharField(max_length=255, unique=True, db_index=False)
    phone_number = models.BigIntegerField(
        unique=True,
        validators=[
            MinValueValidator(10000000000),
            MaxValueValidator(99999999999),
            validate_phone_number],db_index=True)
    

    class Meta:
        ordering = ('-username',)

class Orders(models.Model):
    order_id = models.IntegerField(db_index=True, validators=[MinValueValidator(1), MaxValueValidator(10)], unique=True, primary_key=True)
    username = models.CharField(max_length=255, db_index=True)
    products = models.CharField(max_length=255)
    purchase_amount = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    type = models.BinaryField(max_length=1, db_index=True)

    class Meta:
        ordering = ('-order_id',)

class Users_Orders(models.Model):
    users_username = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username', related_name='orders', db_column='username')
    orders_order_id = models.ForeignKey(Orders, on_delete=models.CASCADE, to_field='order_id', db_column='order_id')

    class Meta:
        ordering = ('-users_username',)

class Products(models.Model):
    PRODUCT_TYPES = [
        ('CD', 'Cold Drinks'),
        ('CA', 'Cakes'),
        ('MS', 'Milkshakes'),
        ('HD', 'Hot Drinks'),
    ]


    avatar = models.ImageField(null= True, default="coffee_shop_logo_whithout_background_1.png")
    id = models.IntegerField(primary_key=True, db_index=True, db_column='id',  unique=True)
    name = models.CharField(max_length=255, db_index=True, unique=True)
    sugar = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    coffee = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],default=0)
    flour = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],default=0)
    chocolate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],default=0)
    vertical = models.CharField(max_length=2, choices=PRODUCT_TYPES, db_index=True)
    price = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True )

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return self.name

class Orders_Products(models.Model):
    id = models.IntegerField(primary_key=True, db_index=True, db_column='id', validators=[MinValueValidator(1), MaxValueValidator(10)], unique=True)
    orders_order_id = models.ForeignKey(Orders, on_delete=models.CASCADE, to_field='order_id', db_column='order_id')
    products_id = models.ForeignKey(Products, on_delete=models.CASCADE, to_field='id', db_column='products_id')

    class Meta:
        ordering = ('-id',)

class Admins(models.Model):
    username = models.CharField(max_length=255, unique=True, primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('-username',)

class Storage(models.Model):
    NAME_CHOICES= [('sugar','sugar'), ('coffee','coffee'), ('flour','flour'), ('chocolate','chocolate')]
    name = models.CharField(choices=NAME_CHOICES, max_length=255, unique=True, primary_key=True)
    amount = models.IntegerField()