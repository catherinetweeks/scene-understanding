import json
from pathlib import Path
from typing import Dict, List, Tuple, Set

# Each vertex connects certain regions (from the KIND list)
vertex_regions = {
    "A": [1, 2],
    "B": [1, 2, 3],
    "C": [3, 4, 5],
    "D": [2, 4, 6]
}

# --- Helper functions ---

def all_unique_pairs(regions):
    """Generate all unique pairs of regions for a vertex"""
    pairs = []
    for i in range(len(regions)):
        for j in range(i + 1, len(regions)):
            pairs.append((regions[i], regions[j]))
    return pairs

def add_link(links, r1, r2, via):
    """Record a bidirectional region link"""
    if (r1, r2) not in links and (r2, r1) not in links:
        links.append((r1, r2, via))

def load_vertex_analysis(filename: str = "vertex_analysis_output.json") -> Dict[str, str]:
    """
    Load vertex analysis results from step 2
    Expected format from vertex_analysis.py:
    {
        "A": "L",
        "B": "Fork",
        "C": "Arrow",
        ...
    }
    """
    try:
        filepath = Path(__file__).parent / filename
        with open(filepath) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Could not find {filename}, using test data instead")
        return vertex_types  # Fall back to test data

def calculate_angle(point1, point2, center):
    """Calculate angle between two points around a center point"""
    import math
    
    x1, y1 = point1[0] - center[0], point1[1] - center[1]
    x2, y2 = point2[0] - center[0], point2[1] - center[1]
    
    angle = math.degrees(math.atan2(y2, x2) - math.atan2(y1, x1))
    return angle if angle >= 0 else angle + 360

def process_arrow_vertex(regions, angles):
    """Process Arrow vertex to find smallest angle regions"""
    if len(regions) < 3:
        return None
        
    # Find two regions with smallest angle
    sorted_angles = sorted(enumerate(angles), key=lambda x: x[1])
    r1, r2 = regions[sorted_angles[0][0]], regions[sorted_angles[1][0]]
    return (r1, r2)

def log_vertex_processing(vertex_id, vtype, links_made):
    """Log vertex processing details"""
    print(f"\nProcessing vertex {vertex_id} ({vtype}):")
    if links_made:
        print("Links created:")
        for r1, r2 in links_made:
            print(f"  Region {r1} <-> Region {r2}")
    else:
        print("  No links created")

def validate_vertex_data(vertex_types, vertex_regions):
    """Validate vertex input data"""
    if not set(vertex_types.keys()) == set(vertex_regions.keys()):
        raise ValueError("Vertex type and region keys don't match")
    
    valid_types = {"L", "Fork", "Arrow", "T"}
    for vtype in vertex_types.values():
        if vtype not in valid_types:
            raise ValueError(f"Invalid vertex type: {vtype}")

# --- Main linking function ---

def link_regions(vertex_types: Dict[str, str], 
                vertex_regions: Dict[str, List[int]]) -> List[Tuple[int, int, str]]:
    """
    Link regions based on vertex types and their connecting regions.
    
    Args:
        vertex_types: Dictionary mapping vertex IDs to their types (L, Fork, Arrow, T)
        vertex_regions: Dictionary mapping vertex IDs to lists of connected region IDs
    
    Returns:
        List of tuples (region1, region2, vertex) representing linked regions
    """
    links = []
    
    # Validate vertex types
    valid_types = {"L", "Fork", "Arrow", "T"}
    invalid_types = set(vertex_types.values()) - valid_types
    if invalid_types:
        raise ValueError(f"Invalid vertex types found: {invalid_types}")

    for vertex, vtype in vertex_types.items():
        regions = vertex_regions.get(vertex, [])
        
        # Validate minimum regions for each type
        min_regions = {"L": 2, "Fork": 3, "Arrow": 3, "T": 3}
        if len(regions) < min_regions[vtype]:
            print(f"Warning: Vertex {vertex} has fewer regions than expected for type {vtype}")
            continue

        links_made = []

        if vtype == "L":
            # Two regions meet — typically a boundary, not a shared surface
            continue

        elif vtype == "Fork":
            # Link all region pairs (they share a 3-way connection)
            for (r1, r2) in all_unique_pairs(regions):
                add_link(links, r1, r2, vertex)
                links_made.append((r1, r2))

        elif vtype == "Arrow":
            # Find the two regions with smallest angle
            # For now using first two regions, but could be improved with angle calculations
            if len(regions) >= 3:
                # Link first two regions as they form the arrow point
                add_link(links, regions[0], regions[1], vertex)
                links_made.append((regions[0], regions[1]))
                # Optionally link arrow point to shaft region
                add_link(links, regions[1], regions[2], vertex)
                links_made.append((regions[1], regions[2]))

        elif vtype == "T":
            # Occlusion — typically no region linking
            continue

        log_vertex_processing(vertex, vtype, links_made)

    return links

def visualize_links(links: List[Tuple[int, int, str]]) -> None:
    """Create a simple ASCII visualization of region links."""
    from collections import defaultdict
    
    # Group links by vertex
    vertex_links = defaultdict(list)
    for r1, r2, v in links:
        vertex_links[v].append((r1, r2))
    
    print("\nRegion Link Visualization:")
    for vertex, region_pairs in vertex_links.items():
        print(f"\nVertex {vertex}:")
        for r1, r2 in region_pairs:
            print(f"  {r1} <---> {r2}")

def test_link_regions():
    """Test the region linking functionality."""
    test_types = {
        "V1": "Fork",
        "V2": "Arrow",
        "V3": "L"
    }
    test_regions = {
        "V1": [1, 2, 3],
        "V2": [2, 3, 4],
        "V3": [3, 4]
    }
    
    links = link_regions(test_types, test_regions)
    assert len(links) > 0, "Should create at least one link"

def get_vertex_regions(filename: str) -> Dict[str, List[int]]:
    """Extract regions from KIND lists in input file"""
    try:
        with open(filename) as f:
            data = json.load(f)
        
        vertex_regions = {}
        for vertex in data['vertex-data']:
            regions = [x for x in vertex['kind-list'] if isinstance(x, int)]
            vertex_regions[vertex['id']] = regions
        return vertex_regions
    except FileNotFoundError:
        print(f"Warning: Could not find {filename}, using test data instead")
        return vertex_regions  # Fall back to test data

if __name__ == "__main__":
    # Run tests
    test_link_regions()
    
    # Load data from files
    input_file = "cube.json"  # or "one.json"
    vertex_classifications = load_vertex_analysis("vertex_analysis_output.json")
    regions = get_vertex_regions(input_file)
    
    # Run region linking
    linked_regions = link_regions(vertex_classifications, regions)
    visualize_links(linked_regions)
