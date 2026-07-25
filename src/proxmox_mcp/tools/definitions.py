"""
Tool descriptions for Proxmox MCP tools.
"""

# Node tool descriptions
GET_NODES_DESC = """List all nodes in the Proxmox cluster with their status, CPU, memory, and role information.

Example:
{"node": "pve1", "status": "online", "cpu_usage": 0.15, "memory": {"used": "8GB", "total": "32GB"}}"""

GET_NODE_STATUS_DESC = """Get detailed status information for a specific Proxmox node.

Parameters:
node* - Name/ID of node to query (e.g. 'pve1')

Example:
{"cpu": {"usage": 0.15}, "memory": {"used": "8GB", "total": "32GB"}}"""

# VM tool descriptions
GET_VMS_DESC = """List all virtual machines across the cluster with their status and resource usage.

Example:
{"vmid": "100", "name": "ubuntu", "status": "running", "cpu": 2, "memory": 4096}"""

CHANGE_VM_STATE_DESC = """Change the state of a virtual machine (shutdown, start, reboot, pause, hibernate, reset, etc.).

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - VM ID number (e.g. '100')
action* - Action to perform (one of: 'start', 'stop', 'shutdown', 'reboot', 'reset', 'suspend', 'resume', 'pause', 'hibernate')

Example:
{"success": true, "action": "shutdown", "vmid": "100", "node": "pve1"}
"""

CREATE_VM_DESC = """Create (spin up) a new virtual machine from a local ISO.

Parameters:
node* - Host node name (e.g. 'pve1')
name* - Name for the new VM (e.g. 'my-new-vm')
iso* - ISO image filename from local storage (e.g. 'local:iso/ubuntu-22.04.iso')
cores - Number of CPU cores (default: 2)
memory - Memory in MB (default: 2048)
storage - Storage pool to use (default: 'local-lvm')

Example:
{"success": true, "vmid": "101", "name": "my-new-vm", "node": "pve1"}
"""

EXECUTE_VM_COMMAND_DESC = """Execute commands in a VM via QEMU guest agent.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - VM ID number (e.g. '100')
command* - Shell command to run (e.g. 'uname -a')

Example:
{"success": true, "output": "Linux vm1 5.4.0", "exit_code": 0}"""

# Container tool descriptions
GET_CONTAINERS_DESC = """List all LXC containers across the cluster with their status and resource usage.

Example:
{"vmid": "200", "name": "nginx", "status": "running", "node": "pve1", "cpus": 2, "memory": {"used": 268435456, "total": 536870912}}"""

GET_CONTAINER_STATUS_DESC = """Get detailed status for a specific LXC container, including uptime, CPU, memory, and any active lock.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - Container ID number (e.g. '200')

Example:
{"vmid": "200", "name": "nginx", "status": "running", "uptime": 123456, "cpus": 2, "memory": {"used": 268435456, "total": 536870912}}"""

CHANGE_CONTAINER_STATE_DESC = """Change the state of an LXC container.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - Container ID number (e.g. '200')
action* - Action to perform (one of: 'start', 'stop', 'shutdown', 'reboot', 'suspend', 'resume')

Note: LXC containers do not support QEMU-VM actions such as 'reset', 'pause', or 'hibernate'.

Example:
{"success": true, "action": "start", "vmid": "200", "node": "pve1"}"""

# Storage tool descriptions
GET_STORAGE_DESC = """List storage pools across the cluster with their usage and configuration.

Example:
{"storage": "local-lvm", "type": "lvm", "used": "500GB", "total": "1TB"}"""

# Cluster tool descriptions
GET_CLUSTER_STATUS_DESC = """Get overall Proxmox cluster health and configuration status.

Example:
{"name": "proxmox", "quorum": "ok", "nodes": 3, "ha_status": "active"}"""
