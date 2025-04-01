import logging
import sys
from .server import mcp

def main():
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler("outline_mcp_debug.log"), logging.StreamHandler()]
    )
    logging.debug("Starting Outline MCP server")
    
    try:
        logging.debug("Running MCP server with stdio transport")
        mcp.run(transport='stdio')
    except Exception as e:
        logging.error(f"Error running MCP server: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()