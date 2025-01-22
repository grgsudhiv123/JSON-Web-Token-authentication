from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        
    def validate(self, data):
        # Check if age is provided and is less than 18
        if 'age' in data:
            if data['age'] is not None and data['age'] < 18:
                raise serializers.ValidationError({
                    'error': "age cannot be less than 18"
                })

        # Check if name is provided and does not contain digits
        if 'name' in data:
            if any(n.isdigit() for n in data['name']):
                raise serializers.ValidationError({
                    'error': "name cannot contain digits"
                })

        return data
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
    
    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user