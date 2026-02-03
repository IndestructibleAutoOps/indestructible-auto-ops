#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL30-49
# @GL-semantic: platform-adapter
# @GL-audit-trail: ./governance/GL_SEMANTIC_ANCHOR.json
#
"""
Cross-Platform Adapter
======================
GL Layer: GL30-49 Execution Layer

Provides cross-platform compatibility for Windows, Linux, and macOS.

Features:
- Platform detection
- Platform-specific configuration
- Unified interface for cross-platform operations
- Dependency installer mapping
- Shell command adaptation
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
import os
import platform
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum


class PlatformType(Enum):
    """Supported platform types"""
    LINUX = "Linux"
    DARWIN = "Darwin"  # macOS
    WINDOWS = "Windows"
    UNKNOWN = "Unknown"


@dataclass
class PlatformConfig:
    """Platform-specific configuration"""
    name: str
    shell_cmd: str
    shell_args: List[str]
    dep_installer: str
    dep_install_cmd: str
    path_separator: str
    line_ending: str
    env_prefix: str
    script_extension: str
    executable_extension: str
    home_var: str
    temp_dir: str


class PlatformAdapter:
    """
    Cross-platform adapter for multi-platform Monorepo support.
    
    Provides unified interface for:
    - Platform detection
    - Command execution
    - Path handling
    - Dependency management
    """
    
    VERSION = "1.0.0"
    
    # Platform configurations
    PLATFORM_CONFIGS = {
        PlatformType.LINUX: PlatformConfig(
            name="Linux",
            shell_cmd="bash",
            shell_args=["-c"],
            dep_installer="apt",
            dep_install_cmd="apt-get install -y",
            path_separator="/",
            line_ending="\n",
            env_prefix="export ",
            script_extension=".sh",
            executable_extension="",
            home_var="HOME",
            temp_dir="/tmp"
        ),
        PlatformType.DARWIN: PlatformConfig(
            name="macOS",
            shell_cmd="zsh",
            shell_args=["-c"],
            dep_installer="brew",
            dep_install_cmd="brew install",
            path_separator="/",
            line_ending="\n",
            env_prefix="export ",
            script_extension=".sh",
            executable_extension="",
            home_var="HOME",
            temp_dir="/tmp"
        ),
        PlatformType.WINDOWS: PlatformConfig(
            name="Windows",
            shell_cmd="powershell",
            shell_args=["-Command"],
            dep_installer="choco",
            dep_install_cmd="choco install -y",
            path_separator="\\",
            line_ending="\r\n",
            env_prefix="$env:",
            script_extension=".ps1",
            executable_extension=".exe",
            home_var="USERPROFILE",
            temp_dir="C:\\Temp"
        ),
        PlatformType.UNKNOWN: PlatformConfig(
            name="Unknown",
            shell_cmd="sh",
            shell_args=["-c"],
            dep_installer="",
            dep_install_cmd="",
            path_separator="/",
            line_ending="\n",
            env_prefix="export ",
            script_extension=".sh",
            executable_extension="",
            home_var="HOME",
            temp_dir="/tmp"
        )
    }
    
    def __init__(self):
        """Initialize platform adapter"""
        self._platform_type = self._detect_platform()
        self._config = self.PLATFORM_CONFIGS[self._platform_type]
    
    def _detect_platform(self) -> PlatformType:
        """Detect current platform"""
        system = platform.system()
        
        if system == "Linux":
            return PlatformType.LINUX
        elif system == "Darwin":
            return PlatformType.DARWIN
        elif system == "Windows":
            return PlatformType.WINDOWS
        else:
            return PlatformType.UNKNOWN
    
    @property
    def platform_type(self) -> PlatformType:
        """Get current platform type"""
        return self._platform_type
    
    @property
    def config(self) -> PlatformConfig:
        """Get current platform configuration"""
        return self._config
    
    def get_platform_config(self) -> Dict[str, Any]:
        """
        Get platform configuration as dictionary.
        
        Returns:
            Dictionary with platform-specific settings
        """
        return {
            "platform": self._platform_type.value,
            "name": self._config.name,
            "cmd": self._config.shell_cmd,
            "dep_installer": self._config.dep_installer,
            "path_separator": self._config.path_separator,
            "script_extension": self._config.script_extension,
            "executable_extension": self._config.executable_extension
        }
    
    def run_command(
        self,
        command: str,
        capture_output: bool = True,
        check: bool = False,
        timeout: Optional[int] = None
    ) -> Tuple[int, str, str]:
        """
        Run a command using platform-appropriate shell.
        
        Args:
            command: Command to run
            capture_output: Whether to capture stdout/stderr
            check: Whether to raise on non-zero exit
            timeout: Command timeout in seconds
        
        Returns:
            Tuple of (exit_code, stdout, stderr)
        """
        cmd_list = [self._config.shell_cmd] + self._config.shell_args + [command]
        
        try:
            result = subprocess.run(
                cmd_list,
                capture_output=capture_output,
                text=True,
                check=check,
                timeout=timeout
            )
            return (result.returncode, result.stdout or "", result.stderr or "")
        except subprocess.CalledProcessError as e:
            return (e.returncode, e.stdout or "", e.stderr or "")
        except subprocess.TimeoutExpired:
            return (-1, "", "Command timed out")
        except Exception as e:
            return (-1, "", str(e))
    
    def install_dependency(self, package: str) -> Tuple[bool, str]:
        """
        Install a package using platform-appropriate installer.
        
        Args:
            package: Package name to install
        
        Returns:
            Tuple of (success, message)
        """
        if not self._config.dep_installer:
            return (False, "No dependency installer configured for this platform")
        
        cmd = f"{self._config.dep_install_cmd} {package}"
        exit_code, stdout, stderr = self.run_command(cmd)
        
        if exit_code == 0:
            return (True, f"Successfully installed {package}")
        else:
            return (False, f"Failed to install {package}: {stderr}")
    
    def normalize_path(self, path: str) -> str:
        """
        Normalize path for current platform.
        
        Args:
            path: Path to normalize
        
        Returns:
            Normalized path string
        """
        if self._platform_type == PlatformType.WINDOWS:
            return path.replace("/", "\\")
        else:
            return path.replace("\\", "/")
    
    def get_home_dir(self) -> Path:
        """Get user home directory"""
        return Path.home()
    
    def get_temp_dir(self) -> Path:
        """Get temporary directory"""
        return Path(self._config.temp_dir)
    
    def which(self, program: str) -> Optional[str]:
        """
        Find program in PATH.
        
        Args:
            program: Program name to find
        
        Returns:
            Path to program or None
        """
        return shutil.which(program)
    
    def is_command_available(self, command: str) -> bool:
        """
        Check if a command is available.
        
        Args:
            command: Command to check
        
        Returns:
            True if command is available
        """
        return self.which(command) is not None
    
    def get_env_var(self, name: str, default: str = "") -> str:
        """
        Get environment variable.
        
        Args:
            name: Variable name
            default: Default value if not set
        
        Returns:
            Variable value or default
        """
        return os.environ.get(name, default)
    
    def set_env_var(self, name: str, value: str):
        """
        Set environment variable.
        
        Args:
            name: Variable name
            value: Variable value
        """
        os.environ[name] = value
    
    def get_system_info(self) -> Dict[str, str]:
        """
        Get system information.
        
        Returns:
            Dictionary with system information
        """
        return {
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "node": platform.node()
        }
    
    def create_script(self, commands: List[str], script_path: str) -> str:
        """
        Create a platform-appropriate script file.
        
        Args:
            commands: List of commands to include
            script_path: Base path for script (extension added automatically)
        
        Returns:
            Full path to created script
        """
        full_path = script_path + self._config.script_extension
        line_ending = self._config.line_ending
        
        if self._platform_type == PlatformType.WINDOWS:
            # PowerShell script
            content = line_ending.join([
                "# Auto-generated PowerShell script",
                "$ErrorActionPreference = 'Stop'",
                ""
            ] + commands)
        else:
            # Bash/Zsh script
            shebang = f"#!/usr/bin/env {self._config.shell_cmd}"
            content = line_ending.join([
                shebang,
                "# Auto-generated shell script",
                "set -euo pipefail",
                ""
            ] + commands)
        
        # For Windows scripts, explicitly write with Windows line endings
        if self._platform_type == PlatformType.WINDOWS:
            with open(full_path, 'w', encoding='utf-8', newline='\r\n') as f:
                f.write(content)
        else:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Make executable on Unix-like systems
        if self._platform_type != PlatformType.WINDOWS:
            os.chmod(full_path, 0o755)
        
        return full_path


# Global adapter instance
_platform_adapter: Optional[PlatformAdapter] = None


def get_platform_adapter() -> PlatformAdapter:
    """
    Get global platform adapter instance.
    
    Returns:
        PlatformAdapter instance
    """
    global _platform_adapter
    
    if _platform_adapter is None:
        _platform_adapter = PlatformAdapter()
    
    return _platform_adapter


def get_platform_config() -> Dict[str, Any]:
    """
    Get current platform configuration.
    
    Convenience function matching the problem statement interface.
    
    Returns:
        Dictionary with platform configuration
    """
    adapter = get_platform_adapter()
    return adapter.get_platform_config()


if __name__ == "__main__":
    # Demo usage
    print("Cross-Platform Adapter Demo")
    print("=" * 50)
    
    adapter = get_platform_adapter()
    config = adapter.get_platform_config()
    
    print(f"\nPlatform: {config['platform']}")
    print(f"Name: {config['name']}")
    print(f"Shell: {config['cmd']}")
    print(f"Package Manager: {config['dep_installer']}")
    print(f"Path Separator: {config['path_separator']}")
    print(f"Script Extension: {config['script_extension']}")
    
    print(f"\nSystem Info:")
    for key, value in adapter.get_system_info().items():
        print(f"  {key}: {value}")
    
    print(f"\nHome Directory: {adapter.get_home_dir()}")
    print(f"Temp Directory: {adapter.get_temp_dir()}")
    
    # Check common commands
    print(f"\nCommand Availability:")
    for cmd in ["python3", "git", "node", "npm", "make"]:
        available = "✅" if adapter.is_command_available(cmd) else "❌"
        print(f"  {cmd}: {available}")
    
    # Run a simple command
    print(f"\nRunning 'echo Hello':")
    exit_code, stdout, stderr = adapter.run_command("echo Hello")
    print(f"  Exit Code: {exit_code}")
    print(f"  Output: {stdout.strip()}")
