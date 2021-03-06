from django.db import models

class Order(models.Model):
    user            = models.ForeignKey('users.User', on_delete=models.CASCADE)
    order_status    = models.ForeignKey('OrderStatus', on_delete=models.PROTECT)
    shipping_cost   = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    order_date_time = models.DateTimeField(auto_now=True)
    total_price     = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    class Meta:
        db_table = 'orders'

class OrderStatus(models.Model):
    status = models.IntegerField()

    class Meta:
        db_table = 'order_status'

class ShippingInformation(models.Model):
    address      = models.CharField(max_length=200)
    message      = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=45)
    order        = models.ForeignKey('Order', on_delete=models.CASCADE)

    class Meta:
        db_table='shipping_informations'

class Cart(models.Model):
    product     = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    order       = models.ForeignKey('Order', on_delete=models.CASCADE)
    quantity    = models.IntegerField()
    option      = models.ForeignKey('products.ProductOption', on_delete=models.CASCADE)

    class Meta:
        db_table='carts'

class PaymentMethod(models.Model):
    name  = models.CharField(max_length=45)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

    class Meta:
        db_table='payment_methods'

class DiscountType(models.Model):
    name  = models.CharField(max_length=45)
    rate  = models.DecimalField(max_digits=10,decimal_places=2)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

    class Meta:
        db_table='discount_types'
