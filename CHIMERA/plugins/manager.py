import importlib
import os
import inspect
from typing import Dict, Any
from .base import CHIMERAPlugin

class PluginManager:
    """
    Dynamically loads and manages CHIMERA plugins.
    """
    def __init__(self, plugin_dir: str):
        self.plugin_dir = plugin_dir
        self.plugins: Dict[str, CHIMERAPlugin] = {}
        self._load_plugins()
        
    def _load_plugins(self):
        """Discovers and loads all plugins in the plugins directory."""
        if not os.path.exists(self.plugin_dir):
            return
            
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and filename not in ["__init__.py", "base.py", "manager.py"]:
                module_name = filename[:-3]
                module = importlib.import_module(f"plugins.{module_name}")
                
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if inspect.isclass(attr) and issubclass(attr, CHIMERAPlugin) and attr is not CHIMERAPlugin:
                        # Instantiate the plugin and register it
                        plugin_instance = attr()
                        self.plugins[plugin_instance.name] = plugin_instance
                        print(f"[PluginManager] Loaded plugin: {plugin_instance.name}")
                        
    def execute_plugin(self, plugin_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Executes a registered plugin by name."""
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin '{plugin_name}' not found.")
            
        plugin = self.plugins[plugin_name]
        print(f"[PluginManager] Executing {plugin.name}...")
        
        # Here we could validate the payload against plugin.get_schema()
        result = plugin.execute(payload)
        return result
