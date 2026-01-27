#!/usr/bin/env python3
"""
Duplicate Path Analysis Script
==============================
Analyze the project for duplicate paths and naming patterns
"""

import json
import os
from collections import Counter, defaultdict
from pathlib import Path


def find_duplicate_directories(base_path, max_depth=3):
    """Find directories with the same name"""
    dir_counter = Counter()
    dir_locations = defaultdict(list)

    for root, dirs, files in os.walk(base_path):
        root_str = str(root)
        base_str = str(base_path)
        depth = root_str.count(os.sep) - base_str.count(os.sep)
        if depth > max_depth:
            continue

        for dir_name in dirs:
            # Skip cache and temporary directories
            if dir_name in ["__pycache__", ".git", "node_modules", ".pytest_cache"]:
                continue

            dir_counter[dir_name] += 1
            dir_locations[dir_name].append(root)

    return dir_counter, dir_locations


def analyze_structure(base_path):
    """Analyze project structure"""
    results = {
        "base_path": str(base_path),
        "analysis": {
            "duplicate_directories": {},
            "potential_duplicates": {},
            "unique_directories": {},
        },
    }

    # Find duplicates at different depth levels
    for max_depth in [1, 2, 3, 4]:
        dir_counter, dir_locations = find_duplicate_directories(base_path, max_depth)

        # Filter for duplicates (count > 1)
        duplicates = {name: count for name, count in dir_counter.items() if count > 1}

        if duplicates:
            results["analysis"]["potential_duplicates"][f"depth_{max_depth}"] = {
                "total_duplicates": len(duplicates),
                "directories": {
                    name: {
                        "count": count,
                        # Show first 5 locations
                        "locations": dir_locations[name][:5],
                    }
                    for name, count in sorted(
                        duplicates.items(), key=lambda x: x[1], reverse=True
                    )
                },
            }

    return results


def find_similar_paths(base_path, similarity_threshold=0.7):
    """Find paths with similar naming patterns"""
    from difflib import SequenceMatcher

    all_paths = []
    for root, dirs, files in os.walk(base_path):
        # Skip cache directories
        if "__pycache__" in root or ".git" in root or "node_modules" in root:
            continue

        for dir_name in dirs:
            if dir_name in ["__pycache__", ".git", "node_modules"]:
                continue
            all_paths.append((root, dir_name))

    # Find similar directory names
    similar_pairs = []
    checked = set()

    for i, (root1, name1) in enumerate(all_paths):
        for j, (root2, name2) in enumerate(all_paths):
            if i >= j:
                continue

            ratio = SequenceMatcher(None, name1.lower(), name2.lower()).ratio()
            if ratio > similarity_threshold and ratio < 1.0:
                key = tuple(sorted([name1, name2]))
                if key not in checked:
                    similar_pairs.append(
                        {
                            "name1": name1,
                            "location1": root1,
                            "name2": name2,
                            "location2": root2,
                            "similarity": ratio,
                        }
                    )
                    checked.add(key)

    return similar_pairs[:20]  # Return top 20 similar pairs


def main():
    """Main analysis function"""
    project_path = Path.cwd()
    print(f"Analyzing project: {project_path}")
    print("=" * 80)

    # Run structure analysis
    print("\n📊 Analyzing project structure...")
    results = analyze_structure(project_path)

    # Print duplicate directory analysis
    print("\n🔍 DUPLICATE DIRECTORY ANALYSIS")
    print("=" * 80)

    total_duplicates = 0
    for depth_key, depth_data in results["analysis"]["potential_duplicates"].items():
        print(f"\n{depth_key.upper()}:")
        print(f"  Total duplicates found: {depth_data['total_duplicates']}")
        total_duplicates += depth_data["total_duplicates"]

        # Show top 10 most duplicated directories
        top_duplicates = list(depth_data["directories"].items())[:10]
        for dir_name, info in top_duplicates:
            print(f"\n  📁 {dir_name} (found {info['count']} times)")
            for loc in info["locations"][:3]:
                rel_path = Path(loc).relative_to(project_path)
                print(f"     - {rel_path}")
            if info["count"] > 3:
                print(f"     ... and {info['count'] - 3} more locations")

    print(f"\n{'='*80}")
    print(f"TOTAL DUPLICATES ACROSS ALL DEPTHS: {total_duplicates}")

    # Find similar paths
    print("\n\n🔎 SIMILAR PATH ANALYSIS")
    print("=" * 80)
    similar_pairs = find_similar_paths(project_path)

    if similar_pairs:
        print(f"\nFound {len(similar_pairs)} similar directory name pairs:")
        for pair in similar_pairs:
            print(
                f"\n  {pair['name1']} ↔ {pair['name2']} (similarity: {pair['similarity']:.2%})"
            )
            print(
                f"    Location 1: {Path(pair['location1']).relative_to(project_path)}"
            )
            print(
                f"    Location 2: {Path(pair['location2']).relative_to(project_path)}"
            )
    else:
        print("\nNo similar directory names found.")

    # Save results to JSON
    output_file = project_path / "duplicate_paths_analysis.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*80}")
    print("✅ Analysis complete!")
    print(f"📄 Detailed results saved to: {output_file}")
    print(f"{'='*80}")

    return results


if __name__ == "__main__":
    main()
