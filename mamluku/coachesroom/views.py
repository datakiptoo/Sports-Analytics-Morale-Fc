from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic
from .forms import RoomForm
#rooms=[
 #   {'id':1,'name':'Training'},
  #  {'id':2,'name':'Fixtures'},
   # {'id':3,'name':'Post-Match Reviews'},
     
#]


def loginpage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('Home')
    if request.method == 'POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"User does not exist")
            
            
        user=authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, "Username OR Password does not exist")
            
    context={'page':page}
    return render(request,'coachesroom/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('Home')

def registerUser(request):
    form=UserCreationForm()
    
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('Home')
        else:
            messages.error(request,"An error occured during registration")
            
    return render(request, 'coachesroom/login_register.html',{'form':form})

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q)        
        )
    topics=Topic.objects.all()
    room_count=rooms.count()
    context={'rooms':rooms,'topics':topics,'room_count':room_count}
    return render(request,'coachesroom/homepage.html',context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    context={'rooms':room}    
    return render(request,'coachesroom/chat.html',context)

@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    if request.method =="POST":
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Home')
    context={'form':form}
    return render(request,"coachesroom/room_form.html", context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('you are not allowed here!!')
    
    if request.method == 'POST':
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('Home')
        
    
    context={'form':form}
    return render(request,"coachesroom/room_form.html", context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('you are not allowed here!!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('Home')
    return render(request,'coachesroom/delete.html',{'obj':room})
    

