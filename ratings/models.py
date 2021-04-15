from django.db import models

class Rate(models.Model):
    rate    = models.DecimalField(max_digits=6, decimal_places=2)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    user    = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table='rates'

class Comment(models.Model):
    product    = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='comments'

class CommentImage(models.Model):
    image_url = models.CharField(max_length=2000)
    comment   = models.ForeignKey('Comment', on_delete=models.CASCADE)

    class Meta:
        db_table='comment_images'

