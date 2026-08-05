import json
import uuid
from typing import Dict, Any, List

class n8nBuilder:
    """
    Generates dynamic n8n workflow schemas that can be executed or imported.
    """
    
    def __init__(self, workflow_name: str = "CHIMERA Generated Workflow"):
        self.workflow_name = workflow_name
        self.nodes = []
        self.connections = {}
        
    def add_webhook_trigger(self, path: str = "chimera-hook") -> str:
        """Adds a Webhook node to start the workflow."""
        node_name = "Webhook"
        node = {
            "parameters": {
                "path": path,
                "responseMode": "lastNode",
                "options": {}
            },
            "id": str(uuid.uuid4()),
            "name": node_name,
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 1,
            "position": [250, 300]
        }
        self.nodes.append(node)
        return node_name
        
    def add_http_request(self, url: str, method: str = "GET", depends_on: str = None) -> str:
        """Adds an HTTP request node."""
        node_name = f"HTTP Request - {str(uuid.uuid4())[:8]}"
        node = {
            "parameters": {
                "method": method,
                "url": url,
                "sendQuery": True,
                "queryParameters": {
                    "parameters": [
                        {"name": "query", "value": "={{$json.query}}"}
                    ]
                }
            },
            "id": str(uuid.uuid4()),
            "name": node_name,
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 3,
            "position": [450, 300]
        }
        self.nodes.append(node)
        
        # Link it
        if depends_on:
            if depends_on not in self.connections:
                self.connections[depends_on] = {"main": [[]]}
            
            self.connections[depends_on]["main"][0].append({
                "node": node_name,
                "type": "main",
                "index": 0
            })
            
        return node_name

    def export(self) -> Dict[str, Any]:
        """Returns the full n8n valid JSON workflow."""
        return {
            "meta": {
                "instanceId": "chimera-forge"
            },
            "nodes": self.nodes,
            "connections": self.connections,
            "settings": {},
            "staticData": None,
            "tags": [],
            "name": self.workflow_name,
            "active": False,
            "versionId": str(uuid.uuid4())
        }
