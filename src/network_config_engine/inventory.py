from pathlib import Path

import csv


def load_inventory(filepath: Path):
    with open(filepath, mode="r", encoding="utf-8-sig") as file:
        inventory = []
        reader = csv.DictReader(file)

        for router in reader:
            inventory.append(router)

    return inventory


if __name__ == "__main__":
    inventory_file = Path("data/inventory.csv")
    inventory = load_inventory(inventory_file)

    print(inventory)