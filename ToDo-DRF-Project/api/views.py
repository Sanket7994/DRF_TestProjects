from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Todo
from .serializer import TodoSerializer

# Create your views here.
class TodoListViewAPI(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    # 1. List all the todo items for given requested user
    def get(self, request, *args, **kwargs):
        todos = Todo.objects.filter(user = request.user.id)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    
    # 3. Create the Todo with given todo data
    def post(self, request, *args, **kwargs):
        
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
            }
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        return Response(serializer.error, status = status.HTTP_400_BAD_REQUEST)
    
    
# Create your views here.
class TodoDetailApiView(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    # 1. Helper method to get the object with given todo_id, and user_id
    def get_object(self, todo_id, user_id):
        try:
            return Todo.objects.get(id=todo_id, user=user_id)
        except Todo.DoesNotExist:
            raise ValueError('User does not exist.')
        
        
    # 2. Retrieves the Todo with given todo_id
    def get(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response({
                "res": "Object with this Todo_id doesn`t exist."}, 
                            status = status.HTTP_400_BAD_REQUEST)
            
        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 3. Updates the todo item with given todo_id if exists
    def put(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response({
                "res": "Object with this Todo_id doesn`t exist."}, 
                            status = status.HTTP_400_BAD_REQUEST)
        
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
            }
        serializer = TodoSerializer(instance = todo_instance, 
                                    data=data, 
                                    partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            
            
    # 3. Deletes the todo item with given todo_id if exists
    def delete(self, request, todo_id, *args, **kwargs):
        
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response({
                "res": "Object with this Todo_id doesn`t exist."}, 
                            status = status.HTTP_400_BAD_REQUEST)
            
        todo_instance.delete()
        return Response({"res":"Object deleted successfully."}, status=status.HTTP_200_OK)