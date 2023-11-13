from django.shortcuts import render
from .models import Room

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
    context={}
    return render(request,"coachesroom/room_form.html", context)

