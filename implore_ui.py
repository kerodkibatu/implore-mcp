"""
Implore UI - Separate process for displaying GUI dialogs.
"""

import sys
import json
import argparse
from PySide6.QtWidgets import QApplication, QInputDialog


def main():
    parser = argparse.ArgumentParser(description="Display GUI dialog for user input")
    parser.add_argument("--message", required=True, help="Message to display")
    parser.add_argument("--title", required=True, help="Dialog title")
    parser.add_argument("--output-file", required=True, help="Output file path for result")
    
    args = parser.parse_args()
    
    # Initialize Qt Application
    app = QApplication(sys.argv)
    
    # Show input dialog
    text, ok = QInputDialog.getText(
        None,
        args.title,
        args.message,
        text=""
    )
    
    # Prepare result
    result = {
        "success": ok,
        "value": text if ok else None,
        "cancelled": not ok
    }
    
    # Write result to output file
    with open(args.output_file, 'w') as f:
        json.dump(result, f)
    
    # Exit with appropriate code
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

