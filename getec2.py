import boto3
def getcpunumber(region):
    ec2 = boto3.client('ec2',region_name=region)

    reservations = ec2.describe_instances(MaxResults=100)['Reservations']
    print()
    vcpus = 0
   # instances=[]
    cmdb_servers_info = {}
    for reservation in reservations:
        
        for instance in reservation['Instances']:
            server_host = instance['PrivateIpAddress']
            server_name=''
            for tag in instance['Tags']:
                if tag['Key'] == 'Name':
                    consoleName = tag['Value']
            instance_id = instance['InstanceId']
            instance_type_name = instance['InstanceType']
            instance_type = ec2.describe_instance_types(InstanceTypes=[instance_type_name])
            current_vcpu_count = instance_type['InstanceTypes'][0]['VCpuInfo']['DefaultVCpus']
            current_memory = instance_type['InstanceTypes'][0]['MemoryInfo']['SizeInMiB']
            os_type = instance['PlatformDetails']
            # private_ip = instance['PrivateIpAddress']
            cmdb_servers_info[server_host] = {
                    "server_name": server_name,
                    "salt_minion_id": instance_id,
                    "mem_total": str(round(int(current_memory) / 1024)) + "G",
                    "num_cpus": int(current_vcpu_count),
                    "server_kernel": os_type,
                    "server_cloud": "aws",
                    "server_cloud_region": 'us-east-1'
                }
            
           
           # print(f"server_name: {server_name} -- server_host: {server_host}")
    #        print(f'{cmdb_servers_info[server_host][server_name]} - {cmdb_servers_info[server_host][salt_minion_id]} - {cmdb_servers_info[server_host][mem_total]} - {cmdb_servers_info[server_host][num_cpus]} - {cmdb_servers_info[server_host][server_kernel]} - {cmdb_servers_info[server_host][server_cloud]} - {cmdb_servers_info[server_host][server_cloud_region]}')
 #           print(f'{server_name} - {salt_minion_id} - {mem_total} - {cmdb_servers_info[server_host][num_cpus]} - {cmdb_servers_info[server_host][server_kernel]} - {cmdb_servers_info[server_host][server_cloud]} - {cmdb_servers_info[server_host][server_cloud_region]}')

        #    print(f'{instance_id} - {instance_type_name} - {current_vcpu_count} - {current_memory/1024} - {server_name} - {os_type} - { server_host}')
            #vcpus += current_vcpu_count
           # instances.append(instance_id,current_vcpu_count,current_memory)
    
    #print(vcpus)
    for info in cmdb_servers_info:
        print(info["server_name"])
        #print(f'{info.server_name} - {info.salt_minion_id} - {info.mem_total} - {info.num_cpus} - {info.server_kernel} - {info.server_cloud} - {info.server_cloud_region}')

    #return instances

def getcpunumber0(region):
    ec2 = boto3.client('ec2',region_name=region)

    reservations = ec2.describe_instances(MaxResults=100)['Reservations']
    print()
    vcpus = 0
   # instances=[]
    for reservation in reservations:
        for instance in reservation['Instances']:
            consoleName=''
            for tag in instance['Tags']:
                if tag['Key'] == 'Name':
                    consoleName = tag['Value']
            instance_id = instance['InstanceId']
            instance_type_name = instance['InstanceType']
            instance_type = ec2.describe_instance_types(InstanceTypes=[instance_type_name])
            current_vcpu_count = instance_type['InstanceTypes'][0]['VCpuInfo']['DefaultVCpus']
            current_memory = instance_type['InstanceTypes'][0]['MemoryInfo']['SizeInMiB']
            os_type = instance['PlatformDetails']
            private_ip = instance['PrivateIpAddress']
            print(f'{instance_id} - {instance_type_name} - {current_vcpu_count} - {current_memory/1024} - {consoleName} - {os_type} - { private_ip}')
            #vcpus += current_vcpu_count
           # instances.append(instance_id,current_vcpu_count,current_memory)
    
    #print(vcpus)
    #return instances
def getmemsize(region):
    #details = client.describe_instance_types( InstanceTypes=[ type ] )
    #memory = details['InstanceTypes']['MemoryInfo']['SizeInMiB']
    return '1024'

def listec2(region):
    ec2 = boto3.client('ec2',region_name=region)
    paginator = ec2.get_paginator('describe_instances')
    #response = ec2.describe_instances()
    instances = []

            
    inst_types = []
    it_paginator = ec2.get_paginator('describe_instance_types')
    for page in it_paginator.paginate():
        print(page['InstanceTypes'])
        

    return instances


def main():
    region = 'us-east-1'  # 替换为你的区域名
#    instances = listec2(region)
#    for ec2 in instances:
#        print(ec2)
    getcpunumber(region)
   # for ec2 in result:
    #    print(ec2)
        
if __name__ == "__main__":
    main()  
    