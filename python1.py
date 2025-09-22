
# python1.py
import boto3
import json

# Initialize EC2 client
ec2 = boto3.client("ec2", region_name="us-east-1")

def get_untagged_instances():
    response = ec2.describe_instances()
    untagged = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]

            # Get tags (if any)
            tags = {t["Key"]: t["Value"] for t in instance.get("Tags", [])}

            if "Name" not in tags:
                untagged.append(instance_id)

    return untagged


if __name__ == "__main__":
    untagged_instances = get_untagged_instances()

    if untagged_instances:
        print("❌ Untagged Instances Found:")
        for inst in untagged_instances:
            print(f" - {inst}")
    else:
        print("✅ All instances have Name tags")

    # Save to JSON file
    with open("untagged_instances.json", "w") as f:
        json.dump(untagged_instances, f, indent=2)
