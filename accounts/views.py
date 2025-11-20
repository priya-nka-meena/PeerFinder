from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Profile
import random


# ---------------------------------------------------
# REGISTRATION WITH OTP + UNIQUE USERNAME + UNIQUE EMAIL
# ---------------------------------------------------
def register(request):
    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']

        # 🔥 Allow only NIT Delhi emails
        allowed_domain = "nitdelhi.ac.in"
        email_domain = email.split("@")[-1]

        if email_domain != allowed_domain:
            return render(request, "register.html", {
                "error": "Only NIT Delhi official emails (@nitdelhi.ac.in) are allowed!",
                "data": request.POST
            })

        # 🔥 Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {
                "error": "Username already taken!",
                "data": request.POST
            })

        # 🔥 Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {
                "error": "Email already registered!",
                "data": request.POST
            })

        # 🔥 Store user-entered data temporarily in session
        request.session['reg_data'] = {
            "username": username,
            "name": request.POST['name'],
            "skills": request.POST['skills'],
            "interests": request.POST['interests'],
            "year": request.POST['year'],
            "branch": request.POST['branch'],
            "gender": request.POST['gender'],
            "email": email,
            "password": request.POST['password'],
        }

        # 🔥 Generate OTP
        otp = random.randint(100000, 999999)
        request.session['otp'] = otp

        # 🔥 Send OTP email
        send_mail(
            subject="Your PeerFinder OTP Verification",
            message=f"Your OTP is {otp}",
            from_email="peerpartnernitd@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )

        return redirect("verify_otp")

    return render(request, "register.html")



# ---------------------------------------------------
# VERIFY OTP
# ---------------------------------------------------
def verify_otp(request):
    if request.method == "POST":
        user_otp = request.POST['otp']
        real_otp = str(request.session.get('otp'))

        if user_otp == real_otp:

            data = request.session.get('reg_data')

            # 🔥 Create User using USERNAME (not email)
            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"]
            )

            # 🔥 Create Profile
            Profile.objects.create(
                user=user,
                name=data["name"],
                skills=data["skills"],
                interests=data["interests"],
                year=data["year"],
                branch=data["branch"],
                gender=data["gender"]
            )

            login(request, user)

            # Cleanup session
            del request.session['reg_data']
            del request.session['otp']

            return redirect("dashboard")

        else:
            return render(request, "verify_otp.html", {"error": "Invalid OTP. Please try again."})

    return render(request, "verify_otp.html")



# ---------------------------------------------------
# LOGIN
# ---------------------------------------------------
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})

    return render(request, "login.html")



# ---------------------------------------------------
# LOGOUT
# ---------------------------------------------------
def logout_user(request):
    logout(request)
    return redirect("login")



# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------
@login_required
def dashboard(request):
    return render(request, "dashboard.html")



# ---------------------------------------------------
# PROFILE PAGE
# ---------------------------------------------------
@login_required
def profile(request):
    return render(request, "profile.html", {"profile": request.user.profile})



# ---------------------------------------------------
# EDIT PROFILE
# ---------------------------------------------------
@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        profile.name = request.POST["name"]
        profile.skills = request.POST["skills"]
        profile.interests = request.POST["interests"]
        profile.year = request.POST["year"]
        profile.branch = request.POST["branch"]
        profile.gender = request.POST["gender"]
        profile.save()

        return redirect("profile")

    return render(request, "edit_profile.html", {"profile": profile})



# ---------------------------------------------------
# HOME
# ---------------------------------------------------
def home(request):
    return render(request, "home.html")
