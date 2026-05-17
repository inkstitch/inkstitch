"""
Undo/Redo pure logic manager for Cross Stitch Canvas.
"""

from typing import List, Optional
from .grid_state import GridStateManager

MAX_UNDO_STEPS = 10

class UndoManager:
    """
    Commit to full snapshot stack, but with a hard cap to prevent memory explosion.
    
    UX Contract: Snapshots MUST be taken once per user action (e.g. mouse down),
    not per individual cell change.
    """
    def __init__(self, initial_state: GridStateManager):
        self.undo_stack: List[GridStateManager] = [initial_state.clone()]
        self.redo_stack: List[GridStateManager] = []
        
    def save_state(self, current_state: GridStateManager) -> None:
        """
        Called when a new undoable action is started (e.g., just before drawing).
        """
        self.undo_stack.append(current_state.clone())
        self.redo_stack.clear()
        
        # Enforce memory cap (+1 to keep the baseline state if possible, though stack caps size entirely)
        if len(self.undo_stack) > MAX_UNDO_STEPS + 1:
            self.undo_stack.pop(0)
            
    def can_undo(self) -> bool:
        """Check if undo is possible (must leave at least one past state)."""
        return len(self.undo_stack) > 1
        
    def can_redo(self) -> bool:
        return len(self.redo_stack) > 0
        
    def undo(self, current_state: GridStateManager) -> GridStateManager:
        """
        Reverts to the previous state. Returns the restored state.
        Returns the unchanged current_state if no undo is possible.
        """
        if not self.can_undo():
            return current_state
            
        self.redo_stack.append(current_state.clone())
        previous_state = self.undo_stack.pop()
        return previous_state.clone()

    def redo(self, current_state: GridStateManager) -> GridStateManager:
        """
        Reapplies the next state. Returns the restored state.
        Returns the unchanged current_state if no redo is possible.
        """
        if not self.can_redo():
            return current_state
            
        self.undo_stack.append(current_state.clone())
        next_state = self.redo_stack.pop()
        return next_state.clone()