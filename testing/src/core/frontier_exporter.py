# src/core/frontier_exporter.py
class FrontierExporter:
    def __init__(self, output_dir="frontiers"):
        self.output_dir = output_dir
        import os
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def export_frontier(self, frontier, algorithm_name):
       # print(f"Exporting frontier for {algorithm_name}")
        filename = f"{self.output_dir}/{algorithm_name}_frontier.txt"
        with open(filename, "w") as f:
            f.write(str(frontier))
