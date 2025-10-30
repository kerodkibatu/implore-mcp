# Implore MCP

**MCP to Implore the Human Intelligence**

A Model Context Protocol (MCP) server that provides a quiz-style tool to request input from humans via GUI dialogs. This tool allows AI assistants to "implore" human users for clarification, decisions, or knowledge extraction through an interactive visual interface.

Inspired by the [Interactive Feedback MCP](https://github.com/dotcursorrules/interactive-feedback-mcp) pattern.

## Features

- **Quiz-Style Interface**: Display multiple questions in a single, scrollable dialog
- **Multiple Question Types**: 
  - Multiple choice (radio buttons with automatic "Other..." option including text input)
  - Free-form text input
- **Process Isolation**: GUI runs in a separate subprocess to avoid blocking the MCP server
- **Structured Responses**: Get organized answers mapped to question IDs
- **FastMCP Integration**: Built on FastMCP for easy MCP server implementation
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Architecture

The tool uses a decoupled architecture:
- `server.py`: MCP server that handles tool requests and launches the GUI subprocess
- `implore_ui.py`: Separate GUI process that displays quiz dialogs and communicates results via temporary files
- Communication via temporary JSON files ensures the main server process remains responsive

## Installation

1. Clone or download this repository:
```bash
git clone <repository-url>
cd implore-mcp
```

2. Install dependencies using uv:
```bash
uv sync
```

Or install directly:
```bash
uv pip install fastmcp>=2.0.0 psutil>=7.0.0 pyside6>=6.8.2.1
```

## Usage

### Running the Server

Start the MCP server:

```bash
uv run server.py
```

Or using Python directly:

```bash
python server.py
```

### Configuring in MCP Clients

Add to your MCP client configuration (e.g., Claude Desktop, Cline):

#### Using uv:
```json
{
  "mcpServers": {
    "implore": {
      "command": "uv",
      "args": ["run", "C:/path/to/implore-mcp/server.py"]
    }
  }
}
```

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

### Using the Tool

Once configured, the AI assistant can use the `implore` tool to request input from you:

#### Example 1: Single Free-Form Question
```
Tool: implore
Arguments: {
  "questions": [
    {
      "text": "What is your preferred color scheme?",
      "type": "free_form"
    }
  ]
}
Result: {
  "success": true,
  "answers": {
    "q1": "Dark mode"
  }
}
```

#### Example 2: Multiple Choice Question
```
Tool: implore
Arguments: {
  "questions": [
    {
      "id": "framework",
      "text": "Which web framework should we use?",
      "type": "multiple_choice",
      "options": ["React", "Vue", "Angular", "Svelte"]
    }
  ],
  "title": "Framework Selection"
}
Result: {
  "success": true,
  "answers": {
    "framework": "React"
  }
}
```

#### Example 3: Mixed Question Types
```
Tool: implore
Arguments: {
  "questions": [
    {
      "id": "deployment",
      "text": "Where should we deploy the application?",
      "type": "multiple_choice",
      "options": ["AWS", "Azure", "Google Cloud", "On-Premise"]
    },
    {
      "id": "timeline",
      "text": "What is your preferred timeline?",
      "type": "free_form"
    },
    {
      "id": "budget",
      "text": "What is your budget range?",
      "type": "multiple_choice",
      "options": ["Under $100", "$100-$500", "$500-$1000", "Over $1000"]
    },
    {
      "id": "additional",
      "text": "Any additional requirements or concerns?",
      "type": "free_form"
    }
  ],
  "title": "Project Planning Questions"
}
Result: {
  "success": true,
  "answers": {
    "deployment": "AWS",
    "timeline": "2-3 months",
    "budget": "$500-$1000",
    "additional": "Need to support mobile devices"
  }
}
```

## Tool Reference

### `implore`

Displays a quiz-style GUI dialog to request input from the user. The dialog runs in a separate process and can handle multiple questions of different types.

**Parameters:**

- `questions` (list, required): Array of question objects for quiz-style interface
- `title` (str, optional): The title of the dialog window. Default: "Human Input Requested"

**Question Object Structure:**

Each question in the list should have:
- `text` (str, required): The question text to display
- `type` (str, required): Either "multiple_choice" or "free_form"
- For "multiple_choice", an automatic "Other..." option with free-text input is always included after the provided options.
- `options` (list, optional): List of option strings (required for multiple_choice)
- `id` (str, optional): Unique identifier (auto-generated as "q1", "q2", etc. if not provided)

**Returns:**

Dictionary with structured response:
- **Success**: `{"success": True, "answers": {question_id: answer, ...}}`
- **Cancelled**: `{"success": False, "cancelled": True}`
- **Error**: `{"success": False, "error": "error message"}`

**Notes:**
- Multiple choice questions that aren't answered will have `null` value
- Free-form questions that aren't answered will have empty string value
- Prefer using comprehensive multiple choice options for most questions to guide responses, reserving free-form for simple copy-paste values or easily answered open questions. The automatic "Other..." option in multiple choice provides flexibility for additional input.

## Use Cases

The `implore` tool is perfect for:

1. **Requirement Clarification**: Ask users to clarify ambiguous requirements
2. **Design Decisions**: Get user preferences on architecture or design choices
3. **Configuration Selection**: Let users choose from predefined configuration options
4. **Knowledge Extraction**: Extract implicit knowledge from users through targeted questions
5. **Progress Checkpoints**: Confirm decisions before proceeding with major changes
6. **Feature Prioritization**: Ask users to prioritize features or tasks
7. **Error Resolution**: When multiple solutions exist, ask user which approach to take

## Dependencies

- **fastmcp** (>=2.0.0): FastMCP framework for building MCP servers
- **psutil** (>=7.0.0): System and process utilities
- **pyside6** (>=6.8.2.1): Qt for Python - GUI framework

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

## Credits

Developed with inspiration from the [Interactive Feedback MCP](https://github.com/dotcursorrules/interactive-feedback-mcp) pattern.
