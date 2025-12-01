import matplotlib.pyplot as plt
import matplotlib.ticker as ticker      # used to format x-axis tick marks
import os                              # used for file checking when loading graphs

class GraphDisplayer:
    def __init__(self):
        self.figure, self.ax = plt.subplots(figsize=(10, 6))  # creates a new figure and axes
        self.graph_data = None        # stores plotted data (x, y) for later use
        self.complexity_label = None  # stores algorithm complexity label

    def create_graph(self, timing_data, complexity_label="O(n)"):
        # input sizes (x) and runtimes (y) data points
        x = timing_data[:, 0].astype(float)  # input sizes
        y = timing_data[:, 1].astype(float)  # runtimes

        # checks for empty or invalid data
        if x.size == 0 or y.size == 0:
            print("No valid timing data to display.")
            return

        self.ax.clear()  # clears previous graph

        # plots the data as a blue line with circle markers
        self.ax.plot(x, y, color="royalblue", linewidth=2, marker="o", label="Measured Runtime")

        # adds title and shows estimated algorithm complexity
        self.ax.set_title(
            f"Algorithm Runtime Performance\nEstimated Complexity: {complexity_label}",
            fontsize=14, fontweight="bold"
        )

        # labels both axes
        self.ax.set_xlabel("Input Size (n)")
        self.ax.set_ylabel("Execution Time (nanoseconds)")

        # ensures x-axis ticks are integers for readability
        self.ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        # adds dashed grid for readability
        self.ax.grid(True, linestyle="--", alpha=0.6)

        # displays legend with "Measured Runtime" label
        self.ax.legend()

        # saves the data and label for later use
        self.graph_data = (x, y)
        self.complexity_label = complexity_label

        # adjusts spacing to avoid overlapping labels and shows the graph
        self.figure.tight_layout()
        plt.show()

    def save_graph(self, file_path="runtime_graph.png"):
        if self.graph_data is None:
            print("No graph available to save.")
            return

        try:
            # saves the current figure as a PNG image
            self.figure.savefig(file_path)
            print(f"Graph saved successfully to '{file_path}'")
        except Exception as e:
            # catches errors while saving
            print(f"Error saving graph: {e}")

    @staticmethod
    def load_graph(file_path):
        if not os.path.exists(file_path):
            print("Graph file not found.")
            return

        # reads the saved image and displays it in a new window
        img = plt.imread(file_path)
        plt.figure(figsize=(8, 6))
        plt.imshow(img)
        plt.axis("off")  # hides axes
        plt.title("Loaded Runtime Graph", fontsize=13, fontweight="bold")
        plt.show()

    def clear_graph(self):
        self.ax.clear()  # clears the existing plot
        plt.close(self.figure)  # closes the current figure window
        self.figure, self.ax = plt.subplots(figsize=(10, 6))  # recreates figure and axes
        self.graph_data = None
        self.complexity_label = None
        print("Graph cleared.")
