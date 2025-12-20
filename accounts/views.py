from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import random

from .models import Profile, Invitation


# ---------------------------------------------------
# REGISTRATION WITH OTP
# ---------------------------------------------------
def register(request):
    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']

        # Only allow @nitdelhi.ac.in
        allowed_domain = "nitdelhi.ac.in"
        if email.split("@")[-1] != allowed_domain:
            return render(request, "register.html", {
                "error": "Only NIT Delhi emails allowed!",
                "data": request.POST
            })

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {
                "error": "Username already taken!",
                "data": request.POST
            })

        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {
                "error": "Email already registered!",
                "data": request.POST
            })

        # Store details in session
        request.session['reg_data'] = {
            "username": username,
            "name": request.POST['name'],
            "skills": request.POST['skills'],
            "interests": request.POST['interests'],
            "year": request.POST['year'],
            "branch": request.POST['branch'],
            "gender": request.POST['gender'],
            "contact_number": request.POST['contact_number'],  # ✅ add this
            
            "email": email,
            "password": request.POST['password'],
        }

        otp = random.randint(100000, 999999)
        request.session['otp'] = otp

        send_mail(
            subject="PeerFinder OTP Verification",
            message=f"Your OTP is {otp}",
            from_email="peerpartnernitd@gmail.com",
            recipient_list=[email],
        )

        return redirect("verify_otp")

    return render(request, "register.html")


# ---------------------------------------------------
# VERIFY OTP
def verify_otp(request):
    if request.method == "POST":

        # SAFE FETCH
        otp_session = request.session.get('otp')
        reg_data = request.session.get('reg_data')

        if not reg_data:
            return render(request, "verify_otp.html", {"error": "Session expired! Please register again."})

        if request.POST['otp'] == str(otp_session):

            user = User.objects.create_user(
                username=reg_data["username"],
                email=reg_data["email"],
                password=reg_data["password"],
            )

            Profile.objects.create(
                user=user,
                name=reg_data["name"],
                skills=reg_data["skills"],
                interests=reg_data["interests"],
                year=reg_data["year"],
                branch=reg_data["branch"],
                gender=reg_data["gender"],
                contact_number=reg_data["contact_number"],
            )

            login(request, user)

            # SAFE DELETE
            request.session.pop('reg_data', None)
            request.session.pop('otp', None)

            return redirect("dashboard")

        return render(request, "verify_otp.html", {"error": "Invalid OTP"})

    return render(request, "verify_otp.html")

# ---------------------------------------------------
# LOGIN
# ---------------------------------------------------
def login_user(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect("dashboard")

        return render(request, "login.html", {"error": "Invalid credentials"})

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
# PROFILE
# ---------------------------------------------------
@login_required
def profile(request):
    return render(request, "profile.html", {"profile": request.user.profile})


# ---------------------------------------------------
# EDIT PROFILE
# ---------------------------------------------------
# @login_required
# def edit_profile(request):
#     profile = request.user.profile

#     if request.method == "POST":
#         profile.name = request.POST["name"]
#         profile.skills = request.POST["skills"]
#         profile.interests = request.POST["interests"]
#         profile.year = request.POST["year"]
#         profile.branch = request.POST["branch"]
#         profile.gender = request.POST["gender"]
#         profile.contact_number = request.POST["contact_number"]
#         profile.save()

#         return redirect("profile")

#     return render(request, "edit_profile.html", {"profile": profile})

@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        profile.name = request.POST.get("name")
        profile.skills = request.POST.get("skills")
        profile.interests = request.POST.get("interests")
        profile.year = request.POST.get("year")
        profile.branch = request.POST.get("branch")
        profile.gender = request.POST.get("gender")
        profile.contact_number = request.POST.get("contact_number")  # SAFE

        profile.save()
        return redirect("profile")

    return render(request, "edit_profile.html", {"profile": profile})

# ---------------------------------------------------
# SEND INVITATION
# ---------------------------------------------------
@login_required
def send_invitation(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)

    existing = Invitation.objects.filter(
        sender=request.user,
        receiver=receiver
    ).first()

    if not existing:
        Invitation.objects.create(sender=request.user, receiver=receiver)

    return redirect(request.META.get("HTTP_REFERER", "dashboard"))


# ---------------------------------------------------
# VIEW MY INVITATIONS
# ---------------------------------------------------
@login_required
def my_invitations(request):
    invites = Invitation.objects.filter(receiver=request.user)
    return render(request, "matching/invitations.html", {"invites": invites})


# ---------------------------------------------------
# APPROVE INVITATION
# ---------------------------------------------------
@login_required
def approve_invitation(request, invite_id):
    invite = get_object_or_404(Invitation, id=invite_id, receiver=request.user)
    invite.status = "approved"
    invite.save()
    return redirect("my_invitations")


# ---------------------------------------------------
# REJECT INVITATION
# ---------------------------------------------------
@login_required
def reject_invitation(request, invite_id):
    invite = get_object_or_404(Invitation, id=invite_id, receiver=request.user)
    invite.status = "rejected"
    invite.save()
    return redirect("my_invitations")


# ---------------------------------------------------
# HOME
# ---------------------------------------------------
def home(request):
    return render(request, "home.html")
