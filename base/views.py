from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Room, Topic
from .forms import RoomForm


def login_handler(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        messages.error(request, "Username or password incorrect")

    context = {"page": "login"}

    return render(request, "base/login_register.html", context)


def logout_handler(request: HttpRequest):
    logout(request)
    return redirect("home")


def register_handler(request: HttpRequest):
    context = {"page": "register"}

    return render(request, "base/login_register.html", context)


def home_handler(request: HttpRequest):
    q = request.GET.get("q") if request.GET.get("q") is not None else ""

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(desc__icontains=q)
    )
    topics = Topic.objects.all()

    context = {"rooms": rooms, "topics": topics, "rooms_count": rooms.count()}

    return render(request, "base/home.html", context)


def room_handler(request: HttpRequest, id: str):
    room = Room.objects.get(id=id)

    context = {"room": room}

    return render(request, "base/room.html", context)


@login_required(login_url="/login")
def create_room_handler(request: HttpRequest):
    form = RoomForm()

    context = {"form": form}

    if request.method == "POST":
        form = RoomForm(request.POST)
        form.save()

        return redirect("home")

    return render(request, "base/room_form.html", context)


@login_required(login_url="/login")
def update_room_handler(request: HttpRequest, id: str):
    room = Room.objects.get(id=int(id))
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!!")

    context = {"form": form}

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)

        if form.is_valid():
            form.save()
            return redirect("home")

    return render(request, "base/room_form.html", context)


@login_required(login_url="/login")
def delete_room_handler(request: HttpRequest, id: str):
    room = Room.objects.get(id=int(id))

    if request.user != room.host:
        return HttpResponse("You are not allowed here!!")

    if request.method == "POST":

        room.delete()
        return redirect("home")

    context = {"obj": room}

    return render(request, "base/delete.html", context)
