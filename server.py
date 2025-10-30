"""
Implore MCP Server - A tool to request input from humans via GUI dialog.
Developed with inspiration from Interactive Feedback MCP pattern.
"""

import os
import sys
import json
import tempfile
import subprocess
from typing import Dict

import psutil
from fastmcp import FastMCP

# The log_level is necessary for Cline to work
mcp = FastMCP("implore", log_level="ERROR")


def launch_implore_ui(message: str, title: str) -> Dict[str, any]:
    """Launch the GUI in a separate process and get the result via temp file."""
    # Create a temporary file for the feedback result
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        output_file = tmp.name

    try:
        # Get the path to implore_ui.py relative to this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ui_script_path = os.path.join(script_dir, "implore_ui.py")

        # Run implore_ui.py as a separate process
        args = [
            sys.executable,
            "-u",
            ui_script_path,
            "--message", message,
            "--title", title,
            "--output-file", output_file
        ]
        
        result = subprocess.run(
            args,
            check=False,
            shell=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            close_fds=True
        )
        
        # Read the result from the temporary file
        with open(output_file, 'r') as f:
            ui_result = json.load(f)
        os.unlink(output_file)
        return ui_result
        
    except Exception as e:
        if os.path.exists(output_file):
            os.unlink(output_file)
        raise e


@mcp.tool()
def implore(message: str = "HelloWorld", title: str = "Human Input Requested") -> str:
    """
    Implore the Human Intelligence - Display a GUI dialog to request input from the user.
    
    This tool launches a separate GUI process to show a dialog box with the specified 
    message and waits for the user to respond. The GUI runs independently to avoid 
    blocking the main MCP server process.
    
    Args:
        message: The message to display to the user (default: "HelloWorld")
        title: The title of the dialog window (default: "Human Input Requested")
    
    Returns:
        The user's response as a string, or a message if cancelled
    """
    try:
        result = launch_implore_ui(message, title)
        
        if result["success"]:
            value = result["value"]
            return value if value else "(empty response)"
        else:
            return "(cancelled by user)"
            
    except Exception as e:
        return f"Error displaying dialog: {str(e)}"

if __name__ == "__main__":
    # Run the MCP server
    mcp.run(transport="stdio")
