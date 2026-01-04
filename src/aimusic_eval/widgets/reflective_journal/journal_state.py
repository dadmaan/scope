"""
Journal State Manager

Manages journal entry state and observer pattern for cross-tab updates.
Handles appending entries and notifying history display to update.

PRESERVED: All data structure schemas - NO MODIFICATIONS
"""


class JournalStateManager:
    """
    Manages reflective journal state and cross-tab communication.

    Responsibilities:
    - Append new journal entries to synthesis_data
    - Notify observers when entries are added (for history display updates)
    - Maintain entry count
    """

    def __init__(self, synthesis_data_ref):
        """
        Initialize state manager with reference to global synthesis_data.

        Args:
            synthesis_data_ref (dict): Reference to global synthesis_data dict
        """
        self.synthesis_data = synthesis_data_ref
        self.observers = []

    def append_entry(self, entry_data):
        """
        Add a new journal entry and notify observers.

        Args:
            entry_data (dict): Complete journal entry with all fields
        """
        # Append to entries list
        if 'reflective_journal' not in self.synthesis_data:
            self.synthesis_data['reflective_journal'] = {
                'entries': [],
                'entry_count': 0
            }

        self.synthesis_data['reflective_journal']['entries'].append(entry_data)
        self.synthesis_data['reflective_journal']['entry_count'] = len(
            self.synthesis_data['reflective_journal']['entries']
        )

        # Notify observers
        self._notify_observers()

    def register_observer(self, callback):
        """
        Register a callback to be notified when entries are added.

        Args:
            callback (function): Function to call when entry added (no args)
        """
        self.observers.append(callback)

    def _notify_observers(self):
        """Notify all registered observers of state change."""
        for callback in self.observers:
            try:
                callback()
            except Exception as e:
                print(f"Observer notification error: {e}")

    def get_entry_count(self):
        """Get current number of journal entries."""
        return self.synthesis_data.get('reflective_journal', {}).get('entry_count', 0)

    def get_entries(self):
        """Get list of all journal entries."""
        return self.synthesis_data.get('reflective_journal', {}).get('entries', [])
