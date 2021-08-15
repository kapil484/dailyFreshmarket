from django.db import models

# Create your models here.
class CartInfo(models.Model):
    user=models.ForeignKey('user.UserInfo', null=True, on_delete =models.CASCADE)
    goods=models.ForeignKey('goods.GoodsInfo', null=True, on_delete =models.CASCADE)
    count=models.IntegerField(default=0)
