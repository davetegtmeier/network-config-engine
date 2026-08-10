from pathlib import Path

import yaml


def load_external_endpoints(filepath: Path):
    with filepath.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return data["external_endpoints"]


if __name__ == "__main__":
    external_endpoints_file = Path("data/external_endpoints.yaml")
    external_endpoints = load_external_endpoints(external_endpoints_file)

    print(external_endpoints)

