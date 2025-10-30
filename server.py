"""
Implore MCP Server - A tool to request input from humans via GUI quiz dialog.
Developed with inspiration from Interactive Feedback MCP pattern.
"""

import os
import sys
import json
import tempfile
import subprocess
from typing import Dict, List, Optional

import psutil
from fastmcp import FastMCP
from pydantic import BaseModel, Field

# The log_level is necessary for Cline to work
mcp = FastMCP("implore", log_level="ERROR")


class Question(BaseModel):
    """A single question in the quiz."""
    id: str = Field(description="Unique identifier for the question")
    text: str = Field(description="The question text to display")
    type: str = Field(description="Question type: 'multiple_choice' or 'free_form'")
    options: Optional[List[str]] = Field(default=None, description="Options for multiple choice questions")


def launch_implore_ui(questions_json: str, title: str) -> Dict[str, any]:
    """Launch the GUI in a separate process and get the result via temp file."""
    # Create a temporary file for the result
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
            "--questions", questions_json,
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
def implore(
    questions: List[Dict],
    title: str = "Human Input Requested"
) -> Dict[str, any]:
    """
    This tool launches a separate GUI process to show a quiz with one or more questions
    and waits for the user to respond. Multiple choice questions include an automatic "Other..." 
    option with text input for additional flexibility. Perfect for clarifying requirements, 
    getting decisions, or extracting implicit knowledge from users.
    
    Args:
        questions: A list of question objects. Each question object should have:
                   - text (str): The question text
                   - type (str): Either "multiple_choice" or "free_form". 
                     For "multiple_choice", an automatic "Other..." radio button with text input is included after the options.
                   - options (list, optional): List of options for multiple choice questions
                   - id (str, optional): Unique identifier (auto-generated as "q1", "q2", etc. if not provided)
        title: The title of the dialog window (default: "Human Input Requested")
    
    Returns:
        Dictionary with structured response:
        - On success: {"success": True, "answers": {question_id: answer, ...}}
        - On cancel: {"success": False, "cancelled": True}
        - On error: {"success": False, "error": "error message"}
    
    Notes:
    - Unanswered multiple choice questions return null
    - Unanswered free-form questions return empty string ""
    - Prefer using comprehensive multiple choice options for most questions to provide structured choices, 
      reserving free-form for simple copy-paste values or easily answered open questions. 
      The automatic "Other..." option in multiple choice provides flexibility for cases not covered by the options.
    
    Examples:
        Single question:
        implore(questions=[
            {
                "id": "api_key",
                "text": "What is your API key?",
                "type": "free_form"
            }
        ])
        
        Multiple questions:
        implore(questions=[
            {
                "id": "framework",
                "text": "Which framework should we use?",
                "type": "multiple_choice",
                "options": ["React", "Vue", "Angular"]
            },
            {
                "id": "requirements",
                "text": "Any additional requirements?",
                "type": "free_form"
            }
        ])
    """
    try:
        # Validate and structure the questions
        question_list = []
        for i, q in enumerate(questions):
            if isinstance(q, dict):
                # Ensure required fields
                q_id = q.get("id", f"q{i+1}")
                q_text = q.get("text", "")
                q_type = q.get("type", "free_form")
                q_options = q.get("options", None)
                
                question_list.append({
                    "id": q_id,
                    "text": q_text,
                    "type": q_type,
                    "options": q_options
                })
        
        # Convert to JSON string for passing to subprocess
        questions_json = json.dumps(question_list)
        
        # Launch the UI
        result = launch_implore_ui(questions_json, title)
        
        if result.get("success"):
            answers = result.get("answers", {})
            return {
                "success": True,
                "answers": answers
            }
        else:
            return {
                "success": False,
                "cancelled": True
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def main():
    """Run the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()