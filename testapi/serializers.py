import logging
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers

from django_project.utils import custom_exceptions as ce
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

logger = logging.getLogger('testapi')

class UserCreateSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, style={
                                     "input_type":   "password"})
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True, label="Confirm password")

    class Meta:
        model = User
        fields = [
            "email",
            "password1",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        email = validated_data["email"]
        password1 = validated_data["password1"]
        password2 = validated_data["password2"]
        if (email and User.objects.filter(email=email).exists()):
            raise serializers.ValidationError(
                {"email": "Email addresses must be unique."})
        if password1 != password2:
            raise serializers.ValidationError(
                {"password": "The two passwords differ."})
        user = User(email=email)
        user.set_password(password1)
        user.save()
        return user

class UserSigninSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)
    
    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise ce.ValidationFailed(
                'Invalid credentials, please try again.'
            )
        try:
            # logger.info(user._meta.get_fields())
            # logger.info(
            #     "UserSigninSerializer - user type = {}".format(type(user))
            # )
            # logger.info(
            #     "UserSigninSerializer - user fileds = {}".format(user.__dict__)
            # )

            refresh = RefreshToken.for_user(user)
            update_last_login(None, user)
            
        except User.DoesNotExist:
            raise ce.ValidationFailed(
                'No such user, please try again.'
            )

        data = {
            'email' : user.email,
            'access' : str(refresh.access_token),
            'refresh' : str(refresh)
        }

        # logger.info(
        #     "UserSigninSerializer - data = {}".format(data)
        # )
        return data

class EmailSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=100, min_length=None, allow_blank=False)
    email_subject = serializers.CharField(max_length=255)
    email_message = serializers.CharField(max_length=255)

    

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token
