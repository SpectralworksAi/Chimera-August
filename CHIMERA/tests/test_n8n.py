import sys
import os
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# Add parent dir to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from builders.n8n_builder import n8nBuilder
from plugins.manager import PluginManager

# --- MOCK N8N SERVER FOR TESTING ---
class Mockn8nHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        payload = json.loads(post_data.decode('utf-8'))
        
        # Simulate processing
        result = {
            "status": "processed_by_mock_n8n",
            "received_data": payload,
            "mock_insight": "CHIMERA integration successful!"
        }
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode('utf-8'))
        
    def log_message(self, format, *args):
        pass # Suppress logging

def start_mock_server():
    server = HTTPServer(('localhost', 8080), Mockn8nHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server

def main():
    print("Starting Mock n8n Webhook Server on localhost:8080...")
    server = start_mock_server()
    
    # 1. Build a workflow
    print("\n[PHASE 1] Building dynamic n8n Workflow...")
    builder = n8nBuilder("Agentic Research Pipeline")
    trigger = builder.add_webhook_trigger("chimera-hook")
    builder.add_http_request("https://api.github.com", depends_on=trigger)
    
    workflow_json = builder.export()
    
    workflows_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'workflows'))
    workflow_path = os.path.join(workflows_dir, 'test_workflow.json')
    
    with open(workflow_path, 'w') as f:
        json.dump(workflow_json, f, indent=2)
        
    print(f"Generated n8n workflow saved to: {workflow_path}")
    
    # 2. Execute the workflow via Plugin
    print("\n[PHASE 2] Executing workflow via CHIMERA Plugin SDK...")
    plugins_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'plugins'))
    manager = PluginManager(plugins_dir)
    
    payload = {
        "webhook_url": "http://localhost:8080/chimera-hook",
        "payload": {
            "query": "Test integration"
        }
    }
    
    result = manager.execute_plugin("n8n_executor", payload)
    
    print("\n[RESULT] n8n Execution Output:")
    print(json.dumps(result, indent=2))
    
    assert result["status"] == "success"
    print("\n[SUCCESS] Release 0.4 tests completed successfully.")
    
    server.shutdown()

if __name__ == "__main__":
    main()
