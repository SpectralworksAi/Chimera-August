import urllib.request
import json
from typing import Dict, Any
from .base import CHIMERAPlugin

class n8nExecutorPlugin(CHIMERAPlugin):
    """
    Executes an n8n workflow by hitting its Webhook URL and returning the response.
    """
    
    @property
    def name(self) -> str:
        return "n8n_executor"
        
    @property
    def description(self) -> str:
        return "Triggers an n8n webhook and returns the pipeline output."
        
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "webhook_url": {"type": "string", "format": "uri"},
                "payload": {"type": "object"}
            },
            "required": ["webhook_url", "payload"]
        }
        
    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        webhook_url = payload.get("webhook_url")
        data = payload.get("payload", {})
        
        if not webhook_url:
            return {"status": "error", "message": "Missing webhook_url"}

        try:
            req = urllib.request.Request(webhook_url, method="POST")
            req.add_header('Content-Type', 'application/json')
            
            data_bytes = json.dumps(data).encode('utf-8')
            
            with urllib.request.urlopen(req, data=data_bytes, timeout=10) as response:
                response_text = response.read().decode('utf-8')
                
                try:
                    json_resp = json.loads(response_text)
                except json.JSONDecodeError:
                    json_resp = {"raw": response_text}
                    
                return {
                    "status": "success",
                    "n8n_response": json_resp
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
