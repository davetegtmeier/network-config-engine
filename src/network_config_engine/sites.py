from pathlib import Path

import yaml


def load_sites(file_path: Path) -> dict:
    with file_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return data["sites"]

if __name__ == "__main__":
    sites_file = Path("data/sites.yaml")
    sites = load_sites(sites_file)

    for site_code, site_data in sites.items():
        print(site_code, site_data)
