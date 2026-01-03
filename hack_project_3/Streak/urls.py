from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name="index"),
	# path('enter_room/', views.enter_room, name="enter_room"),
	path("<str:room_name>/", views.room, name="room"),
]