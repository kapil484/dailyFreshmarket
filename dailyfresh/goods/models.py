from django.db import models

# Create your models here.
#  coding: utf-8
#from tinymce.models import HTMLField
from django.db import models

# Create your models here.
#Categories
class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle.encode('utf-8')
#commodity
class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)
    #Picture location Server deployment remember to take a look
    gpic = models.ImageField(upload_to='goods')
    gprice = models.DecimalField(max_digits=5,decimal_places=2)
    isDelete = models.BooleanField(default=False)
    #unit
    gunit = models.CharField(max_length=20,default='500g')
    #Clicks for sorting
    gclick = models.IntegerField()
    #Introduction
    gjianjie = models.CharField(max_length=200)
    #in stock
    gkucun = models.IntegerField()
    #Detailed introduction
    #gcontent = HTMLField()
    #
    gtype = models.ForeignKey(TypeInfo, null=True, on_delete =models.CASCADE)

    def __str__(self):
        return self.gtitle.encode('utf-8')

