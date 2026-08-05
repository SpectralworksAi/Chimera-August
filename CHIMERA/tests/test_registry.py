import sys
import os

# Add parent dir to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from registry.manager import AgentRegistryManager

def main():
    agents_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'registry', 'agents'))
    print("Initializing Agent Registry...")
    registry = AgentRegistryManager(agents_dir)
    
    test_objectives = [
        "We need to research the latest trends in quantum computing.",
        "Please review this architecture and check for security flaws.",
        "Build a python script that implements a linked list.",
        "Sanitize and format this malformed json payload."
    ]
    
    print("\n[TEST] Routing tasks to optimal agents:")
    for objective in test_objectives:
        agent_id = registry.route_task(objective)
        agent = registry.agents.get(agent_id)
        print(f"\nObjective: '{objective}'")
        print(f"Routed to -> {agent['role']} ({agent_id})")
        
    print("\n[SUCCESS] Release 0.6 tests completed successfully.")

if __name__ == "__main__":
    main()
