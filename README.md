# OCIResouceCleanup
Terminate resources based on expiration tags

Install python, oci and create a config for the tenant.(ensure user mentioned in the config file has necessary permissions)

Assuming tag defaults have been set for a compartment in the following format - 
Tag Namespace : "ExpirationTag"
Tag Key : "ExpirationDate(dd/mm/yyyy)"

This script will check if the tagged resources are expired or not, if expired it would try to terminate the resource.
