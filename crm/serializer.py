from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.fields import BooleanField, FloatField, IntegerField, CharField
from rest_framework.serializers import ModelSerializer

from crm.models import Client, Contract, Event


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ContractSerializer(ModelSerializer):
    status = BooleanField(required=True)
    amount = FloatField(required=True)

    def validate(self, data):
        if data['payment_due'] < timezone.now():
            raise ValidationError({'payment_due': 'Date is invalid'})

        if data['amount'] <= 0:
            raise ValidationError({'amount': 'Amount cannot be zero or less'})
        return data

    class Meta:
        model = Contract
        fields = '__all__'


class EventSerializer(ModelSerializer):
    attendees = IntegerField(required=True)
    notes = CharField(required=True)
    support_contact = CharField(read_only=True)

    def validate(self, data):
        if data['event_date'] < timezone.now():
            raise ValidationError({'event_date': 'Date is invalid'})

        if data['attendees'] <= 0:
            raise ValidationError({'attendees': 'Attendees cannot be zero or less'})
        return data

    class Meta:
        model = Event
        fields = '__all__'
