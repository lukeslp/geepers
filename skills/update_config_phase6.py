import json
import os
from pathlib import Path

config_path = Path("/home/coolhand/.config/Claude/claude_desktop_config.json")

# Load existing
with open(config_path, 'r') as f:
    config = json.load(f)

servers = config.get("mcpServers", {})

# Define Product server
new_servers = {
    "geepers-product": {
        "command": "python3",
        "args": ["/home/coolhand/geepers/skills/source/product/src/server.py"],
        "env": {} 
    }
}

# Add placeholder env vars if missing
if "OPENAI_API_KEY" not in new_servers["geepers-product"]["env"]:
    new_servers["geepers-product"]["env"]["OPENAI_API_KEY"] = "${OPENAI_API_KEY}"
    
if "XAI_API_KEY" not in new_servers["geepers-product"]["env"]:
    new_servers["geepers-product"]["env"]["XAI_API_KEY"] = "${XAI_API_KEY}"

# Update/Merge
servers.update(new_servers)
config["mcpServers"] = servers

# Write back
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

print("Configuration updated with Product Skill.")
