import json
import jsonschema
from typing import Dict, Any, Optional

class AutoJanitor:
    """
    Deterministic CHIMERA Quality Engine Module.
    Sanitizes, repairs, and enforces JSON state packets between AI execution hops.
    """

    def __init__(self, schema_path: str):
        with open(schema_path, 'r') as f:
            self.schema = json.load(f)
            
    def sanitize(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        """
        Attempts to fix common structural drifts in the PION packet before validation.
        """
        # Ensure protocol is set correctly
        if "protocol" not in packet or packet["protocol"] != "CPS/1.0 PION":
            packet["protocol"] = "CPS/1.0 PION"
            
        # Ensure state block exists
        if "state" not in packet:
            packet["state"] = {
                "current_objective": "Unknown",
                "active_uncertainty": "None",
                "next_executable_step": "Awaiting directive",
                "held_contradictions": "None",
                "implementation_status": "Auto-repaired by AutoJanitor"
            }
            
        return packet

    def validate(self, packet: Dict[str, Any]) -> bool:
        """
        Validates the packet against the CPS/1.0 PION schema.
        Returns True if valid, raises an exception otherwise.
        """
        jsonschema.validate(instance=packet, schema=self.schema)
        return True

    def process_packet(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        """
        Full lifecycle: sanitize and then validate.
        """
        cleaned_packet = self.sanitize(packet)
        self.validate(cleaned_packet)
        return cleaned_packet
