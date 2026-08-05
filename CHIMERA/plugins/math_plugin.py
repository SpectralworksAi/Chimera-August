from typing import Dict, Any
from .base import CHIMERAPlugin

class MathPlugin(CHIMERAPlugin):
    """
    A simple test plugin that performs basic addition.
    """
    
    @property
    def name(self) -> str:
        return "math_addition"
        
    @property
    def description(self) -> str:
        return "Adds two numbers together."
        
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["a", "b"]
        }
        
    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        a = payload.get("a", 0)
        b = payload.get("b", 0)
        result = a + b
        
        return {
            "original_payload": payload,
            "result": result,
            "status": "success"
        }
