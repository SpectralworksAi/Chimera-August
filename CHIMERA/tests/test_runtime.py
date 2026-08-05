import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.auto_janitor import AutoJanitor
from runtime.loop import ExecutionLoop

def main():
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'schemas', 'pion_v1.schema.json')
    janitor = AutoJanitor(schema_path)
    loop = ExecutionLoop(janitor)
    
    # A dummy initial packet
    packet = {
        "protocol": "CPS/1.0 PION",
        "header": {
            "iteration": 1,
            "source_engine": "CHIMERA_TEST",
            "execution_mode": "OON"
        },
        "state": {
            "current_objective": "Test the runtime loop",
            "active_uncertainty": "None",
            "next_executable_step": "Validate packet",
            "held_contradictions": "None",
            "implementation_status": "Testing"
        },
        "payload": {
            "message": "Hello World"
        }
    }
    
    print("Starting CHIMERA 8.0 Execution Loop Test...")
    final_packet = loop.run_cycle(packet)
    
    print("\n[RESULT] Final Packet:")
    import json
    print(json.dumps(final_packet, indent=2))
    
    # The iteration should be incremented
    assert final_packet["header"]["iteration"] == 2
    print("\n[SUCCESS] Test completed successfully.")

if __name__ == "__main__":
    main()
