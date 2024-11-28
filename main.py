"""KBProxy Redshift Connector"""

import json
import re
import time
import urllib3
from kubernetes import client as kubeclient, config as kubeconfig

with open("appsettings.json", "r", encoding="UTF8") as file:
    config = json.loads(file.read())

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs='cacerts.pem',
    headers=urllib3.make_headers(basic_auth=f"{config['USERNAME']}:{config['PASSWORD']}")
)

kubeconfig.load_kube_config("config.yaml")
kube_client = kubeclient.CoreV1Api()


def get_data(item_id: int) -> tuple:
    """Get the data from the API"""
    data = json.loads(http.request("GET",f"{config['HAProxyHostApi']}/api/v2/services/haproxy/backend?id={item_id}").data.decode("utf-8"))
    if data['code'] == 200:
        return (data['data'], data['code'])
    else:
        return (data.get('data'), 404)

def get_port_from_server_name(server_name: str) -> int:
    """Get the port number from the server name"""
    return re.search(r'TCP(\d+)', server_name).group(1)

def main():
    """Main function"""
    contains_kube = True
    item_id = 0
    config_list = []
    while contains_kube:
        data = get_data(item_id)
        if data[1] == 200:
            if  "RS-03-KUB-01" in data[0].get('name'):
                config_list.append(data[0])
        else:
            contains_kube = False
        item_id += 1
    live_nodes = kube_client.list_node(watch=False)
    node_list = []
    for node in live_nodes.items:
        node_list.append((node.metadata.name, node.status.addresses[0].address))
    server_requires_removing = []
    server_requires_adding = []
    for backend in config_list:
        if backend['servers'] is not None:
            for server in backend['servers']:
                if server['address'] not in [node[1] for node in node_list]:
                    server_requires_removing.append(server)
        for node in node_list:
            if backend['servers'] is None or node[1] not in [server['address'] for server in backend['servers']]:
                port = get_port_from_server_name(backend['name'])
                server_requires_adding.append(({"parent_id": backend["id"], "name":node[0], "status":"active", "address":node[1], "port":port}))


    applied_changes = False
    # Process the servers that require removing first
    for server in server_requires_removing:
        applied_changes = True
        http.request("DELETE", f"{config['HAProxyHostApi']}/api/v2/services/haproxy/backend/server/?parent_id={server['parent_id']}&id={server['id']}")
    # Process the servers that require adding
    for server in server_requires_adding:
        applied_changes = True
        http.request("POST", f"{config['HAProxyHostApi']}/api/v2/services/haproxy/backend/server", body=json.dumps(server))

    if applied_changes:
        # Apply changes
        print("Applying changes")
        applied_data = json.loads(http.request("GET",f"{config['HAProxyHostApi']}/api/v2/services/haproxy/apply").data.decode("utf-8"))
        print(applied_changes)
        http.request("POST", f"{config['HAProxyHostApi']}/api/v2/services/haproxy/apply")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(1200)
