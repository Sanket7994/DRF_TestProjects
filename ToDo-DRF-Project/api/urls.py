from django.urls import path, include
from .views import TodoListViewAPI, TodoDetailApiView

urlpatterns = [
    path('api-auth', include('rest_framework.urls')),
    path('todos/', TodoListViewAPI.as_view()),
    path('todos/<int:todo_id>/', TodoDetailApiView.as_view()),
]


