# Scene Understanding System

A Python implementation of a 3D scene understanding system that analyzes line drawings to identify distinct bodies and their relationships.

## Overview

This system processes line drawings through several stages:
1. Input Parsing - Extracts vertices, regions, and relationships
2. Vertex Analysis - Classifies vertices as L, Fork, Arrow, or T junctions
3. Region Linking - Establishes connections between regions
4. Region Grouping - Groups regions into 3D bodies
5. Output Generation - Displays identified bodies and their regions

## Getting Started

### Prerequisites
```bash
pip install networkx matplotlib
```

### Running the System
1. Run vertex analysis:
```bash
python3 vertex_analysis.py
```

2. Run region linking and grouping:
```bash
python3 region_grouping.py cube.json  # or one.json
```

## Quick Start

The easiest way to run the complete scene understanding pipeline is:

```bash
python3 scene_pipeline.py cube.json    # Process cube scene
python3 scene_pipeline.py one.json     # Process one scene
python3 scene_pipeline.py --visualize  # Show region graph visualization
```

Command line options:
- First argument: Input JSON file (default: cube.json)
- `--visualize` or `-v`: Show interactive region graph visualization

Example usage:
```bash
# Basic analysis
python3 scene_pipeline.py cube.json

# Analysis with visualization
python3 scene_pipeline.py one.json --visualize
```

## File Structure

- [`take_input.py`](take_input.py) - Handles JSON input file parsing
- [`vertex_analysis.py`](vertex_analysis.py) - Classifies vertices based on geometry
- [`region_linking.py`](region_linking.py) - Creates links between regions
- [`region_grouping.py`](region_grouping.py) - Groups regions into 3D bodies

### Input Files
- [`cube.json`](cube.json) - Simple cube example
- [`one.json`](one.json) - More complex scene example

## Implementation Details

### Vertex Types
- **L**: Two lines meeting at a corner
- **Fork**: Three lines meeting with all angles < 180°
- **Arrow**: Three lines meeting with one angle > 180°
- **T**: Three lines meeting with two collinear

### Region Grouping Rules
1. **GLOBAL Stage**: 
   - Merges nuclei with ≥2 strong links
   - Excludes background region

2. **SINGLEBODY Stage**:
   - Merges single regions with exactly one link to multi-region nuclei
   - Only merges if target nucleus has multiple regions

## Example Output

### Cube Scene
```
Scene Analysis Results:
----------------------
BODY 1: regions [1, 2, 3]
----------------------
```

### One Scene
```
Scene Analysis Results:
----------------------
BODY 1: regions [1, 2]
BODY 2: regions [3, 4, 5]
----------------------
```

## Visualization

The system includes two visualization methods:
1. ASCII visualization of region links
2. Network graph visualization using networkx (optional)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/NewFeature`)
3. Commit your changes (`git commit -am 'Add NewFeature'`)
4. Push to the branch (`git push origin feature/NewFeature`)
5. Create a new Pull Request

## License

This project is available under the MIT License.