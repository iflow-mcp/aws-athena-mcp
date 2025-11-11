#!/usr/bin/env python3
"""
Setup script for iflow-mcp-aws-athena-mcp
"""

from setuptools import setup, find_packages
import os
import shutil
import subprocess
from pathlib import Path

def copy_node_files():
    """Copy Node.js files to the package directory"""
    package_dir = Path("iflow_mcp_aws_athena_mcp")
    
    # Files to copy
    files_to_copy = [
        "src",
        "package.json", 
        "tsconfig.json",
        "package-lock.json"
    ]
    
    for file_path in files_to_copy:
        src = Path(file_path)
        dst = package_dir / file_path
        
        if src.exists():
            if src.is_dir():
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

# Copy Node.js files during setup
copy_node_files()

setup()