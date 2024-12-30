<img src="https://dev.azure.com/RedshiftEnt/Redshift-CICD/_apis/build/status%2FPersonal%20Projects%2FKBProxy?branchName=main"/>

<h1>Simple Sync for HAProxy and Kubernetes Nodes</h1>

<p>
This service syncs live Kubernetes nodes with an HAProxy instance running on pfSense. It is designed to run every 20 minutes and only applies updates when necessary.
</p>

<h2>How It Works</h2>
<ul>
  <li>Updates all HAProxy backends containing the string specified in <code>BACKEND_SEARCH_STRING</code> (found in <code>appsettings.json</code>).</li>
  <li>Compatible with clusters using a private CA (requires a <code>cacerts.pem</code> chain in the <code>config</code> directory).</li>
</ul>

<h2>Setup</h2>
<p>
All additional/config files must be placed in a <code>config</code> folder at the root level.
</p>

<h3>Example <code>appsettings.json</code></h3>
<pre>
{
  "USERNAME": "admin",           // Username for the HAProxy API
  "PASSWORD": "pfsense",         // Password for the HAProxy API
  "HAProxyHostApi": "https://myrouter.local", // HAProxy pfSense Host
  "BACKEND_SEARCH_STRING": "ClusterName" // Backend search string
}
</pre>
<p><strong>Note:</strong> Remove comments when copying this JSON; the service will error otherwise.</p>

<h3>Required Files</h3>
<ul>
  <li><code>cacerts.pem</code>: Private CA chain for SSL. Place in the <code>config</code> directory during build or runtime.</li>
  <li><code>config.yaml</code>: Kubernetes kubeconfig file. Place in the <code>config</code> directory.</li>
</ul>
