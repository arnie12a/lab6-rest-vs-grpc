
#!/usr/bin/env python3

import argparse
import google.auth
from google.cloud import compute_v1

# VM configuration
MACHINE_TYPE = "e2-standard-2"

VMS = [
    {"name": "lab6-vm1", "zone": "us-west1-a"},
    {"name": "lab6-vm2", "zone": "us-west1-a"},
    {"name": "lab6-vm3", "zone": "europe-west3-a"},
]


def create_vm(project, snapshot, name, zone):
    print(f"\nCreating {name} in {zone}...")

    client = compute_v1.InstancesClient()

    # Boot disk restored from Lab 5 snapshot
    disk = compute_v1.AttachedDisk(
        boot=True,
        auto_delete=True,
        type_="PERSISTENT",
        initialize_params=compute_v1.AttachedDiskInitializeParams(
            source_snapshot=(
                f"projects/{project}/global/snapshots/{snapshot}"
            ),
            disk_type=f"zones/{zone}/diskTypes/pd-balanced",
        ),
    )

    # Default VPC, with external IP for convenient SSH
    network = compute_v1.NetworkInterface(
        network=f"projects/{project}/global/networks/default",
        access_configs=[
            compute_v1.AccessConfig(
                name="External NAT",
                type_="ONE_TO_ONE_NAT",
            )
        ],
    )

    vm = compute_v1.Instance(
        name=name,
        machine_type=f"zones/{zone}/machineTypes/{MACHINE_TYPE}",
        disks=[disk],
        network_interfaces=[network],
        tags=compute_v1.Tags(items=["lab6-server"]),
    )

    operation = client.insert(
        project=project,
        zone=zone,
        instance_resource=vm,
    )

    operation.result(timeout=300)

    created = client.get(
        project=project,
        zone=zone,
        instance=name,
    )

    internal_ip = created.network_interfaces[0].network_i_p

    print(f"Created: {name}")
    print(f"Zone: {zone}")
    print(f"Internal IP: {internal_ip}")

    return internal_ip


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--project",
        required=True,
        help="Google Cloud project ID",
    )

    parser.add_argument(
        "--snapshot",
        required=True,
        help="Existing Lab 5 snapshot name",
    )

    args = parser.parse_args()

    results = {}

    for vm in VMS:
        try:
            ip = create_vm(
                project=args.project,
                snapshot=args.snapshot,
                name=vm["name"],
                zone=vm["zone"],
            )
            results[vm["name"]] = ip

        except Exception as e:
            print(f"Failed to create {vm['name']}: {e}")

    print("\nVM Creation Summary")
    print("-" * 45)

    for name, ip in results.items():
        print(f"{name}: {ip}")


if __name__ == "__main__":
    main()
