from django.conf import settings
from django.db import models


# Create your models here.
class Client(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=25)
    mobile = models.CharField(max_length=25)
    company_name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Client: {self.first_name} | Company: {self.company_name}"


class Contract(models.Model):
    sales_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    amount = models.FloatField(blank=True)
    payment_due = models.DateTimeField()

    def __str__(self):
        return f"Contract ID: {self.id} | Client: {self.client.first_name} | Sales Contact: {self.sales_contact}"


class ContractStatus(models.Model):
    signed = models.BooleanField(default=False)

    def __str__(self):
        return f"Contract ID: {self.id} | Signed: {self.signed}"


class Event(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    event_status = models.ForeignKey(to=ContractStatus, on_delete=models.CASCADE)
    attendees = models.IntegerField(default=0)
    event_date = models.DateTimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Event ID: {self.id} | Client: {self.client.first_name} | Support Contact: {self.support_contact} | " \
               f"Event Status: {self.event_status}"
