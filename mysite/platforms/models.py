from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Platform(models.Model):
    property_type_choices = [
        ('Residential', 'Residential'),
        ('Commercial', 'Commercial'),
        ('Land', 'Land'),
        ('Industrial', 'Industrial'),
        ('Special Purpose', 'Special Purpose')
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold Out'),
    ]

    owner_contact_number = models.CharField(max_length=15, blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(default="This Property is mindblowing!")
    property_type = models.CharField(max_length=20, choices=property_type_choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size_sqft = models.PositiveIntegerField()
    year_built = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    listed_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='platform_image/', blank=True, null=True, default='platform_image/houses.png')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    sold_date = models.DateTimeField(null=True, blank=True)


    def mark_as_sold(self):
        self.status = 'sold'
        self.sold_date = now()
        self.save()

    def __str__(self):
        return f"{self.title} in {self.location}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    ], default='Pending')
    date_placed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid of {self.amount} on {self.property} by {self.user}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Platform, on_delete=models.CASCADE)

    def __str__(self):
        return self.property.title

    class Meta:
        unique_together = ('user', 'property')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # New field for profile photo
    about_me = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.user.username
