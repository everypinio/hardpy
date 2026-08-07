from platform import node as platform_node

import machineid


def machine_id() -> str:
    """Get machine id.

    Returns:
        str: id, if available, otherwise MAC address
    """
    try:
        return machineid.id()
    except machineid.MachineIdNotFound:
        return platform_node()
