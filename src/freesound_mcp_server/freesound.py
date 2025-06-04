import asyncio
import os
import sys
from typing import Optional
import json

import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()
FREESOUND_API_KEY = os.getenv("FREESOUND_API_KEY")
FREESOUND_BASE_URL = "https://freesound.org/apiv2"

mcp = FastMCP("freesound")

@mcp.tool()
async def search_sounds(query: str, max_results: int = 10) -> dict:
    """
    Search Freesound for audio files.
    
    Args:
        query: Search terms (e.g., "thunderstorm", "piano music", "bird sounds")
        max_results: Number of results to return (1-30, default 10)
        
    Returns:
        Dictionary with search results including preview URLs and metadata
    """
    
  
    if max_results < 1: max_results = 1
    elif max_results > 30: max_results = 30
    
    # api https request 
    url = f"{FREESOUND_BASE_URL}/search/text/"
    params = {
        "token": FREESOUND_API_KEY,
        "query": query.strip(),
        "page_size": max_results,
        "fields": "id,name,tags,license,duration,previews,url,username,type,description"
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            formatted_results = format_response(query, max_results, data)

            return formatted_results

    except httpx.HTTPStatusError as e:
        return {"error": f"API error for {url}: {e.response.status_code}"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}
    except Exception as e:
        return {"error": str(e)}
    


def format_response(query: str, max_results: int, data: dict) -> dict:
    
    formatted_results = {
        "query": query,
        "total_found": data.get("count", 0),
        "results_returned": len(data.get("results", [])),
        "sounds": []
    }
    
    for sound in data.get("results", []):
        # truncate description
        description = sound.get("description", "")
        if len(description) > 200: description = description[:200] + "..."
        
        formatted_sound = {
            "id": sound.get("id"),
            "name": sound.get("name"),
            "duration_seconds": sound.get("duration"),
            "description": description,
            "tags": sound.get("tags", []),
            "license": sound.get("license"),
            "file_type": sound.get("type"),
            "uploader": sound.get("username"),
            "freesound_page": sound.get("url"),
            "preview_urls": sound.get("previews", {}),
            "download_info": "Visit the Freesound page to download the full quality file"
        }
        formatted_results["sounds"].append(formatted_sound)
    
    # add pagination info if there are more results
    if data.get("next"): formatted_results["note"] = f"Showing first {max_results} results. There are {data.get('count', 0)} total results available."
    
    # message if no results
    if not formatted_results["sounds"]: formatted_results["message"] = f"No sounds found for '{query}'. Try different search terms or check spelling."

    return formatted_results



# async def run_server():
#     """Run the MCP server using stdio transport"""
#     try:
#         # Start the MCP server
#         await mcp.run()
#     except KeyboardInterrupt:
#         print("Server stopped by user", file=sys.stderr)
#     except Exception as e:
#         print(f"Server error: {e}", file=sys.stderr)
#         sys.exit(1)


def main():
    mcp.run(transport='stdio')


    # """Main entry point for the CLI"""
    # if len(sys.argv) > 1:
    #     if sys.argv[1] in ["--help", "-h"]:
    #         print("Freesound MCP Server - Phase 1")
    #         print("Usage: freesound-mcp")
    #         print()
    #         print("Environment variables required:")
    #         print("  FREESOUND_API_KEY - Get from https://freesound.org/apiv2/apply/")
    #         print()
    #         print("Connect to Claude Desktop by adding this server to your MCP configuration.")
    #         return
    #     elif sys.argv[1] in ["--version", "-v"]:
    #         print("freesound-mcp 0.1.0")
    #         return
    
    # # Validate environment before starting
    # if not FREESOUND_API_KEY or FREESOUND_API_KEY == "your_freesound_api_key_here":
    #     print("Error: Please set your FREESOUND_API_KEY in the .env file", file=sys.stderr)
    #     print("Get your API key from: https://freesound.org/apiv2/apply/", file=sys.stderr)
    #     sys.exit(1)
    
    # print("Starting Freesound MCP Server...", file=sys.stderr)
    # print("Ready to search for audio files!", file=sys.stderr)
    
    # # Run the server
    # asyncio.run(run_server())


if __name__ == "__main__":
    mcp.run(transport='stdio')