from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from crm.models import Client, Contract, Event
from crm.permissions import HasClientPermissions
from crm.serializer import ClientSerializer, ContractSerializer, EventSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all().order_by('id')
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, HasClientPermissions]


class ContractViewSet(ModelViewSet):
    queryset = Contract.objects.all().order_by('id')
    serializer_class = ContractSerializer


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all().order_by('id')
    serializer_class = EventSerializer
