from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Puser(models.Model):
    user = models.OneToOneField(User)
    class Meta:
        managed = True
        db_table = 'Puser'

class City(models.Model):
    city = models.CharField(max_length=100)
    reigon = models.CharField(max_length=100)

    def getDetails(self):
        ret = {}
        ret['id'] = self.id
        ret['name']=self.city
        ret['region']=self.reigon
        return ret

    class Meta:
        managed = True
        db_table = 'City'


class SkuType(models.Model):
    type = models.CharField(max_length=255)
    sub_type = models.TextField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'sku_type'



class ManufactureName(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'manufacturer'


class Products(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    manufacture = models.ForeignKey(ManufactureName, models.DO_NOTHING)
    pack_size = models.CharField(max_length=255)
    sku_type = models.ForeignKey('SkuType', models.DO_NOTHING, db_column='sku_type')
    drug_form = models.CharField(max_length=100)
    pack_form = models.CharField(max_length=100)

    def getDetails(self):
        ret = {}
        ret['id'] = self.id
        ret['name'] = self.name
        ret['drug_form']=self.drug_form
        ret['pack_form']=self.pack_form
        ret['pack_size']=self.pack_size
        ret['manufacture']=self.manufacture.name
        return ret

    class Meta:
        managed = True
        db_table = 'product'



class Availability(models.Model):
    product = models.ForeignKey('Products', models.DO_NOTHING)
    city = models.ForeignKey('City', models.DO_NOTHING)
    mrp = models.CharField(max_length=100)
    cut_price = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    available = models.IntegerField()
    inventory = models.CharField(max_length=100)

    def getDetails(self):
        ret = {}
        ret['id'] = self.id
        ret['mrp'] = self.mrp
        ret['cut_price']=self.cut_price
        ret['price']=self.price
        ret['available']=self.available
        ret['inventory']=self.inventory
        ret['city']=self.city.getDetails()
        return ret

    class Meta:
        managed = True
        db_table = 'Availability'






class SaltName(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    def getDetails(self):
        return {"name":self.name}
    class Meta:
        managed = True
        db_table = 'salt'




class ProductSaltMap(models.Model):
    product = models.ForeignKey('Products', models.DO_NOTHING)
    salt = models.ForeignKey('SaltName', models.DO_NOTHING)
    salt_strength = models.CharField(max_length=255)
    # strength_unit = models.CharField(max_length=100)

    def getDetails(self):
        ret = {}
        ret['id'] = self.id
        ret['salt'] = self.salt.name
        ret['strength_unit']=self.strength_unit
        ret['salt_strength']=self.salt_strength
        return ret

    class Meta:
        managed = True
        db_table = 'product_salt_map'




class Logs(models.Model):
    
    msg = models.CharField(max_length=255)
    user = models.ForeignKey(Puser, models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'logs'