import tkinter as tk
from tkinter import messagebox, scrolledtext
from collections import deque
import matplotlib.pyplot as plt
import networkx as nx

# ======================== BFS Function ========================
def bfs_shortest_path(graph, start, goal):
    visited = set()
    queue = deque([[start]])

    if start == goal:
        return [start]

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node not in visited:
            for neighbor in graph.get(node, []):
                new_path = path + [neighbor]
                queue.append(new_path)

                if neighbor == goal:
                    return new_path
            visited.add(node)
    return None

# ======================== Graph Visualization ========================
def visualize_graph(graph, path, start, goal):
    G = nx.DiGraph()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    edge_colors = ['red' if (u, v) in zip(path, path[1:]) else 'gray' for u, v in G.edges()]
    node_colors = ['limegreen' if n == start else 'orangered' if n == goal else 'skyblue' for n in G.nodes()]

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors,
            node_size=2000, font_size=14, font_weight='bold', arrowsize=20)
    plt.title(f"Jalur Terpendek (BFS) dari {start} ke {goal}")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# ======================== Graph Input Parser ========================
def parse_graph(input_text):
    graph = {}
    lines = input_text.strip().split('\n')
    for line in lines:
        if ':' in line:
            node, neighbors = line.split(':')
            graph[node.strip().upper()] = [n.strip().upper() for n in neighbors.split(',') if n.strip()]
    return graph

# ======================== Main GUI ========================
def run_bfs():
    graph_input = graph_text.get("1.0", tk.END)
    graph = parse_graph(graph_input)
    start = start_var.get().strip().upper()
    goal = goal_var.get().strip().upper()
    if not start or not goal:
        messagebox.showerror("Input Error", "Silakan isi node awal dan tujuan.")
        return
    if start not in graph or goal not in graph:
        messagebox.showerror("Node Tidak Valid", "Node yang dimasukkan tidak ditemukan dalam graf.")
        return
    path = bfs_shortest_path(graph, start, goal)
    if path:
        result_var.set(f"Jalur terpendek: {' → '.join(path)}")
        visualize_graph(graph, path, start, goal)
    else:
        result_var.set("Tidak ditemukan jalur dari node awal ke tujuan.")

# ======================== GUI Setup ========================
root = tk.Tk()
root.title("Visualisasi BFS - Jalur Terpendek")
root.geometry("600x500")
root.configure(bg="#f4f4f4")

# Title
tk.Label(root, text="Masukkan Struktur Graf (contoh: A:B,C)", font=("Helvetica", 12, "bold"), bg="#f4f4f4").pack(pady=(10, 2))

# Graph input area
graph_text = scrolledtext.ScrolledText(root, height=8, width=60, font=("Courier", 10))
graph_text.pack()
graph_text.insert(tk.END, "A:B,C\nB:D,E\nC:F\nD:\nE:F\nF:")

# Node input
frame_input = tk.Frame(root, bg="#f4f4f4")
tk.Label(frame_input, text="Node Awal:", font=("Helvetica", 10), bg="#f4f4f4").grid(row=0, column=0, padx=5, pady=5)
start_var = tk.StringVar()
tk.Entry(frame_input, textvariable=start_var, width=10).grid(row=0, column=1, padx=5)

tk.Label(frame_input, text="Node Tujuan:", font=("Helvetica", 10), bg="#f4f4f4").grid(row=0, column=2, padx=5)
goal_var = tk.StringVar()
tk.Entry(frame_input, textvariable=goal_var, width=10).grid(row=0, column=3, padx=5)

frame_input.pack(pady=10)

# Run button
tk.Button(root, text="Cari Jalur Terpendek", command=run_bfs, bg="#4285F4", fg="white", font=("Helvetica", 10, "bold")).pack(pady=5)

# Result label
result_var = tk.StringVar()
tk.Label(root, textvariable=result_var, font=("Helvetica", 11), bg="#f4f4f4", fg="green").pack(pady=10)

root.mainloop()