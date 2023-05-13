from rest_framework import serializers
from .models import CustomUser, Todo


# To convert the Model object to an API-appropriate format like JSON, 
# Django REST framework uses the ModelSerializer class to convert any model to serialized JSON objects:

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name']
        
        
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["task", "completed", "timestamp", "updated", "user"]
        