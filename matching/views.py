from django.shortcuts import render
from .logic import build_graph, cluster_students, recommend_partners, get_student_data


# --------------------------
# Show all clusters
# --------------------------
def show_clusters(request):
    students = get_student_data()
    g = build_graph(students)
    clusters_ids = cluster_students(g)

    # Map student IDs to full student info
    student_dict = {s["id"]: s for s in students}
    clusters = {cid: [student_dict[i] for i in ids] for cid, ids in clusters_ids.items()}

    return render(request, "matching/clusters.html", {"clusters": clusters})

# --------------------------
# Show top recommendations for a student
# --------------------------
def show_recommendations(request, student_id):
    students = get_student_data()
    recs = recommend_partners(student_id, students)

    student_dict = {s["id"]: s for s in students}
    recs_with_names = [{"student": student_dict[r[0]], "score": r[1]} for r in recs]

    return render(request, "matching/recommendations.html", {"recommendations": recs_with_names})

# --------------------------
# Show interactive D3.js graph
# --------------------------
def show_graph(request):
    students = get_student_data()
    g = build_graph(students)

    nodes = students
    links = []
    for src, neighbors in g.items():
        for tgt in neighbors:
            # Avoid duplicate links
            if {"source": tgt, "target": src} not in links:
                links.append({"source": src, "target": tgt})

    return render(request, "matching/graph.html", {"nodes": nodes, "links": links})

# --------------------------
# Optional: Home page
# --------------------------
def home(request):
    return render(request, "matching/home.html")  # create a simple home.html
