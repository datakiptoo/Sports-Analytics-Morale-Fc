from django.shortcuts import render

def home(request):
    return render(request,'coachesroom/homepage.html')

def room(request):
    return render(request,'coachesroom/room.html')

