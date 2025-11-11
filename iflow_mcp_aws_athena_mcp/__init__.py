#!/usr/bin/env python3
"""
iFlow MCP AWS Athena MCP Server

A Python wrapper for the Node.js-based AWS Athena MCP server.
This package allows installation via pip while running the underlying Node.js server.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

__version__ = "1.0.0"

def find_node():
    """Find Node.js executable"""
    node_cmd = shutil.which("node")
    if not node_cmd:
        raise RuntimeError("Node.js is not installed or not in PATH. Please install Node.js >= 16")
    return node_cmd

def find_npm():
    """Find npm executable"""
    npm_cmd = shutil.which("npm")
    if not npm_cmd:
        raise RuntimeError("npm is not installed or not in PATH. Please install Node.js with npm")
    return npm_cmd

def get_package_dir():
    """Get the package directory"""
    return Path(__file__).parent

def install_dependencies():
    """Install Node.js dependencies"""
    package_dir = get_package_dir()
    package_json = package_dir / "package.json"
    
    if not package_json.exists():
        raise RuntimeError(f"package.json not found in {package_dir}")
    
    npm_cmd = find_npm()
    try:
        subprocess.run([npm_cmd, "install"], cwd=package_dir, check=True)
        subprocess.run([npm_cmd, "run", "build"], cwd=package_dir, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to install Node.js dependencies: {e}")

def main():
    """Main entry point for the MCP server"""
    try:
        node_cmd = find_node()
        package_dir = get_package_dir()
        
        # Check if build directory exists, if not, install dependencies
        build_dir = package_dir / "build"
        if not build_dir.exists():
            print("Installing Node.js dependencies...", file=sys.stderr)
            install_dependencies()
        
        # Run the Node.js server
        server_script = build_dir / "index.js"
        if not server_script.exists():
            raise RuntimeError(f"Server script not found: {server_script}")
        
        subprocess.run([node_cmd, str(server_script)], check=True)
        
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()