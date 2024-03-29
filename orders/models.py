from django.db import models
from accounts.models import User
from menu.models import FoodItem
from vendor.models import Vendor

request_object = ''

class Payment(models.Model):
    PAYMENT_METHOD = (
        ('PayPal', 'PayPal'),
        ('RazorPay', 'RazorPay'), # Only for Indian Students.
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=100)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id

    

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    vendors = models.ManyToManyField(Vendor,blank=True) #type:ignore
    order_number = models.CharField(max_length=20)
    # billing address
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=15, blank=True)
    state = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)

    total = models.FloatField()
    tax_data = models.JSONField(blank=True, help_text = "Data format: {'tax_type':{'tax_percentage':'tax_amount'}}",null=True) #type:ignore
    total_data = models.JSONField(blank=True, help_text = "Data format:{vendor1: {'tax_type':{'tax_percentage':'tax_amount'}}}",null=True)
    total_tax = models.FloatField()
    
    payment_method = models.CharField(max_length=25)
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Concatenate first name and last name
    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.order_number

    # Will calculate total amount and tax amount for each vendor for single order
    def get_total_by_vendor(self):
        vendor = Vendor.objects.get(user=request_object.user) #type:ignore
        subtotal,total_tax=0,0
        tax_dict = {}

        if self.total_data:
            vendor_data = self.total_data.get(str(vendor.id))  #type:ignore

            # calculate tax_dict and subtotal
            subtotal = 0
            tax_dict = {}
            for sub_total,tax in vendor_data.items():
                subtotal += float(sub_total)
                tax_dict.update(tax)

            # calculate total tax
            total_tax = 0
            for tax in tax_dict:
                for value in tax_dict[tax]:
                    total_tax += tax_dict[tax][value]

        context = {
            'grand_total':round(subtotal+total_tax,2),
            'subtotal':round(subtotal,2),
            'total_tax':round(total_tax,2),
            'tax_dict':tax_dict,
        }
        return context
   
    def order_placed_to(self):
        return ", ".join(str(i) for i in self.vendors.all())



class OrderedFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fooditem.food_title