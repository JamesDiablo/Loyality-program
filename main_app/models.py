from django.db import models



class Card(models.Model):
    """
    This model represents a card in the database.

    Fields:
        series (CharField): A four character string that represents the series of the card.
        number (CharField): A sixteen character string that represents the number of the card.
        release_date (DateTimeField): The date the card was released.
        expire_date (DateTimeField): The date the card will expire.
        last_use_date (DateTimeField): The date the card was last used, this field is nullable and blank.
        purchases_sum (DecimalField): The total amount of purchases made with the card, with a default value of 0.
        status (CharField): A ten character string that represents the status of the card.
        discount_percent (DecimalField): The discount percentage given to the card, with a default value of 0.
        orders (ManyToManyField): The orders made with the card, as a many-to-many relationship with the Order model.
        deleted (BooleanField): A boolean flag that indicates if the card has been deleted, with a default value of False.

    """
    series = models.CharField(max_length=4) 
    number = models.CharField(max_length=16) 
    release_date = models.DateTimeField()  
    expire_date = models.DateTimeField() 
    last_use_date = models.DateTimeField(null=True, blank=True) 
    purchases_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    status = models.CharField(max_length=10) 
    discount_percent = models.DecimalField(max_digits=3, decimal_places=2, default=0) 
    orders = models.ManyToManyField("Order") 
    deleted = models.BooleanField(default=False) 


class Order(models.Model):
    """
    This model represents an order in the database.

    Fields:
        id_order (AutoField): A unique identifier for the order.
        date (DateTimeField): The date the order was made.
        sum (DecimalField): The total sum of the order.
        discount_percent (DecimalField): The discount percentage applied to the order.
        discount_calculation (DecimalField): The calculation of the discount applied to the order.

    """
    id_order = models.AutoField(primary_key=True)
    date = models.DateTimeField() 
    sum = models.DecimalField(max_digits=10, decimal_places=2) 
    discount_percent = models.DecimalField(max_digits=3, decimal_places=2) 
    discount_calculation = models.DecimalField(max_digits=10, decimal_places=2) 

class Item(models.Model):
    """
    This model represents an items in the database.

    Fields:
        order (ForeignKey): The order the item belongs to, as a foreign key relationship with the Order model.
        name (CharField): The name of the item.
        price (DecimalField): The price of the item.
        discounted_price (DecimalField): The discounted price of the item.

    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2) 

class Basket(models.Model):
    """
    This is the Basket model, which represents the basket of the user.

    Attributes:
        card (ForeignKey): ForeignKey to the Card model, representing the card that the user has added to the basket.
        date_added (DateTimeField): DateTimeField representing the date and time when the card was added to the basket. 
        This field is automatically set to the current date and time when the object is created.

    Note:
        When a Card object is deleted, all related Basket objects will also be deleted, due to the `on_delete` argument set to `models.CASCADE`.
    """
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)