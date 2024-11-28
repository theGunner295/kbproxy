Very simple sync between live nodes and an pfSense HAProxy instance.
Configured by default to run once every 20 minutes, only applying changes when required.

Will go through and update all backends that contain the string found in "BACKEND_SEARCH_STRING" in appsettings.json

Example appsettings.json

{
    "USERNAME": "admin",
    "PASSWORD": "pfsense",
    "HAProxyHostApi": "https://myrouter.local",
    "BACKEND_SEARCH_STRING": "ClusterName"
}


Currently it's only compatible with clusters that use a private CA.
Put a cacerts.pem chain into the root dir either during build or at runtime.

Kubeconfig needs to be present in the same place with the name config.yaml
