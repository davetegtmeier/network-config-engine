from pathlib import Path

from sites import load_sites
from inventory import load_inventory


if __name__ == "__main__":
    sites_file = Path("data/sites.yaml")
    inventory_file = Path("data/inventory.csv")

    sites = load_sites(sites_file)
    inventory = load_inventory(inventory_file)

    seen_hostnames = set()
    seen_ip_addresses = set()

    # Validate each router in the inventory.
    for router in inventory:
        site_found = False

        hostname = router["hostname"].strip().upper()
        ip_address = router["ip_address"].strip()

        # Check for duplicate hostnames.
        if hostname in seen_hostnames:
            print(f"Duplicate hostname: {hostname}")
        else:
            seen_hostnames.add(hostname)

        # Check for duplicate IP addresses.
        if ip_address in seen_ip_addresses:
            print(f"Duplicate IP address: {hostname} - {ip_address}")
        else:
            seen_ip_addresses.add(ip_address)

        # Find the router's site and validate its zone.
        for site_code in sites:
            if hostname.startswith(site_code):
                site_found = True

                zone = router["zone"].strip().upper()
                site_data = sites[site_code]

                if zone in site_data["zones"]:
                    print(f"{hostname} -> {site_code} ({zone})")
                else:
                    print(f"{zone} is not a valid zone for {site_code}")

                break

        # Report routers that do not match any known site.
        if not site_found:
            print(f"{hostname} does not match a known site")