from rest_framework import serializers
from .models import Product, Category
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

 
class RegisterUserSer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(trim_whitespace=False)
    password2 = serializers.CharField(trim_whitespace=False)

    def validate(self, attrs):
        pass1=attrs.get('password1')
        pass2 = attrs.get('password2')
        if pass2 != pass1:
            raise serializers.ValidationError({"password":"parollar bir xil emas"})
        return super().validate(attrs)

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        password2 = validated_data.pop('password2')
        user=User.objects.create_user(**validated_data)
        user.set_password(password1)
        user.save()
        token = Token.objects.create(user=user)
        return token
    
    class Meta:
        model = User
        fields = ["id", "email", "password"]


class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']















class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
