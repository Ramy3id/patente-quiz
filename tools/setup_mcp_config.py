import json
import os

mcp_config = {
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "-y",
        "@executeautomation/playwright-mcp-server"
      ]
    },
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "R:\\Ramy\\PATENTE_PRO_APP",
        "C:\\Users\\Ramy Fahmy\\.gemini\\antigravity\\scratch\\dev-workspace"
      ]
    },
    "command-runner": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-everything"
      ]
    }
  }
}

paths = [
    r"C:\Users\Ramy Fahmy\.gemini\config\mcp_config.json",
    r"C:\Users\Ramy Fahmy\.gemini\config\mcp_settings.json",
    r"C:\Users\Ramy Fahmy\.gemini\antigravity\scratch\dev-workspace\mcp_config.json",
    r"R:\Ramy\PATENTE_PRO_APP\mcp_config.json"
]

for p in paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(mcp_config, f, indent=2, ensure_ascii=False)
    # verify syntax
    with open(p, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    servers = list(loaded.get("mcpServers", {}).keys())
    print(f"Verified JSON: {p} -> Servers: {servers}")

print("All MCP configuration files successfully written and validated.")
