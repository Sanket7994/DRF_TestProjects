from rest_framework import serializers
from .models import School, Student, CustomUser


# To convert the Model object to an API-appropriate format like JSON, 
# Django REST framework uses the ModelSerializer class to convert any model to serialized JSON objects:

class CustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'
        
        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
    