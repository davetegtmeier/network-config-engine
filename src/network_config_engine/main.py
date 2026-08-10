from pathlib import Path

from sites import load_sites
from inventory import load_inventory
from router_vrfs import load_router_vrfs
from external_endpoints import load_external_endpoints
from bgp_adjacencies import load_bgp_adjacencies

if __name__ == "__main__":
    sites_file = Path("data/sites.yaml")
    inventory_file = Path("data/inventory.csv")
    router_vrfs_file = Path("data/router_vrfs.csv")
    external_endpoints_file = Path("data/external_endpoints.yaml")
    bgp_adjacencies_file = Path("data/bgp_adjacencies.csv")

    sites = load_sites(sites_file)
    inventory = load_inventory(inventory_file)
    router_vrfs = load_router_vrfs(router_vrfs_file)
    external_endpoints = load_external_endpoints(external_endpoints_file)
    bgp_adjacencies = load_bgp_adjacencies(bgp_adjacencies_file)

    inventory_hostnames = set()
    inventory_ip_addresses = set()

    # Validate each router in the inventory.
    for router in inventory:
        site_found = False

        inventory_hostname = router["hostname"].strip().upper()
        ip_address = router["ip_address"].strip()

        # Check for duplicate hostnames.
        if inventory_hostname in inventory_hostnames:
            print(f"Duplicate hostname: {inventory_hostname}")
        else:
            inventory_hostnames.add(inventory_hostname)

        # Check for duplicate IP addresses.
        if ip_address in inventory_ip_addresses:
            print(f"Duplicate IP address: {inventory_hostname} - {ip_address}")
        else:
            inventory_ip_addresses.add(ip_address)

        # Find the router's site and validate its zone.
        for site_code in sites:
            if inventory_hostname.startswith(site_code):
                site_found = True

                zone = router["zone"].strip().upper()
                site_data = sites[site_code]

                if zone in site_data["zones"]:
                    print(f"{inventory_hostname} -> {site_code} ({zone})")
                else:
                    print(f"{zone} is not a valid zone for {site_code}")

                break

        # Report routers that do not match any known site.
        if not site_found:
            print(f"{inventory_hostname} does not match a known site")

    # Validate router VRF hostnames against the inventory.
    router_vrf_pairs = set()
    
    for router_vrf in router_vrfs:
        vrf_hostname = router_vrf["hostname"].strip().upper()
        vrf_name = router_vrf["vrf"].strip().upper()
        
        if vrf_hostname not in inventory_hostnames:
            print(f"{vrf_hostname} does not exist in the inventory")

        if not vrf_name:
            print(f"{vrf_hostname} has a blank VRF")

        router_vrf_pair = (vrf_hostname, vrf_name)

        if router_vrf_pair in router_vrf_pairs:
            print(f"Duplicate router/VRF relationship: {vrf_hostname} - {vrf_name}")
        else:
            router_vrf_pairs.add(router_vrf_pair)
            print(router_vrf_pair)

    for adjacency in bgp_adjacencies:
        endpoint1 = adjacency["endpoint1"].strip().upper()
        endpoint2 = adjacency["endpoint2"].strip().upper()
        vrf = adjacency["vrf"].strip().upper()

        if endpoint1 == endpoint2:
            print(f"Cannot create a BGP adjacency: {endpoint1} cannot peer with itself")

        if endpoint1 not in inventory_hostnames and endpoint1 not in external_endpoints:
            print(f"Cannot create a BGP adjacency: {endpoint1} is not a valid host")

        if endpoint2 not in inventory_hostnames and endpoint2 not in external_endpoints:
            print(f"Cannot create a BGP adjacency: {endpoint2} is not a valid host")

        if vrf:
            if endpoint1 in inventory_hostnames:
                endpoint1_vrf = (endpoint1, vrf)

                if endpoint1_vrf not in router_vrf_pairs:
                    print(f"{endpoint1} does not have VRF {vrf}")

            if endpoint2 in inventory_hostnames:
                endpoint2_vrf = (endpoint2, vrf)

                if endpoint2_vrf not in router_vrf_pairs:
                    print(f"{endpoint2} does not have VRF {vrf}")
        
                