from typing import Any, List, Optional
import httpx
import json
import os
import sys
import asyncio
from mcp.server.fastmcp import FastMCP

import logging
# Setup basic logger for now, main() will configure it more thoroughly
logger = logging.getLogger(__name__)

# Initialize FastMCP server
print("Initializing FastMCP server", file=sys.stderr)

# Create the FastMCP instance
try:
    mcp = FastMCP(
        "outline-search",
        title="Outline Knowledge Base Search",
        description="Search and retrieve documents from Outline knowledge bases"
    )
    print(f"FastMCP server initialized: {mcp}", file=sys.stderr)
except Exception as e:
    print(f"Failed to initialize FastMCP: {str(e)}", file=sys.stderr)
    raise

# Path for storing credentials
CREDENTIALS_FILE = os.path.expanduser("~/.outline_mcp_credentials.json")

def load_credentials():
    """Load stored credentials if they exist"""
    if os.path.exists(CREDENTIALS_FILE):
        try:
            with open(CREDENTIALS_FILE, 'r') as f:
                return json.load(f)
        except:
            return None
    return None

def save_credentials(outline_url, api_key):
    """Save credentials for future use"""
    os.makedirs(os.path.dirname(CREDENTIALS_FILE), exist_ok=True)
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump({"outline_url": outline_url, "api_key": api_key}, f)

async def search_outline_documents(
    outline_url: str, 
    api_key: str,
    query: str,
    offset: int = 0,
    limit: int = 25,
    status_filter: List[str] = ["published"],
    date_filter: str = "year"
) -> dict[str, Any]:
    """Make a request to the Outline API with proper error handling."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "offset": offset,
        "limit": limit,
        "query": query,
        "statusFilter": status_filter,
        "dateFilter": date_filter
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{outline_url}/api/documents.search", 
                headers=headers,
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

def format_document_result(document: dict) -> str:
    """Format a document result into a readable string."""
    doc = document.get("document", {})
    context = document.get("context", "No context available")
    
    return f"""
Title: {doc.get('title', 'Unknown')}
ID: {doc.get('id', 'Unknown')}
URL ID: {doc.get('urlId', 'Unknown')}
Context: {context}
Created: {doc.get('createdAt', 'Unknown')}
"""

@mcp.tool()
async def search_documents(
    query: str,
    outline_url: str = None,
    api_key: str = None,
    limit: int = 5,
    status_filter: str = "published",
    date_filter: str = "year"
) -> str:
    """Search for documents in Outline.
    
    Args:
        query: Search term
        outline_url: Base URL of your Outline instance (only needed first time)
        api_key: Outline API key (only needed first time)
        limit: Maximum number of results (default: 5)
        status_filter: Filter by status (default: "published")
        date_filter: Filter by date (default: "year")
    """
    # Check environment variables first
    env_url = os.environ.get("OUTLINE_URL")
    env_key = os.environ.get("OUTLINE_API_KEY")
    
    # Try to load stored credentials next
    credentials = load_credentials()
    
    # Use values in this priority: provided directly > environment variables > stored credentials
    final_url = outline_url or env_url or (credentials and credentials.get("outline_url"))
    final_key = api_key or env_key or (credentials and credentials.get("api_key"))
    
    # If no credentials available, inform the user
    if not final_url or not final_key:
        return "Please provide both outline_url and api_key for the first search"
    
    # Save new credentials if provided directly
    if outline_url and api_key:
        save_credentials(outline_url, api_key)
    
    # Continue with search using the credentials
    status_filters = [status_filter]
    
    results = await search_outline_documents(
        outline_url=final_url,
        api_key=final_key,
        query=query,
        limit=limit,
        status_filter=status_filters,
        date_filter=date_filter
    )
    
    if "error" in results:
        return f"Error searching documents: {results['error']}"
    
    if not results.get("data"):
        return "No documents found matching your query."
    
    formatted_results = [format_document_result(doc) for doc in results["data"]]
    return "\n---\n".join(formatted_results)

@mcp.tool()
async def update_credentials(outline_url: str, api_key: str) -> str:
    """Update stored Outline credentials.
    
    Args:
        outline_url: Base URL of your Outline instance
        api_key: Outline API key
    """
    save_credentials(outline_url, api_key)
    return "Credentials updated successfully"

@mcp.tool()
async def ping() -> str:
    """Simple test function to verify the MCP server is working.
    
    Returns:
        A simple status message
    """
    return "Outline MCP server is running correctly"

@mcp.tool()
async def get_document_by_id(document_id: str) -> str:
    """Get full document content by ID.
    
    Args:
        document_id: ID of the document to retrieve
    """
    # Check environment variables first
    env_url = os.environ.get("OUTLINE_URL")
    env_key = os.environ.get("OUTLINE_API_KEY")
    
    # Load stored credentials as fallback
    credentials = load_credentials()
    
    outline_url = env_url or (credentials and credentials.get("outline_url"))
    api_key = env_key or (credentials and credentials.get("api_key"))
    
    if not outline_url or not api_key:
        return "No credentials found. Please use the search_documents tool first to set up credentials or set OUTLINE_URL and OUTLINE_API_KEY environment variables."
    
    # Make API request to get document
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{outline_url}/api/documents.info", 
                headers=headers,
                json={"id": document_id},
                timeout=30.0
            )
            response.raise_for_status()
            document = response.json().get("data", {})
            
            if not document:
                return "Document not found."
            
            # Format document content
            formatted_doc = f"""
Title: {document.get('title', 'Unknown')}
URL ID: {document.get('urlId', 'Unknown')}
Created: {document.get('createdAt', 'Unknown')}
Updated: {document.get('updatedAt', 'Unknown')}

Content:
{document.get('text', 'No content available')}
"""
            return formatted_doc
            
        except Exception as e:
            return f"Error retrieving document: {str(e)}"

def main():
    """Entry point for the MCP server."""
    try:
        # Set up logging configuration first
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stderr),
                logging.FileHandler("outline_mcp_debug.log")
            ]
        )
        
        # Enable MCP library debugging
        logging.getLogger('mcp').setLevel(logging.DEBUG)
        
        # Print to stderr for debugging
        print("Starting Outline MCP server", file=sys.stderr)
        
        # Debug information
        logger.info("Starting Outline MCP server")
        logger.debug(f"Environment vars: OUTLINE_URL={os.environ.get('OUTLINE_URL', 'Not set')}")
        logger.debug(f"Using credentials file: {CREDENTIALS_FILE}")
        
        # List registered tools for debugging
        for tool in mcp.tools.values():
            logger.debug(f"Registered tool: {tool.name}")
        
        # Start the MCP server with better error reporting
        print("Running MCP server on stdio", file=sys.stderr)
        
        # Use proper error handling
        try:
            print("Starting MCP server with stdio transport", file=sys.stderr)
            # Use the synchronous run method instead of the async version
            mcp.run(transport="stdio")
        except KeyboardInterrupt:
            print("MCP server stopped by user", file=sys.stderr)
            sys.exit(0)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error running MCP server: {e}\n{error_details}", file=sys.stderr)
        logger.error(f"Error running MCP server: {e}\n{error_details}")
        sys.exit(1)

if __name__ == "__main__":
    main()