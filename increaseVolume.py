import boto3

def list_gp3_volumes(region):
    ec2 = boto3.client('ec2', region_name=region)
    paginator = ec2.get_paginator('describe_volumes')
    volumes = []

    for page in paginator.paginate(Filters=[{'Name': 'volume-type', 'Values': ['gp3']}]):
        for volume in page['Volumes']:
            volumes.append((volume['VolumeId'], volume['Size']))

    return volumes

def expand_volume(region, volume_id, new_size):
    ec2 = boto3.client('ec2', region_name=region)
    ec2.modify_volume(VolumeId=volume_id, Size=new_size)

def main():
    region = 'us-east-1'  # 替换为你的区域名
    volumes = list_gp3_volumes(region)

    for volume_id, size in volumes:
        new_size = int(size * 1.2)  # 扩展 20%
        expand_volume(region, volume_id, new_size)
        print(f"Expanded volume {volume_id} from {size} GB to {new_size} GB")

if __name__ == "__main__":
    main()