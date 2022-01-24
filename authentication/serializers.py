from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from authentication.models import CustomUser


class RegisterSerializer(ModelSerializer):
    password = CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()

        return user
