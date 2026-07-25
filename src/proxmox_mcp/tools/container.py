"""
LXC container-related tools for Proxmox MCP.

This module provides tools for managing and interacting with Proxmox LXC
containers:
- Listing all containers across the cluster with their status
- Retrieving detailed status for a single container
- Changing container run state (start, stop, shutdown, reboot, etc.)

Unlike QEMU VMs, LXC containers do not expose a guest-agent command
execution endpoint through the Proxmox API, so there is no in-container
command tool here. Use the host shell (`pct exec <vmid> -- ...`) for that.
"""
from typing import List
from mcp.types import TextContent as Content
from .base import ProxmoxTool
from .definitions import GET_CONTAINERS_DESC

class ContainerTools(ProxmoxTool):
    """Tools for managing Proxmox LXC containers.

    Provides functionality for:
    - Retrieving cluster-wide container information
    - Getting detailed status for a single container
    - Changing container run state

    Implements a fallback mechanism for scenarios where detailed
    container configuration might be temporarily unavailable.
    """

    # Actions supported by the LXC status API. Deliberately excludes
    # QEMU-only actions such as 'reset', 'pause', and 'hibernate'.
    VALID_ACTIONS = ["start", "stop", "shutdown", "reboot", "suspend", "resume"]

    def get_containers(self) -> List[Content]:
        """List all LXC containers across the cluster with detailed status.

        Retrieves comprehensive information for each container including:
        - Basic identification (ID, name)
        - Runtime status (running, stopped)
        - Resource allocation and usage (CPU cores, memory)
        - Node placement

        Implements a fallback mechanism that returns basic information
        if detailed configuration retrieval fails for any container.

        Returns:
            List of Content objects containing formatted container information.

        Raises:
            RuntimeError: If the cluster-wide container query fails
        """
        try:
            result = []
            for node in self.proxmox.nodes.get():
                node_name = node["node"]
                containers = self.proxmox.nodes(node_name).lxc.get()
                for container in containers:
                    vmid = container["vmid"]
                    # Get container config for CPU cores
                    try:
                        config = self.proxmox.nodes(node_name).lxc(vmid).config.get()
                        cpus = config.get("cores", "N/A")
                    except Exception:
                        # Fallback if we can't read the config
                        cpus = "N/A"
                    result.append({
                        "vmid": vmid,
                        "name": container.get("name", "N/A"),
                        "status": container["status"],
                        "node": node_name,
                        "cpus": cpus,
                        "memory": {
                            "used": container.get("mem", 0),
                            "total": container.get("maxmem", 0)
                        }
                    })
            return self._format_response(result, "containers")
        except Exception as e:
            self._handle_error("get containers", e)

    def get_container_status(self, node: str, vmid: str) -> List[Content]:
        """Get detailed status for a specific LXC container.

        Args:
            node: Host node name (e.g. 'pve1')
            vmid: Container ID number (e.g. '200')

        Returns:
            List of Content objects containing the formatted container status.

        Raises:
            ValueError: If the container is not found
            RuntimeError: If the status query fails
        """
        try:
            status = self.proxmox.nodes(node).lxc(vmid).status.current.get()
            data = {
                "vmid": str(vmid),
                "name": status.get("name", "N/A"),
                "status": status.get("status", "unknown"),
                "node": node,
                "uptime": status.get("uptime", 0),
                "lock": status.get("lock", ""),
                "cpus": status.get("cpus", "N/A"),
                "memory": {
                    "used": status.get("mem", 0),
                    "total": status.get("maxmem", 0)
                }
            }
            return self._format_response(data, "container_status")
        except Exception as e:
            self._handle_error(f"get status for container {vmid}", e)

    def change_container_state(self, node: str, vmid: str, action: str) -> List[Content]:
        """Change the state of an LXC container.

        Args:
            node: Host node name (e.g. 'pve1')
            vmid: Container ID number (e.g. '200')
            action: One of 'start', 'stop', 'shutdown', 'reboot', 'suspend', 'resume'

        Returns:
            List of Content objects indicating success or failure.

        Raises:
            ValueError: If the action is invalid or the container is not found
            RuntimeError: If the state change fails
        """
        try:
            if action not in self.VALID_ACTIONS:
                raise ValueError(
                    f"Invalid action: {action}. Must be one of {self.VALID_ACTIONS}"
                )

            # The Proxmox LXC API uses .status.<action>.post()
            status_api = self.proxmox.nodes(node).lxc(vmid).status
            api_method = getattr(status_api, action, None)
            if not api_method:
                raise ValueError(f"Action '{action}' is not supported by the Proxmox API.")

            api_method.post()
            result = {
                "success": True,
                "action": action,
                "vmid": str(vmid),
                "node": node
            }
            return self._format_response(result)
        except Exception as e:
            self._handle_error(f"change container state ({action}) for container {vmid}", e)
