from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm
#rooms=[
 #   {'id':1,'name':'Training'},
  #  {'id':2,'name':'Fixtures'},
   # {'id':3,'name':'Post-Match Reviews'},
     
#]

def home(request):
    rooms = Room.objects.all()
    context={'rooms':rooms}
    return render(request,'coachesroom/homepage.html',context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    context={'rooms':room}    
    return render(request,'coachesroom/chat.html',context)

def createRoom(request):
    form=RoomForm()
    if request.method =="POST":
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Home')
    context={'form':form}
    return render(request,"coachesroom/room_form.html", context)

def updateRoom(request, pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    
    if request.method == 'POST':
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('Home')
        
    
    context={'form':form}
    return render(request,"coachesroom/room_form.html", context)

def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('Home')
    return render(request,'coachesroom/delete.html',{'obj':room})
    

