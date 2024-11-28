<img src="https://dev.azure.com/RedshiftEnt/Redshift-CICD/_apis/build/status%2FPersonal%20Projects%2FKBProxy?branchName=main"/>

Very simple sync between live nodes and an pfSense HAProxy instance.
Configured by default to run once every 20 minutes, only applying changes when required.

Will go through and update all backends in HAProxy that contain the string found in "BACKEND_SEARCH_STRING" in appsettings.json

ALL ADDITIONAL/CONFIG FILES NEED TO GO INTO A CONFIG FOLDER IN THE ROOT FOLDER!

Example appsettings.json

{
    "USERNAME": "admin", // Username for the HAProxy API
    "PASSWORD": "pfsense", // Password for the HAProxy API
    "HAProxyHostApi": "https://myrouter.local", // HAProxy pfSense Host
    "BACKEND_SEARCH_STRING": "ClusterName" // Backend search string
}

Remove comments in above json if you copy it, service will error otherwise.

Currently it's only compatible with clusters that use a private CA.
Put a cacerts.pem chain into the config dir either during build or at runtime.

Kubeconfig needs to be present in the same place with the name config.yaml
