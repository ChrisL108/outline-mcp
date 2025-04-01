# Outline MCP

An MCP (Model Control Protocol) server for integrating Outline with Claude.

## Overview

This tool provides Claude with the ability to search and retrieve documents from your Outline knowledge base. Use it to help Claude answer questions using your organization's internal documentation.

## Features

- Search for documents in your Outline instance
- Retrieve full document content by ID
- Maintain persistent credentials between sessions

## Installation

### Option 1: Install via Smithery CLI (requires smithery key)

```bash
npx -y @smithery/cli@latest install @ChrisL108/outline-mcp --client claude --key your-smithery-key
```

You can enter your `OUTLINE_URL` and `OUTLINE_API_KEY` when prompted by Claude or add them to your `claude_desktop_config.json` directly:

```json
"env": {
    "OUTLINE_URL": "https://your.outline.com",
    "OUTLINE_API_KEY": "your-api-key"
}
```

This will update your config to look like this:

```json
"outline-mcp": {
    "command": "npx",
    "args": [
      "-y",
      "@smithery/cli@latest",
      "run",
      "@ChrisL108/outline-mcp",
      "--key",
      "your-smithery-key"
    ],
    "env": {
      "OUTLINE_URL": "https://your.outline.com",
      "OUTLINE_API_KEY": "your-api-key"
    }
}
```

### Option 2: Install via UVX

```json
"outline-mcp": {
    "command": "uvx",
    "args": [
      "--from",
      "git+https://github.com/ChrisL108/outline-mcp",
      "outline-mcp"
    ],
    "env": {
      "OUTLINE_URL": "https://your.outline.com",
      "OUTLINE_API_KEY": "your-api-key"
    }
}
```

## Usage

Once installed, you can use the following functions in your conversations with Claude:

### Search Documents

```
search_documents(query, outline_url=None, api_key=None, limit=5, status_filter="published", date_filter="year")
```

Parameters:
- `query`: Search term (required)
- `outline_url`: Base URL of your Outline instance (only needed first time)
- `api_key`: Outline API key (only needed first time)
- `limit`: Maximum number of results (default: 5)
- `status_filter`: Filter by status (default: "published")
- `date_filter`: Filter by date (default: "year")

### Get Document by ID

```
get_document_by_id(document_id)
```

Parameters:
- `document_id`: ID of the document to retrieve (required)

### Update Credentials

```
update_credentials(outline_url, api_key)
```

Parameters:
- `outline_url`: Base URL of your Outline instance
- `api_key`: Outline API key

### Ping

```
ping()
```

Simple test function to verify the MCP server is working.

## Example Prompts

Here are some example prompts you can use with Claude:

1. "Search Outline for information about our product roadmap."
2. "Can you find any documents related to our hiring process?"
3. "Check our internal documentation for our AWS setup."
4. "Can you get the full content of this document? [document_id]"

## Troubleshooting

If you encounter issues:

1. Ensure your Outline URL and API key are correctly configured
2. Verify that your Outline instance is accessible
3. Check if your API key has the necessary permissions
4. Try the `ping()` function to verify the MCP server is running correctly

## Security Considerations

- Keep your API key secure and don't share it
- The MCP server only has the permissions granted to your API key
- Consider using a read-only API key if you only need search functionality

## License

MIT License

Copyright (c) 2025 ChrisL108

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Credits

Created by [ChrisL108](https://github.com/ChrisL108)