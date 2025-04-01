#!/usr/bin/env python3
import os
import subprocess
import sys
import time

def main():
    """Run a simple test that just prints stderr from the MCP server."""
    # Set environment variables for testing
    env = os.environ.copy()
    env["OUTLINE_URL"] = "https://example.com"
    env["OUTLINE_API_KEY"] = "test_key"
    
    # Run the MCP server directly without IPC
    print("Starting MCP server process...")
    
    # Use a simpler process that just captures stderr
    process = subprocess.Popen(
        ["python", "-m", "outline_mcp.outline"],
        stderr=subprocess.PIPE,
        env=env,
        text=True
    )
    
    # Wait for a few seconds to see initialization output
    print("Waiting for 3 seconds...")
    time.sleep(3)
    
    # Terminate the process
    print("Terminating process...")
    process.terminate()
    
    # Read stderr
    stderr_output = process.stderr.read()
    
    # Print the stderr output
    print("\n\nSTDERR OUTPUT:")
    print("-" * 50)
    print(stderr_output)
    print("-" * 50)
    
    # Wait for process to exit
    process.wait()
    print(f"Process exited with code: {process.returncode}")

if __name__ == "__main__":
    main()