from django.shortcuts import render, redirect
from django.urls import reverse

def index(request):
	return render(request, 'index.html')

def room(request, room_name):
	print('room name', room_name)
	return render(request, 'room.html', {'room_name':room_name})

