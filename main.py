from region_grouping import *

def main():
    """Main execution flow"""
    import sys
    input_file = "one.json"
    
    # Load input data
    with open(input_file) as f:
        data = json.load(f)
        background = data["background"]
    
    # Get region links from region_linking 
    vertex_types = load_vertex_analysis()
    regions = get_vertex_regions(input_file)
    links = link_regions(vertex_types, regions)
    
    # Validate input
    validate_input(links, background)
    
    # Group regions into bodies
    bodies = group_regions(links, background)
    
    # Format and output results
    format_body_output(bodies)

if __name__ == "__main__":
    main()