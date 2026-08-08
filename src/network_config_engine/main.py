from pathlib import Path

from sites import load_sites
from inventory import load_inventory

if __name__ == "__main__":
    sites_file = Path("data/sites.yaml")
    inventory_file = Path("data/inventory.csv")

sites = load_sites(sites_file)
inventory = load_inventory(inventory_file)


for router in inventory:    
    for site_code in sites:
        if router["hostname"].startswith(site_code):
            zone = router["zone"].strip().upper()
            site_data = sites[site_code]
            if zone in site_data["zones"]:
                print(f"{router['hostname']} -> {site_code} ({zone})")
            else:
                print(f"{zone} is not a valid zone for {site_code}")
            
