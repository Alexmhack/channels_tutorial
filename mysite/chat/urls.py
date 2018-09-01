from django.urls import path

from .views import index, room_view

urlpatterns = [
	path('', index, name='index'),
	path('<room_name>', room_view, name='room-view'),
]
