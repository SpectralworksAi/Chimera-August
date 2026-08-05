import os
import json
from typing import Dict, Any, Optional

class AgentRegistryManager:
    """
    Loads agent profiles and routes tasks to the best-suited agent.
    """
    
    def __init__(self, agents_dir: str):
        self.agents_dir = agents_dir
        self.agents: Dict[str, Dict[str, Any]] = {}
        self._load_agents()
        
    def _load_agents(self):
        """Loads all agent JSON definitions from the registry directory."""
        if not os.path.exists(self.agents_dir):
            return
            
        for filename in os.listdir(self.agents_dir):
            if filename.endswith(".json"):
                path = os.path.join(self.agents_dir, filename)
                with open(path, 'r') as f:
                    try:
                        agent = json.load(f)
                        if "id" in agent:
                            self.agents[agent["id"]] = agent
                            print(f"[Registry] Loaded agent: {agent['role']} ({agent['id']})")
                    except json.JSONDecodeError:
                        print(f"[Registry] Failed to parse {filename}")

    def route_task(self, objective: str) -> Optional[str]:
        """
        Selects the best agent for the given objective using a simple keyword scoring heuristic.
        Returns the agent ID.
        """
        best_agent_id = None
        highest_score = -1
        
        objective_lower = objective.lower()
        
        for agent_id, agent in self.agents.items():
            score = 0
            for cap in agent.get("capabilities", []):
                if cap.lower() in objective_lower:
                    score += 1
                    
            # Tie breaker: if no capabilities match, give a baseline score of 0 instead of -1
            if score > highest_score:
                highest_score = score
                best_agent_id = agent_id
                
        if highest_score == 0 and len(self.agents) > 0:
            # Fallback to the first available agent if no keywords match perfectly
            best_agent_id = list(self.agents.keys())[0]
            
        return best_agent_id
