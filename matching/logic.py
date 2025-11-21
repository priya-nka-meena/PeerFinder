# # matching/logic.py
# from itertools import combinations

# # Function to compute similarity between two students
# def similarity(student1, student2):
#     skill_match = len(set(student1['skills']) & set(student2['skills']))
#     interest_match = len(set(student1['interests']) & set(student2['interests']))
#     return skill_match + interest_match  # simple sum, can weight if needed

# # Build graph (adjacency list)
# def build_graph(students, threshold=1):
#     graph = {s['id']: [] for s in students}
#     for s1, s2 in combinations(students, 2):
#         sim = similarity(s1, s2)
#         if sim >= threshold:
#             graph[s1['id']].append(s2['id'])
#             graph[s2['id']].append(s1['id'])
#     return graph

# # Union-Find to form clusters
# def find(parent, x):
#     if parent[x] != x:
#         parent[x] = find(parent, parent[x])
#     return parent[x]

# def union(parent, x, y):
#     px = find(parent, x)
#     py = find(parent, y)
#     if px != py:
#         parent[py] = px

# def cluster_students(graph):
#     parent = {node: node for node in graph}
#     for node, neighbors in graph.items():
#         for neighbor in neighbors:
#             union(parent, node, neighbor)
#     clusters = {}
#     for node in parent:
#         root = find(parent, node)
#         if root not in clusters:
#             clusters[root] = []
#         clusters[root].append(node)
#     return clusters

# # Recommend partners for a student
# def recommend_partners(student_id, students, top_n=3):
#     target = next(s for s in students if s['id'] == student_id)
#     scores = []
#     for s in students:
#         if s['id'] != student_id:
#             scores.append((s['id'], similarity(target, s)))
#     scores.sort(key=lambda x: x[1], reverse=True)
#     return scores[:top_n]

# # Example usage (only runs if you run this file directly)
# if __name__ == "__main__":
#     from .dummy_data import students
#     g = build_graph(students)
#     clusters = cluster_students(g)
#     print("Clusters:", clusters)
#     print("Recommendations for Alice:", recommend_partners(1, students))



#with actual profile data
# matching/logic.py
from itertools import combinations
from accounts.models import Profile

# --------------------------
# 1️⃣ Helper to fetch students
# --------------------------
def get_student_data():
    students = []
    for profile in Profile.objects.all():
        students.append({
            "id": profile.id,
            "name": profile.name,
            "skills": profile.skills_list(),       # convert comma-separated to list
            "interests": profile.interest_list(),
            "year": profile.year,
            "branch": profile.branch,
            "gender": profile.gender,
            "user_id": profile.user.id,
        })
    return students

# --------------------------
# 2️⃣ Similarity function
# --------------------------
def similarity(student1, student2):
    skill_match = len(set(student1['skills']) & set(student2['skills']))
    interest_match = len(set(student1['interests']) & set(student2['interests']))
    return skill_match + interest_match  # simple sum, can weight if needed

# --------------------------
# 3️⃣ Build graph
# --------------------------
def build_graph(students, threshold=1):
    graph = {s['id']: [] for s in students}
    for s1, s2 in combinations(students, 2):
        sim = similarity(s1, s2)
        if sim >= threshold:
            graph[s1['id']].append(s2['id'])
            graph[s2['id']].append(s1['id'])
    return graph

# --------------------------
# 4️⃣ Union-Find clustering
# --------------------------
def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]

def union(parent, x, y):
    px = find(parent, x)
    py = find(parent, y)
    if px != py:
        parent[py] = px

def cluster_students(graph):
    parent = {node: node for node in graph}
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            union(parent, node, neighbor)
    clusters = {}
    for node in parent:
        root = find(parent, node)
        if root not in clusters:
            clusters[root] = []
        clusters[root].append(node)
    return clusters

# --------------------------
# 5️⃣ Recommendations
# --------------------------
def recommend_partners(student_id, students, top_n=3):
    target = next(s for s in students if s['id'] == student_id)
    scores = []
    for s in students:
        if s['id'] != student_id:
            scores.append((s['id'], similarity(target, s)))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_n]

# --------------------------
# 6️⃣ Example usage (optional)
# --------------------------
if __name__ == "__main__":
    students = get_student_data()  # pull from DB
    g = build_graph(students)
    clusters = cluster_students(g)
    print("Clusters:", clusters)
    print("Recommendations for first student:", recommend_partners(students[0]['id'], students))
