from typing import Dict, Any, List, Optional
from src.desktop.governance import LayeredGovernance

class DesktopBinding:
    """
    HAG-Desktop Build 4.0: Desktop Binding Protocol.
    Interfaces between the HAG brain and the OS (Filesystem, Shell, Apps).
    Protected by Layered Governance Architecture (LGA).
    """
    def __init__(self, governance: LayeredGovernance):
        self.governance = governance
        self.active_session_token = None

    def set_session_token(self, token: str):
        """Sets the L3 capability token for the current task session."""
        self.active_session_token = token

    def read_file(self, task_description: str, file_path: str) -> Dict[str, Any]:
        """Secured file reading via LGA."""
        action = f"read_file('{file_path}')"
        return self.governance.execute_secured_action(
            task_description=task_description,
            action_code=action,
            token=self.active_session_token,
            required_cap="fs_read"
        )

    def write_file(self, task_description: str, file_path: str, content: str) -> Dict[str, Any]:
        """Secured file writing via LGA."""
        action = f"write_file('{file_path}', '...')"
        return self.governance.execute_secured_action(
            task_description=task_description,
            action_code=action,
            token=self.active_session_token,
            required_cap="fs_write"
        )

    def execute_shell(self, task_description: str, command: str) -> Dict[str, Any]:
        """Secured shell command execution via LGA."""
        return self.governance.execute_secured_action(
            task_description=task_description,
            action_code=command,
            token=self.active_session_token,
            required_cap="shell_exec"
        )

    def list_directory(self, task_description: str, path: str) -> Dict[str, Any]:
        """Secured directory listing via LGA."""
        action = f"list_dir('{path}')"
        return self.governance.execute_secured_action(
            task_description=task_description,
            action_code=action,
            token=self.active_session_token,
            required_cap="fs_read"
        )
