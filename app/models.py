from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATE_CHOICES= (
    ('Anaman & Nicobar Islands', 'Andaman & Nicobar Islands'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chandigarh', 'Chandigarh'),
    ('Chhatisgarh', 'Chhatisgarh'),
    ('Dadar & Nagar Haveli', 'Dadar & Nagar Haveli'),
    ('Daman & Diu', 'Daman & Diu'),
    ('Dehli', 'Dehli'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu & Kashmir', 'Jammu & Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Puducherry', 'Punducherry'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttarakhand', 'Uttarakhand'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('West Bangal', 'West Bangal')
)
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    name= models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=10, null=True)
    locality = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode= models.CharField(max_length=255)
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)
    

# second model
CATEGORY_CHOICE = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear'),
    ('TO', 'Top Offer')
)
class Product(models.Model):
    title = models.CharField(max_length=255)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=255)
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=2, default=CATEGORY_CHOICE)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)
 

 # third model 
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price




# fourth model
STATUS_CHOICE= (
    ('Accepted', "Accepted"),
    ('Packed', "Packed"),
    ('On The Way', "On The Way"),
    ('Delivered', "Delivered"),
    ('Cancel', "Cancel")
)
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICE ,max_length=50, default='Pending')


    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price



class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name






