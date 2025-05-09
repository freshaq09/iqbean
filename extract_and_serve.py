#!/usr/bin/env python3
import os
import subprocess
import http.server
import socketserver
import webbrowser
from pathlib import Path

def extract_zip():
    """Extract the zip file to the current directory"""
    zip_file = "attached_assets/iqbean_website.zip"
    
    if not os.path.exists(zip_file):
        print(f"Error: Could not find the zip file at {zip_file}")
        return False
    
    print(f"Extracting {zip_file}...")
    
    try:
        # Try using unzip command
        result = subprocess.run(["unzip", zip_file], capture_output=True, text=True)
        
        if result.returncode != 0:
            # If unzip fails, try using tar
            print("unzip command failed, trying tar...")
            result = subprocess.run(["tar", "-xf", zip_file], capture_output=True, text=True)
            
            if result.returncode != 0:
                print("tar command failed. Could not extract the zip file.")
                print(f"Error: {result.stderr}")
                return False
    except FileNotFoundError:
        print("Error: Command not found. Please make sure unzip or tar is installed.")
        return False
    
    print("Extraction completed successfully!")
    return True

def find_index_html():
    """Find index.html file in the extracted directory"""
    # Search for index.html in current directory and subdirectories
    index_files = list(Path(".").glob("**/index.html"))
    
    if not index_files:
        print("Error: Could not find index.html in the extracted files.")
        return None
    
    # Return the parent directory of the first index.html found
    index_path = index_files[0]
    web_root = str(index_path.parent)
    
    print(f"Found index.html at: {index_path}")
    print(f"Using web root directory: {web_root}")
    
    return web_root

def serve_website(web_root):
    """Serve the website using Python's built-in HTTP server"""
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    
    # Change to the web root directory
    os.chdir(web_root)
    
    # Allow reuse of the address
    socketserver.TCPServer.allow_reuse_address = True
    
    # Try port 8000 first, then try other ports if needed
    for port in range(8000, 8010):  # Try ports 8000-8009
        try:
            httpd = socketserver.TCPServer(("0.0.0.0", port), Handler)
            print(f"Serving website at http://localhost:{port}")
            print("Press Ctrl+C to stop the server")
            
            # Serve until interrupted
            httpd.serve_forever()
            return  # Successfully started server
        except OSError as e:
            if e.errno == 98:  # Address already in use
                print(f"Port {port} is already in use, trying next port...")
                continue
            else:
                print(f"Error: {e}")
                return
    
    print("Error: Could not find an available port between 8000-8009.")

def main():
    """Main function to extract and serve the website"""
    print("Starting website extraction and serving process...")
    
    # Skip extraction if the website directory already exists
    if os.path.exists("iqbean_website"):
        print("Website already extracted, skipping extraction step...")
        web_root = "iqbean_website"
    else:
        # Extract the zip file
        if not extract_zip():
            return
        
        # Find the web root directory
        web_root = find_index_html()
        if not web_root:
            return
    
    # Serve the website
    serve_website(web_root)

if __name__ == "__main__":
    main()
