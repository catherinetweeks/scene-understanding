import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

from vertex_analysis import analyze_vertices, write_analysis
from region_linking import link_regions, get_vertex_regions
from region_grouping import group_regions, format_body_output

class SceneUnderstanding:
    """Pipeline for scene understanding process"""
    def __init__(self, input_file: str = "cube.json"):
        self.input_file = input_file
        self.background = None
        self.vertex_types = {}
        self.region_links = []
        self.bodies = []

    def run_pipeline(self, visualize: bool = False) -> None:
        """Execute full scene analysis pipeline"""
        print(f"\nProcessing {self.input_file}...")
        print("=" * 50)

        # Vertex Analysis
        print("\n Analyzing vertices...")
        self.vertex_types = analyze_vertices(self.input_file)
        write_analysis(self.vertex_types)
        print("✓ Vertex analysis complete")

        # Region Linking
        print("\n Linking regions...")
        regions = get_vertex_regions(self.input_file)
        self.region_links = link_regions(
            self.vertex_types, 
            regions,
            input_file=self.input_file
        )
        print("✓ Region linking complete")

        # Region Grouping and Output
        print("\n Grouping regions and generating output...")
        with open(self.input_file) as f:
            self.background = json.load(f)["background"]
        self.bodies = group_regions(self.region_links, self.background)
        format_body_output(self.bodies)
        print("✓ Region grouping complete")

        if visualize:
            self.visualize_results()

    def visualize_results(self) -> None:
        """Generate visualizations if networkx is available"""
        try:
            import networkx as nx
            import matplotlib.pyplot as plt

            # Create graph
            G = nx.Graph()
            for r1, r2, via in self.region_links:
                if r1 != self.background and r2 != self.background:
                    G.add_edge(r1, r2, label=via)

            # Draw graph
            plt.figure(figsize=(10, 8))
            pos = nx.spring_layout(G)
            nx.draw(G, pos, with_labels=True, node_color='lightblue',
                   font_weight='bold', node_size=1000)

            # Add edge labels
            edge_labels = nx.get_edge_attributes(G, 'label')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

            plt.title(f"Region Connections - {Path(self.input_file).stem}")
            plt.show()

        except ImportError:
            print("\n  Visualization requires networkx and matplotlib")
            print("   Install with: pip install networkx matplotlib")

def main():
    """Command line interface for scene understanding pipeline"""
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Scene Understanding Pipeline")
    parser.add_argument('input', nargs='?', default='cube.json',
                       help='Input JSON file (default: cube.json)')
    parser.add_argument('--visualize', '-v', action='store_true',
                       help='Show region graph visualization')
    args = parser.parse_args()

    # Run pipeline
    pipeline = SceneUnderstanding(args.input)
    try:
        pipeline.run_pipeline(args.visualize)
    except Exception as e:
        print(f"\n Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()