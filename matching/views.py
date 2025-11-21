from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .logic import build_graph, cluster_students, recommend_partners, get_student_data
from accounts.models import Invitation  # invite system included


# --------------------------
# Show all clusters
# --------------------------
@login_required
def show_clusters(request):
    students = get_student_data()
    g = build_graph(students)
    clusters_ids = cluster_students(g)

    student_dict = {s["id"]: s for s in students}
    clusters = {cid: [student_dict[i] for i in ids] for cid, ids in clusters_ids.items()}

    return render(request, "matching/clusters.html", {"clusters": clusters})


# --------------------------
# Show top recommendations for a student
# --------------------------
@login_required
def show_recommendations(request, student_id):
    students = get_student_data()
    recs = recommend_partners(student_id, students)

    student_dict = {s["id"]: s for s in students}
    current_user = request.user

    final_recs = []

    for r in recs:
        target_student = student_dict[r[0]]
        target_user = get_object_or_404(User, id=target_student["id"])

        # Skip showing yourself
        if target_user.id == current_user.id:
            continue

        # Fetch invitation status if exists
        invite = Invitation.objects.filter(
            sender=current_user,
            receiver=target_user
        ).first()

        invite_status = invite.status if invite else "not_sent"

        final_recs.append({
            "student": target_student,
            "user_obj": target_user,
            "score": r[1],
            "invite_status": invite_status
        })

    return render(request, "matching/recommendations.html", {
        "recommendations": final_recs
    })


# --------------------------
# Show interactive graph
# --------------------------
@login_required
def show_graph(request):
    students = get_student_data()
    g = build_graph(students)

    nodes = students
    links = []

    for src, neighbors in g.items():
        for tgt in neighbors:
            if {"source": tgt, "target": src} not in links:
                links.append({"source": src, "target": tgt})

    return render(request, "matching/graph.html", {"nodes": nodes, "links": links})


# --------------------------
# Home page
# --------------------------
def home(request):
    return render(request, "matching/home.html")


# --------------------------
# Show received invitations
# --------------------------
@login_required
def show_invitations(request):
    invites = Invitation.objects.filter(
        receiver=request.user,
        status="pending"
    ).order_by("-created_at")

    return render(request, "matching/invitations.html", {
        "invites": invites
    })


# --------------------------
# Approve / Reject invitation
# --------------------------
@login_required
def respond_invitation(request, invite_id, action):
    invite = get_object_or_404(Invitation, id=invite_id)

    # Security: Only receiver can respond
    if invite.receiver != request.user:
        return redirect("invitations")

    if action == "approve":
        invite.status = "approved"
    elif action == "reject":
        invite.status = "rejected"

    invite.save()
    return redirect("invitations")

from accounts.models import Profile

@login_required
def view_student_profile(request, user_id):
    student_user = get_object_or_404(User, id=user_id)
    student_profile = get_object_or_404(Profile, user=student_user)

    return render(request, "matching/student_profile.html", {
        "student_user": student_user,
        "student_profile": student_profile
    })

