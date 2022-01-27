from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from crm.models import Client, Contract, Event, ContractStatus
from crm.permissions import HasClientPermissions, HasContractPermissions
from crm.serializer import ClientSerializer, ContractSerializer, EventSerializer


class ClientViewSet(ModelViewSet):
    """
    Sales team can :
    - Create a client in the CRM
    - Update a client's information(assigned to them)
    """

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, HasClientPermissions]

    def get_queryset(self):
        return Client.objects.filter(sales_contact=self.request.user.id)

    def create(self, request, *args, **kwargs):
        request.data['sales_contact'] = request.user.id
        return super(ClientViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.data['sales_contact'] = request.user.id
        return super(ClientViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        message = "You're not allowed to delete a client"
        return Response(message, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ContractViewSet(ModelViewSet):
    """
    Sales team can :
    - Create a contract for a client(only if the contract is signed)
    - Indicate that an open(int:1) contract is signed.
    """

    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, HasContractPermissions]

    def get_queryset(self):
        return Contract.objects.filter(sales_contact=self.request.user.id)

    def create(self, request, *args, **kwargs):
        request.data['sales_contact'] = request.user.id

        if request.data['status'] == 1:
            serialized_data = ContractSerializer(data=request.data)
            serialized_data.is_valid(raise_exception=True)
            serialized_data.save()

            ContractStatus.objects.create(signed=1).save()
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        else:
            serialized_data = ContractSerializer(data=request.data)
            serialized_data.is_valid(raise_exception=True)
            serialized_data.save()

            request.data['status'] = ContractStatus.objects.create(signed=0).save()

            return Response(serialized_data.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        request.data['sales_contact'] = request.user.id
        return super(ContractViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        message = "You're not allowed to delete a contract"
        return Response(message, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
