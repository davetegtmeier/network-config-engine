from pathlib import Path
import csv

def load_router_vrfs(filepath: Path):
    with open(filepath, mode='r', encoding='utf-8-sig') as file:
        router_vrf = []
        reader = csv.DictReader(file)
        for vrf in reader:
            router_vrf.append(vrf)

    return router_vrf

if __name__ == "__main__":
    router_vrf_file = Path("data/router_vrfs.csv")
    router_vrf = load_router_vrfs(router_vrf_file)
