from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Fcuser


def home(request):
    user_id = request.session.get("user")

    if user_id:
        fcuser = Fcuser.objects.get(pk=user_id)
        return HttpResponse(fcuser.username)

    return HttpResponse("home")


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        res_data = {}

        useremail = request.POST.get("useremail", None)
        password = request.POST.get("password", None)

        if not (useremail and password):
            res_data["error"] = "모든 값을 입력해야합니다"
        else:
            fcuser = Fcuser.objects.get(useremail=useremail)
            if check_password(password, fcuser.password):
                request.session["user"] = fcuser.id
                return redirect("/")
            else:
                res_data["error"] = "비밀번호가 틀렸습니다"

        return render(request, "login.html", res_data)


def logout(request):
    if request.session["user"]:
        del request.session["user"]
    return redirect("/")


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        res_data = {}

        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["useremail"]
        re_password = request.POST["re-password"]

        if not (username and email and password and re_password):
            res_data["error"] = "모든 값을 입력해야합니다"
        elif password != re_password:
            res_data["error"] = "비밀번호가 다릅니다"
        else:
            fcuser = Fcuser(
                username=username, password=make_password(password), useremail=email
            )
            fcuser.save()

        return render(request, "register.html", res_data)
