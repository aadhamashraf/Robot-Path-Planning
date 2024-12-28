# src/core/frontier_exporter.py
import re


class FrontierExporter:
    def __init__(self, output_dir="frontiers"):
        self.output_dir = output_dir
        import os
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def export_frontier(self, frontier, algorithm_name):
        # Sanitize the algorithm_name to remove invalid characters
        sanitized_name = re.sub(r'[^\w\s-]', '', algorithm_name)
        sanitized_name = sanitized_name.replace(" ", "_")
        filename = f"{self.output_dir}/{sanitized_name}_frontier.txt"
        with open(filename, "w") as f:
            f.write(str(frontier))
