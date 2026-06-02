"""
Lifecycle state machine operations
"""

import yaml
from pathlib import Path
from typing import List, Optional, Dict
from lifecycle_schema import StateMachine, StateTransition


class LifecycleManager:
    """Manages lifecycle state machine operations"""
    
    def __init__(self, state_machine_path: Optional[Path] = None):
        """
        Initialize lifecycle manager
        
        Args:
            state_machine_path: Path to lifecycle_state_machine.yaml file
                               If None, uses default path relative to this file
        """
        if state_machine_path is None:
            # Default to .domainization/lifecycle_state_machine.yaml
            self.state_machine_path = Path(__file__).parent.parent / "lifecycle_state_machine.yaml"
        else:
            self.state_machine_path = Path(state_machine_path)
        
        self._state_machines: Dict[str, StateMachine] = {}
        self._loaded = False
    
    def load(self) -> None:
        """Load state machines from YAML file"""
        if not self.state_machine_path.exists():
            raise FileNotFoundError(f"State machine file not found: {self.state_machine_path}")
        
        with open(self.state_machine_path, 'r') as f:
            data = yaml.safe_load(f)
        
        if not data or 'artifact_types' not in data:
            raise ValueError("Invalid state machine format: missing 'artifact_types' key")
        
        # Clear existing state machines
        self._state_machines.clear()
        
        # Load state machines for each artifact type
        for artifact_type, sm_dict in data['artifact_types'].items():
            state_machine = self._dict_to_state_machine(artifact_type, sm_dict)
            
            # Validate state machine
            is_valid, errors = state_machine.validate()
            if not is_valid:
                raise ValueError(f"Invalid state machine for '{artifact_type}': {', '.join(errors)}")
            
            self._state_machines[artifact_type] = state_machine
        
        self._loaded = True
    
    def get_state_machine(self, artifact_type: str) -> Optional[StateMachine]:
        """
        Retrieve state machine for artifact type
        
        Args:
            artifact_type: Artifact type to get state machine for
        
        Returns:
            StateMachine if found, None otherwise
        """
        if not self._loaded:
            self.load()
        
        return self._state_machines.get(artifact_type)
    
    def validate_transition(self, artifact_type: str, from_state: str, to_state: str) -> tuple[bool, Optional[str]]:
        """
        Check if transition is valid for artifact type
        
        Args:
            artifact_type: The artifact type
            from_state: Current state
            to_state: Target state
        
        Returns:
            (is_valid, error_message)
            error_message is None if valid
        """
        if not self._loaded:
            self.load()
        
        # Get state machine
        state_machine = self._state_machines.get(artifact_type)
        if state_machine is None:
            return (False, f"No state machine defined for artifact type '{artifact_type}'")
        
        # Check if transition is valid
        if not state_machine.is_valid_transition(from_state, to_state):
            allowed = state_machine.get_allowed_transitions(from_state)
            if allowed:
                return (False, f"Invalid transition from '{from_state}' to '{to_state}'. Valid transitions: {', '.join(allowed)}")
            else:
                return (False, f"No valid transitions from state '{from_state}'")
        
        return (True, None)
    
    def get_allowed_transitions(self, artifact_type: str, current_state: str) -> List[str]:
        """
        Get valid next states from current state
        
        Args:
            artifact_type: The artifact type
            current_state: Current state
        
        Returns:
            List of valid next states
        """
        if not self._loaded:
            self.load()
        
        state_machine = self._state_machines.get(artifact_type)
        if state_machine is None:
            return []
        
        return state_machine.get_allowed_transitions(current_state)
    
    def is_modifiable(self, artifact_type: str, lifecycle_status: str) -> bool:
        """
        Check if artifact can be modified based on lifecycle state
        
        Args:
            artifact_type: The artifact type
            lifecycle_status: Current lifecycle state
        
        Returns:
            True if artifact can be modified, False if read-only
        """
        if not self._loaded:
            self.load()
        
        state_machine = self._state_machines.get(artifact_type)
        if state_machine is None:
            # If no state machine defined, assume modifiable
            return True
        
        return state_machine.is_modifiable(lifecycle_status)
    
    def get_initial_state(self, artifact_type: str) -> Optional[str]:
        """
        Get initial state for new artifacts of this type
        
        Args:
            artifact_type: The artifact type
        
        Returns:
            Initial state, or None if no state machine defined
        """
        if not self._loaded:
            self.load()
        
        state_machine = self._state_machines.get(artifact_type)
        if state_machine is None:
            return None
        
        return state_machine.get_initial_state()
    
    def list_artifact_types(self) -> List[str]:
        """
        Get list of all artifact types with state machines
        
        Returns:
            List of artifact type IDs
        """
        if not self._loaded:
            self.load()
        
        return list(self._state_machines.keys())
    
    def list_states(self, artifact_type: str) -> List[str]:
        """
        Get list of all states for an artifact type
        
        Args:
            artifact_type: The artifact type
        
        Returns:
            List of state names, or empty list if no state machine defined
        """
        if not self._loaded:
            self.load()
        
        state_machine = self._state_machines.get(artifact_type)
        if state_machine is None:
            return []
        
        return state_machine.states
    
    def _dict_to_state_machine(self, artifact_type: str, sm_dict: dict) -> StateMachine:
        """Convert dictionary to StateMachine object"""
        # Parse transitions
        transitions = []
        for trans_dict in sm_dict.get('transitions', []):
            transition = StateTransition(
                from_state=trans_dict['from'],
                to_state=trans_dict['to'],
                condition=trans_dict.get('condition', '')
            )
            transitions.append(transition)
        
        return StateMachine(
            artifact_type=artifact_type,
            description=sm_dict.get('description', ''),
            states=sm_dict.get('states', []),
            initial_state=sm_dict.get('initial_state', ''),
            transitions=transitions,
            modifiable_states=sm_dict.get('modifiable_states', []),
            read_only_states=sm_dict.get('read_only_states', []),
            regenerable_states=sm_dict.get('regenerable_states')
        )
