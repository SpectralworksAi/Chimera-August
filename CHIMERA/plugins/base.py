from abc import ABC, abstractmethod
from typing import Dict, Any

class CHIMERAPlugin(ABC):
    """
    Abstract Base Class for all CHIMERA Plugins.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """The unique name of the plugin."""
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        """A brief description of what the plugin does."""
        pass
        
    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """Returns the JSON schema expected for the payload."""
        pass
        
    @abstractmethod
    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the plugin logic using the provided payload.
        Returns the mutated or new payload data.
        """
        pass
