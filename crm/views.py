from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from crm.models import Client, Contract, Event, ContractStatus
from crm.permissions import HasClientPermissions, HasContractPermissions, HasEventPermissions
from crm.serializer import ClientSerializer, ContractSerializer, EventSerializer


class ClientViewSet(ModelViewSet):
    """
    Sales team can :
    - Create a client in the CRM
    - Update a client's information(assigned to them)

    Supports team can:
    - See a client that is related to a current event

    Managements team can :
    - Create, view & update a client
    """

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, HasClientPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['last_name', 'email']

    def get_queryset(self):
        if self.request.user.groups.filter(name='supports'):
            return Client.objects.filter(event__support_contact=self.request.user.id)
        elif self.request.user.groups.filter(name='managements'):
            return Client.objects.all()
        else:
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

    Managements team can :
    - Create, view & update a contract
    """

    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, HasContractPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client__last_name', 'client__email', 'date_created', 'amount']

    def get_queryset(self):
        if self.request.user.groups.filter(name='managements'):
            return Contract.objects.all()
        else:
            return Contract.objects.filter(sales_contact=self.request.user.id)

    def create(self, request, *args, **kwargs):
        request.data['sales_contact'] = request.user.id

        try:
            if request.data['status'] == 1:
                serialized_data = ContractSerializer(data=request.data)
                serialized_data.is_valid(raise_exception=True)
                serialized_data.save()

                ContractStatus.objects.create(signed=1).save()
                return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        except KeyError:
            message = "Field 'status' cannot be blank"
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
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
    """
    Sales team can :
    - Create an event for a signed contract

    Support team can :
    - View and update events assigned to them
    - View client related to event assigned to them

    Managements team can :
    - Assign a support team member to an event
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, HasEventPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client__last_name', 'client__email', 'event_date']

    def get_queryset(self):
        if self.request.user.groups.filter(name='managements'):
            return Event.objects.all()
        else:
            return Event.objects.filter(support_contact=self.request.user.id)

    def create(self, request, *args, **kwargs):
        contract_is_signed = ContractStatus.objects.filter(signed=True).exists()

        try:
            if contract_is_signed:
                serialized_data = EventSerializer(data=request.data)
                serialized_data.is_valid(raise_exception=True)
                serialized_data.save()

                ContractStatus.objects.update(signed=True)

                return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        except KeyError:
            message = "Field 'event_status' cannot be blank"
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = "You cannot create an event for a closed contract"
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        message = "You're not allowed to delete an event"
        return Response(message, status=status.HTTP_405_METHOD_NOT_ALLOWED)
