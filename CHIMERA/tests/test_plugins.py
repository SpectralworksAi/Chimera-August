import sys
import os
import json

# Add parent dir to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from plugins.manager import PluginManager

def main():
    plugins_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'plugins'))
    print("Initializing Plugin Manager...")
    manager = PluginManager(plugins_dir)
    
    # Simulate a payload extracted from a PION packet
    payload = {
        "a": 15,
        "b": 27
    }
    
    print(f"\nAttempting to execute 'math_addition' plugin with payload: {payload}")
    
    try:
        result = manager.execute_plugin("math_addition", payload)
        print("\n[RESULT] Plugin Execution Output:")
        print(json.dumps(result, indent=2))
        
        assert result["result"] == 42
        print("\n[SUCCESS] Test completed successfully.")
    except Exception as e:
        print(f"\n[ERROR] Plugin execution failed: {e}")

if __name__ == "__main__":
    main()
