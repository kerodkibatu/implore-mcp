# Implore MCP

**MCP to Implore the Human Intelligence**

A Model Context Protocol (MCP) server that provides a tool to request input from humans via GUI dialog boxes. This tool allows AI assistants to "implore" human users for input, decisions, or clarification through a visual interface.

Inspired by the [Interactive Feedback MCP](https://github.com/dotcursorrules/interactive-feedback-mcp)

## Features

- **Simple GUI Dialog**: Uses PySide6 to display native GUI dialogs
- **Process Isolation**: GUI runs in a separate subprocess to avoid blocking the MCP server
- **Flexible Input**: Request any text input from users with custom messages
- **System Monitoring**: Includes psutil-based system information tool
- **FastMCP Integration**: Built on FastMCP for easy MCP server implementation
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Architecture

The tool uses a decoupled architecture:
- `server.py`: MCP server that handles tool requests and launches the GUI subprocess
- `implore_ui.py`: Separate GUI process that displays dialogs and communicates results via temporary files
- Communication via temporary JSON files ensures the main server process remains responsive

## Installation

1. Clone or download this repository:
```bash
git clone <repository-url>
cd implore-mcp
```

2. Install dependencies:
```bash
pip install -e .
```

Or install dependencies directly:
```bash
pip install fastmcp>=2.0.0 psutil>=7.0.0 pyside6>=6.8.2.1
```

## Usage

### Running the Server

Start the MCP server:

```bash
python server.py
```

Or if installed as a package:

```bash
implore-mcp
```

### Configuring in MCP Clients

Add to your MCP client configuration (e.g., Claude Desktop, Cline):

#### Using Python directly:
```json
{
  "mcpServers": {
    "implore": {
      "command": "python",
      "args": ["C:/path/to/implore-mcp/server.py"]
    }
  }
}
```

#### Using installed package:
```json
{
  "mcpServers": {
    "implore": {
      "command": "implore-mcp"
    }
  }
}
```

### Using the Tool

Once configured, the AI assistant can use the `implore` tool to request input from you:

**Example 1: Simple HelloWorld**
```
Tool: implore
Arguments: {}
Result: Shows a dialog with "HelloWorld" message
```

**Example 2: Custom Message**
```
Tool: implore
Arguments: {
  "message": "Please provide the API key for the service:",
  "title": "API Key Required"
}
Result: Shows a dialog with your custom message and returns user input
```

## Tool Reference

### `implore`

Displays a GUI dialog to request input from the user. The dialog runs in a separate process.

**Parameters:**
- `message` (str, optional): The message to display to the user. Default: "HelloWorld"
- `title` (str, optional): The title of the dialog window. Default: "Human Input Requested"

**Returns:**
- User's response as a string
- "(empty response)" if user submitted without entering text
- "(cancelled by user)" if user cancelled the dialog
- Error message if dialog could not be displayed

### `system_info`

Gets current system resource information using psutil.

**Parameters:** None

**Returns:**
- Dictionary containing:
  - `cpu_percent`: Current CPU usage percentage
  - `memory_percent`: Current memory usage percentage
  - `process_count`: Number of running processes
  - `available_memory_mb`: Available memory in megabytes

## Dependencies

- **fastmcp** (>=2.0.0): FastMCP framework for building MCP servers
- **psutil** (>=7.0.0): System and process utilities
- **pyside6** (>=6.8.2.1): Qt for Python - GUI framework

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
