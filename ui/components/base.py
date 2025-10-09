"""
Base component class for UI components
"""
import tkinter as tk
from typing import Dict, Any
from abc import ABC, abstractmethod


class UIComponent(ABC):
    """Base class for all UI components"""
    
    def __init__(self, parent: tk.Widget, colors: Dict[str, str], 
                 event_manager, app_state):
        self.parent = parent
        self.colors = colors
        self.event_manager = event_manager
        self.app_state = app_state
        self.frame = None
        
        # 🔄 DEBUG: Log initialization
        print(f"DEBUG {self.__class__.__name__}: Initialized with:")
        print(f"  - event_manager type: {type(event_manager)}")
        print(f"  - app_state type: {type(app_state)}")
        print(f"  - app_state has 'get': {hasattr(app_state, 'get')}")
        print(f"  - app_state has 'set': {hasattr(app_state, 'set')}")
    
    @abstractmethod
    def create(self) -> tk.Frame:
        """Create and return the component's main frame"""
        pass
    
    def destroy(self) -> None:
        """Destroy the component"""
        if self.frame:
            self.frame.destroy()
    
    def show(self) -> None:
        """Show the component"""
        if self.frame:
            self.frame.pack(fill='both', expand=True)
    
    def hide(self) -> None:
        """Hide the component"""
        if self.frame:
            self.frame.pack_forget()
    
    def update_colors(self, colors: Dict[str, str]) -> None:
        """Update component colors"""
        self.colors = colors
        # Subclasses should override to update their widgets