import math
import json
from take_input import get_data


# Helper function - get list of neighbors for each vertex, and remove duplicates by making into a set
def get_neighbors(kind):
    return set([x for x in kind if isinstance(x, str)])

# Main function for analyzing
def analyze_vertices(input:str):
    data = get_data(input)
    vertices = data['vertex-data']
    classifications = {}

    # Make hash table of coordinates 
    coords = {}
    for v in vertices:
        coords[v["id"]]=v["coords"]

    for v in vertices: 
        x1, y1 = v["coords"]
        neighbors = get_neighbors(v["kind-list"])

        angles = []
        for n in neighbors:
            x2, y2 = coords[n]
            dx, dy = x2 - x1, y2-y1
            angle = math.atan2(dy, dx)
            angle_degree = math.degrees(angle)
            angles.append(angle_degree)

        angles.sort()

        #Compute angular differences
        differences = []
        for i in range(len(angles)):
            j = (i+1) % len(angles)
            difference = (angles[j] - angles[i]) % 360
            differences.append(difference)

        #Classifying vertices
        if len(neighbors) == 2:
            classifications[v["id"]]="L" #corner with 2 lines
        elif len(neighbors) == 3:
            max_angle = max(differences)
            if any(abs(d-180) < 10 for d in differences):
                classifications[v["id"]]="T"
            elif max_angle > 180:
                classifications[v["id"]]="Arrow"
            else:
                classifications[v["id"]]="Fork"

    return classifications


def main():
    print(analyze_vertices("cube.json"))
    print(analyze_vertices('one.json'))

if __name__ == '__main__':
    main()
