from django.db import models

class User(models.Model):
    password     = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=45, unique=True)
    email        = models.EmailField(max_length=300, unique=True)
    name         = models.CharField(max_length=45)
    nickname     = models.CharField(max_length=45, blank=True)
    create_at    = models.DateTimeField(auto_now_add=True)
    update_at    = models.DateTimeField(auto_now=True)
    badge        = models.ManyToManyField('Badge', through='UserBadge')

    class Meta:
        db_table = 'users'

class UserGrade(models.Model):
    grade = models.IntegerField()
    user  = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_grades'

class Wishlist(models.Model):
    is_like = models.BooleanField()
    user    = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'wishlists'

class Badge(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'badges'

class UserBadge(models.Model):
    user  = models.ForeignKey('User', on_delete=models.CASCADE)
    badge = models.ForeignKey('Badge', on_delete=models.CASCADE)

    class Meta:
        db_table = 'users_badges'

class PaymentHistory(models.Model):
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE)

    class Meta:
        db_table = 'payment_histories'