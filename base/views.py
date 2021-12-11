from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Room
from .forms import RoomForm


def home(request: HttpRequest):
    rooms = Room.objects.all()
    context = {"rooms": rooms}

    return render(request, "base/home.html", context)


def room(request: HttpRequest, id: str):
    room = Room.objects.get(id=id)

    context = {"room": room}

    return render(request, "base/room.html", context)


def create_room(request: HttpRequest):
    form = RoomForm()

    context = {"form": form}

    if request.method == "POST":
        form = RoomForm(request.POST)
        form.save()

        return redirect("home")

    return render(request, "base/room_form.html", context)


def update_room(request: HttpRequest, id: str):
    room = Room.objects.get(id=int(id))
    form = RoomForm(instance=room)

    context = {"form": form}

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)

        if form.is_valid():
            form.save()
            return redirect("home")

    return render(request, "base/room_form.html", context)


def delete_room(request: HttpRequest, id: str):
    room = Room.objects.get(id=int(id))

    if request.method == "POST":
        room.delete()
        return redirect("home")

    context = {"obj": room}

    return render(request, "base/delete.html", context)
