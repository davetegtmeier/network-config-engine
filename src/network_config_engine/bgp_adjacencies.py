from pathlib import Path

import csv


def load_bgp_adjacencies(filepath: Path):
    with open(filepath, mode='r', encoding='utf-8-sig') as file:
        bgp_adjacencies = []
        reader = csv.DictReader(file)
        for adjacency in reader:
            bgp_adjacencies.append(adjacency)

    return bgp_adjacencies


if __name__ == "__main__":
    bgp_adjacencies_file = Path("data/bgp_adjacencies.csv")
    bgp_adjacencies = load_bgp_adjacencies(bgp_adjacencies_file)

    print(bgp_adjacencies)
