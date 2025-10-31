import json

def get_data(filename:str="cube.json"):
    # Load and parse the JSON file Load and para the JSON file 
    print("Loading file...")
    with open(filename, "r") as f:
        data = json.load(f)

    # # Print the entire structure to understand its contents
    # print("JSON Data Structure:")
    # print(json.dumps(data, indent=2))

    # # Extract main components from the JSON data 
    # print("\nExtracting components...")
    # vertices = data.get("VERTICES", {})
    # regions = data.get("REGIONS", {})
    # kind_lists = data.get("KINDLISTS", {})

    # #Prints the vertices and their coordinates
    # print("\nVertices and their coordinates:")
    # for vertex, coords in vertices.items():
    #     print(f"Vertex {vertex}: {coords}")

    # #Prints the region and its associated information
    # print("\nRegions and their information:")
    # for region, info in regions.items():
    #     print(f"Region {region}: {info}")


    # #Prints the kind lists associated with each vertex
    # for vertex, kind in kind_lists.items():
    #     print(f"Vertex {vertex}: {kind}")

    return data