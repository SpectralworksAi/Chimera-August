from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Add parent dir to path to import CHIMERA modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from registry.manager import AgentRegistryManager
from core.auto_janitor import AutoJanitor
from runtime.loop import ExecutionLoop

app = FastAPI(title="CHIMERA Studio API", version="0.5")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize CHIMERA Backend
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
agents_dir = os.path.join(base_dir, 'registry', 'agents')
schema_path = os.path.join(base_dir, 'schemas', 'pion_v1.schema.json')

registry = AgentRegistryManager(agents_dir)
janitor = AutoJanitor(schema_path)
loop = ExecutionLoop(janitor)

class ObjectivePayload(BaseModel):
    objective: str

@app.post("/api/execute")
async def execute_objective(payload: ObjectivePayload):
    objective = payload.objective
    
    # 1. Route to best agent
    agent_id = registry.route_task(objective)
    agent = registry.agents.get(agent_id, {"role": "Unknown"})
    
    # 2. Construct initial PION packet
    packet = {
        "protocol": "CPS/1.0 PION",
        "header": {
            "iteration": 1,
            "source_engine": agent_id,
            "execution_mode": "CCCC"
        },
        "state": {
            "current_objective": objective,
            "active_uncertainty": "None",
            "next_executable_step": "Processing...",
            "held_contradictions": "None",
            "implementation_status": "Routing to agent"
        },
        "payload": {
            "agent_role": agent["role"],
            "system_prompt": agent.get("system_prompt", "")
        }
    }
    
    # 3. Run through execution loop
    final_packet = loop.run_cycle(packet)
    
    return final_packet

# Mount static UI files last
ui_dir = os.path.join(base_dir, 'ui')
app.mount("/", StaticFiles(directory=ui_dir, html=True), name="ui")
