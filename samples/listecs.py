from datetime import datetime
from airflow.models import Variable

import pymongo
import math

from common.huaweicloud_api.ecs import ECS


class ECSServer:
    access_key = Variable.get("HUAWEICLOUD_ACCESS_KEY")
    security_key = Variable.get("HUAWEICLOUD_SECURITY_KEY")
    mongo_server = pymongo.MongoClient(Variable.get("BAIZE_MONGODB_URL"))

    def __init__(self, region_id: str):
        print(2)
        self.region_id = region_id
        self.ecs = ECS(access_key=self.access_key, security_key=self.security_key, region_id=self.region_id)
        self.task_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.mongo = self.mongo_server["cmdb"]

    def __save_data_to_cmdb(self, cmdb_servers_info: dict) -> None:
        for server_ip in cmdb_servers_info:
            self.mongo['servers'].update_one(
                {"server_ip": server_ip, "server_name": cmdb_servers_info[server_ip]["server_name"]},
                {"$set": cmdb_servers_info[server_ip]},
                upsert=True
            )

    def discovery(self, limit: int = 10) -> None:
        print(f"huaweicloud ecs discovery start(limit - {limit}) {self.ecs} 2")
        cmdb_servers_info = {}
        count_response = self.ecs.get_list_servers_details(limit=1)
        print(f"count_response: {count_response.count}")
        for i in range(math.ceil(count_response.count / limit)):
            response = self.ecs.get_list_servers_details(limit=limit, offset=i + 1)
            for server in response.servers:
                server_host = server.addresses[server.metadata['vpc_id']][0].addr
                print(f"server_name: {server.name} -- server_host: {server_host}")
                cmdb_servers_info[server_host] = {
                    "server_name": server.name,
                    "salt_minion_id": server.id,
                    "mem_total": str(round(int(server.flavor.ram) / 1024)) + "G",
                    "num_cpus": int(server.flavor.vcpus),
                    "server_kernel": server.metadata['os_type'],
                    "server_cloud": "huawei",
                    "server_cloud_region": self.region_id
                }
        self.__save_data_to_cmdb(cmdb_servers_info)
        # print(cmdb_servers_info)