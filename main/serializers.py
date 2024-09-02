from django.contrib.auth.models import User
from rest_framework import serializers
from .models import FriendRequest
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Creating a new user with the email, username and password
        user = User(
            email=validated_data['email'].lower(),
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        # Custom validation logic for login
        email = data.get('email').lower()
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("Invalid credentials.")

        if not user.check_password(password):
            raise ValidationError("Invalid credentials.")
        return data


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'timestamp']

    def validate(self, data):
        sender = self.context['request'].user
        receiver = data['receiver']
        if sender == receiver:
            raise serializers.ValidationError("You cannot send a friend request to yourself.")
        if FriendRequest.objects.filter(sender=sender, receiver=receiver, status='pending').exists():
            raise serializers.ValidationError("A friend request is already pending for this user.")
        return data
