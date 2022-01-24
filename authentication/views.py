from rest_framework import generics
from rest_framework.permissions import AllowAny

from authentication.models import CustomUser
from authentication.serializers import RegisterSerializer


# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
