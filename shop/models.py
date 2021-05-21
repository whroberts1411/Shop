from django.db import models

#------------------------------------------------------------------------------
class Product(models.Model):
    """ One record per product. All product details held here. """

    title = models.CharField(max_length=200)
    price = models.FloatField()
    discount_price = models.FloatField()
    category = models.CharField(max_length=200)
    description = models.TextField()
    image = models.CharField(max_length=300)

#------------------------------------------------------------------------------
    def __str__(self):
        return self.title
#------------------------------------------------------------------------------
class Shopper(models.Model):
    """ Holds details of each registered user of the site. """

    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)
    userid = models.IntegerField(default=1)

 #------------------------------------------------------------------------------
    def __str__(self):
        return self.name
#------------------------------------------------------------------------------
class Order(models.Model):
    """ A header record for an order - just needs an id and a link to the
        Shopper record.   """

    orderdate = models.DateTimeField(auto_now=True)
    userid = models.ForeignKey(Shopper, blank=True, null=True, on_delete=models.CASCADE)

#------------------------------------------------------------------------------
class Item(models.Model):
    """ Main order item record, which links to the product record and the
        order record. The order_ref field is used to link together all order
        items for the same order. """

    item = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cost = models.FloatField()
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.CASCADE)

#------------------------------------------------------------------------------
class OrderRef(models.Model):
    """ The order ref is incremented for each order. Just a single record is
        stored on the database.  """

    order_ref = models.IntegerField()

#------------------------------------------------------------------------------
