from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room, Topic, Messages
from .forms import RoomForm

# Create your views here.

def loginPage(request):
    page = 'login'
    # Avoid user to re-login if he already logged-in
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exit!")
            
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        elif user is not None and password is None:
            return messages.error(request, "Enter the password to login!")
        else:
            return messages.error(request, "Username or Password does not match!")
        
    context = {'page':  page}
    return render(request, 'base/login_registration.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration.')
            
    context = {'form': form}
    return render(request, 'base/login_registration.html', context)


def home(request):
    # Using filter function to create a search functionality by setting a URL parameter 'q'
    # If q has a value it will filter out those values from the data and If its empty or None
    # user will stay at home page or nothing changes or gets a full topic list view
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    # here xxx__icontains is a filter arguments and it ensures that it searches the whole xxx field for the argument
    # Q is a conditional filter 
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Messages.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': topics, 'room_count':  room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)



def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = Messages.objects.filter(room=room)
    participants = room.participants.all()
    
    if request.method == 'POST':
        message = Messages.objects.create(
            user=request.user,
            room=room, 
            body=request.POST.get('body'),    
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
        
    context = {'room': room, 'room_messages': room_messages, 'participants': participants,}
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.messages.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


# Added a decorator which checks if the user is authenticated or not
# If not, User will not be able to create a room without logging in or creating an account
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


# Restricting unauthenticated user to update a room
@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed!')
    # Creating a condition if the changes in the Post needs to be updated
    # the form will be validated and after update is successful
    # user will be redirected to the Home page
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)



# Restricting unauthenticated user to delete a room
@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})



@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Messages.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('You are not allowed!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message,})