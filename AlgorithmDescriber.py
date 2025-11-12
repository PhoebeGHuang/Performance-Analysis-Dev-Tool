import tkinter as tk
from tkinter import ttk, messagebox

class AlgorithmDescriber:
    """
    descriptions of common algorithms
    integrated with CodeDisplayer as a popup reference tool
    """

    def __init__(self):

        self.algorithms = {
            "Bubble Sort": {
                "description": (
                    "Bubble Sort repeatedly compares adjacent elements and swaps them "
                    "if they are in the wrong order. The largest elements "
                    "move to the end of the list after each pass."
                ),
                "time_complexity": "O(n²)",
                "space_complexity": "O(1)",
                "category": "Sorting"
            },
            "Selection Sort": {
                "description": (
                    "Selection Sort repeatedly selects the smallest element from the unsorted "
                    "portion of the list and places it at the beginning."
                ),
                "time_complexity": "O(n²)",
                "space_complexity": "O(1)",
                "category": "Sorting"
            },
            "Insertion Sort": {
                "description": (
                    "Insertion Sort builds a sorted portion of the array one element at a time. "
                    "It compares each new element with those before it and inserts it in its correct position."
                ),
                "time_complexity": "O(n²)",
                "space_complexity": "O(1)",
                "category": "Sorting"
            },
            "Merge Sort": {
                "description": (
                    "Merge Sort sorts by recursively splitting the array into halves, "
                    "sorting each half, and merging them back together."
                ),
                "time_complexity": "O(n log n)",
                "space_complexity": "O(n)",
                "category": "Sorting"
            },
            "Quick Sort": {
                "description": (
                    "Quick Sort selects a pivot element and partitions the list into elements less "
                    "than and greater than the pivot, then recursively sorts each partition."
                ),
                "time_complexity": "O(n log n) average, O(n²) worst case",
                "space_complexity": "O(log n)",
                "category": "Sorting"
            },
            "Binary Search": {
                "description": (
                    "Binary Search operates on a sorted array by repeatedly dividing the search "
                    "interval in half and narrowing down to the target element."
                ),
                "time_complexity": "O(log n)",
                "space_complexity": "O(1)",
                "category": "Searching"
            },
            "Linear Search": {
                "description": (
                    "Linear Search scans each element of the array sequentially until it finds "
                    "the target element or reaches the end of the list."
                ),
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "category": "Searching"
            },
            "Dijkstra's Algorithm": {
                "description": (
                    "Dijkstra's Algorithm finds the shortest path between nodes in a weighted graph, "
                    "using a priority queue to explore the smallest distances first."
                ),
                "time_complexity": "O((V + E) log V)",
                "space_complexity": "O(V)",
                "category": "Graph"
            },
            "Breadth First Search": {
                "description": (
                    "BFS explores a graph level by level using a queue, visiting all nodes at the "
                    "current depth before moving deeper."
                ),
                "time_complexity": "O(V + E)",
                "space_complexity": "O(V)",
                "category": "Graph Traversal"
            },
            "Depth First Search": {
                "description": (
                    "DFS explores as far down a branch as possible before backtracking, typically implemented "
                    "using recursion or a stack."
                ),
                "time_complexity": "O(V + E)",
                "space_complexity": "O(V)",
                "category": "Graph Traversal"
            }
        }

    # methods

    def get_description(self, name):
        # returns description of a specific algorithm
        algo = self.algorithms.get(name)
        if algo:
            return (
                f"Algorithm: {name}\n"
                f"Category: {algo['category']}\n"
                f"Time Complexity: {algo['time_complexity']}\n"
                f"Space Complexity: {algo['space_complexity']}\n\n"
                f"Description:\n{algo['description']}"
            )
        return f"No description available for '{name}'."

    def list_algorithms(self):
        # returns a list of all supported algorithm names
        return sorted(self.algorithms.keys())



    # UI popup

    def show_popup(self, master=None):
        # displays algorithm descriptions in scrollable popup window
        popup = tk.Toplevel(master)
        popup.title("Standard Algorithm Descriptions")
        popup.geometry("800x600")

        # scrollable frame setup
        frame = ttk.Frame(popup)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # title
        ttk.Label(scrollable_frame, text="Standard Algorithm Reference", font=("Segoe UI", 14, "bold")).pack(pady=(0, 10))

        # algorithm descriptions
        for name in self.list_algorithms():
            algo = self.algorithms[name]
            section = ttk.Frame(scrollable_frame)
            section.pack(fill="x", pady=5)
            ttk.Label(section, text=f"{name}", font=("Segoe UI", 11, "bold")).pack(anchor="w")
            ttk.Label(section, text=f"Category: {algo['category']}", font=("Segoe UI", 9, "italic"), foreground="#555").pack(anchor="w")
            ttk.Label(section, text=f"Time: {algo['time_complexity']}   Space: {algo['space_complexity']}", font=("Consolas", 9)).pack(anchor="w")
            ttk.Label(section, text=algo['description'], wraplength=760, font=("Segoe UI", 10), justify="left").pack(anchor="w", pady=(0, 5))
