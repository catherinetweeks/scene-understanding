from typing import Dict, List, Set, Tuple
from collections import defaultdict
import json
from region_linking import load_vertex_analysis, get_vertex_regions, link_regions

class Nucleus:
    """A group of regions that may form part of the same 3D body"""
    def __init__(self, regions: Set[int]):
        self.regions = set(regions)
        self.links = defaultdict(int)  # {nucleus: link_count}
    
    def __str__(self) -> str:
        """String representation of nucleus"""
        return f"Nucleus(regions={sorted(self.regions)})"
    
    def merge_with(self, other: 'Nucleus') -> None:
        """Merge another nucleus into this one and update all links"""
        # Save regions before merging
        other_regions = sorted(other.regions)
        self_regions = sorted(self.regions)
        
        # Merge regions
        self.regions.update(other.regions)
        
        # Update links, excluding the nucleus being merged
        for nucleus, count in list(other.links.items()):
            if nucleus != self:
                self.links[nucleus] += count
                nucleus.links[self] = self.links[nucleus]
                # Clean up old links
                if other in nucleus.links:
                    del nucleus.links[other]
        
        print(f"  Merged regions {other_regions} into {self_regions}")

def global_stage(nuclei: Dict[int, Nucleus]) -> None:
    """GLOBAL stage: Merge nuclei with ≥2 strong links"""
    print("\nGLOBAL Stage:")
    while True:
        merged = False
        nucleus_list = list(nuclei.values())
        
        # Look for nuclei pairs with ≥2 links
        for i, n1 in enumerate(nucleus_list):
            for n2 in nucleus_list[i+1:]:
                if n1.links[n2] >= 2:
                    print(f"Found {n1.links[n2]} links between nuclei:")
                    n1.merge_with(n2)
                    
                    # Update nuclei dictionary
                    for region in n2.regions:
                        nuclei[region] = n1
                    
                    merged = True
                    break
            if merged:
                break
                
        if not merged:
            break

def singlebody_stage(nuclei: Dict[int, Nucleus]) -> None:
    """SINGLEBODY stage: Merge single regions with one link to multi-region nuclei"""
    print("\nSINGLEBODY Stage:")
    while True:
        merged = False
        unique_nuclei = list(set(nuclei.values()))
        
        # First, find pairs of single-region nuclei that should merge
        single_region_pairs = []
        for i, n1 in enumerate(unique_nuclei):
            if len(n1.regions) == 1:
                for n2 in unique_nuclei[i+1:]:
                    if len(n2.regions) == 1 and n1.links[n2] > 0:
                        single_region_pairs.append((n1, n2))
        
        # Merge pairs of single regions first
        if single_region_pairs:
            n1, n2 = single_region_pairs[0]
            print(f"Merging single regions {sorted(n1.regions)} and {sorted(n2.regions)}")
            n1.merge_with(n2)
            for region in n2.regions:
                nuclei[region] = n1
            merged = True
        
        # Then handle single regions connecting to multi-region nuclei
        if not merged:
            for nucleus in unique_nuclei:
                if len(nucleus.regions) == 1:
                    # Find connected multi-region nuclei
                    connected = [n for n in nucleus.links.keys() 
                               if nucleus.links[n] > 0 and len(n.regions) > 1]
                    
                    if len(connected) == 1:
                        target = connected[0]
                        print(f"Merging single region {sorted(nucleus.regions)} "
                              f"into {sorted(target.regions)}")
                        target.merge_with(nucleus)
                        
                        for region in nucleus.regions:
                            nuclei[region] = target
                        
                        merged = True
                        break
        
        if not merged:
            break

def validate_input(links: List[Tuple[int, int, str]], background: int) -> None:
    """Validate input data before processing"""
    if not links:
        raise ValueError("No region links provided")
    if background is None:
        raise ValueError("Background region not specified")

def print_link_summary(links: List[Tuple[int, int, str]]) -> None:
    """Print all links for debugging"""
    print("\n=== LINK SUMMARY ===")
    for r1, r2, via in links:
        print(f"  {r1} <-> {r2} via vertex {via}")
    print("=====================")

def group_regions(links: List[Tuple[int, int, str]], background: int) -> List[Set[int]]:
    """Group regions into bodies using GLOBAL and SINGLEBODY stages"""
    # Initialize one nucleus per region (excluding background)
    nuclei = {}  # {region_number: Nucleus}
    for r1, r2, _ in links:
        if r1 != background and r1 not in nuclei:
            nuclei[r1] = Nucleus({r1})
        if r2 != background and r2 not in nuclei:
            nuclei[r2] = Nucleus({r2})
    
    # Record links between nuclei (excluding background)
    for r1, r2, _ in links:
        if r1 != background and r2 != background:
            n1, n2 = nuclei[r1], nuclei[r2]
            if n1 != n2:
                n1.links[n2] += 1
                n2.links[n1] += 1
    
    # Run grouping stages
    global_stage(nuclei)
    singlebody_stage(nuclei)
    
    # Return unique sets of regions forming bodies
    return [n.regions for n in set(nuclei.values())]

def format_body_output(bodies: List[Set[int]]) -> None:
    print("\nScene Analysis Results:")
    print("----------------------")
    for i, regions in enumerate(bodies, 1):
        sorted_regions = sorted(regions)
        print(f"BODY {i}: regions {sorted_regions}")
    print("----------------------")