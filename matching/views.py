from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .logic import build_graph, cluster_students, recommend_partners
from .dummy_data import students  # use dummy data for now

from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Peer Partner Finder Matching App!")

def get_clusters(request):
    g = build_graph(students)
    clusters = cluster_students(g)
    return JsonResponse({"clusters": clusters})

def get_recommendations(request, student_id):
    student_id = int(student_id)
    recs = recommend_partners(student_id, students)
    return JsonResponse({"recommendations": recs})

