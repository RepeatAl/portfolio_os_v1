"""
Lifecycle state machine schema and validation
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class StateTransition:
    """Represents a valid state transition"""
    
    from_state: str
    to_state: str
    condition: str  # Human-readable description of when this transition occurs
    
    def validate(self) -> tuple[bool, List[str]]:
        """
        Validate state transition
        
        Returns:
            (is_valid, error_messages)
        """
        errors = []
        
        if not self.from_state:
            errors.append("from_state is required")
        if not self.to_state:
            errors.append("to_state is required")
        if not self.condition:
            errors.append("condition is required")
        
        return (len(errors) == 0, errors)


@dataclass
class StateMachine:
    """Represents a lifecycle state machine for an artifact type"""
    
    artifact_type: str
    description: str
    states: List[str]
    initial_state: str
    transitions: List[StateTransition]
    modifiable_states: List[str]
    read_only_states: List[str]
    regenerable_states: Optional[List[str]] = None
    
    def validate(self) -> tuple[bool, List[str]]:
        """
        Validate state machine definition
        
        Returns:
            (is_valid, error_messages)
        """
        errors = []
        
        # Check required fields
        if not self.artifact_type:
            errors.append("artifact_type is required")
        if not self.description:
            errors.append("description is required")
        if not self.states:
            errors.append("states is required and must not be empty")
        if not self.initial_state:
            errors.append("initial_state is required")
        if self.modifiable_states is None:
            errors.append("modifiable_states is required (can be empty list)")
        if self.read_only_states is None:
            errors.append("read_only_states is required (can be empty list)")
        
        # Validate lists are actually lists
        if self.states and not isinstance(self.states, list):
            errors.append("states must be a list")
        if self.transitions and not isinstance(self.transitions, list):
            errors.append("transitions must be a list")
        if self.modifiable_states and not isinstance(self.modifiable_states, list):
            errors.append("modifiable_states must be a list")
        if self.read_only_states and not isinstance(self.read_only_states, list):
            errors.append("read_only_states must be a list")
        if self.regenerable_states and not isinstance(self.regenerable_states, list):
            errors.append("regenerable_states must be a list")
        
        # Validate initial_state is in states
        if self.initial_state and self.states and self.initial_state not in self.states:
            errors.append(f"initial_state '{self.initial_state}' must be in states list")
        
        # Validate all modifiable_states are in states
        if self.modifiable_states and self.states:
            invalid_states = set(self.modifiable_states) - set(self.states)
            if invalid_states:
                errors.append(f"modifiable_states contains invalid states: {invalid_states}")
        
        # Validate all read_only_states are in states
        if self.read_only_states and self.states:
            invalid_states = set(self.read_only_states) - set(self.states)
            if invalid_states:
                errors.append(f"read_only_states contains invalid states: {invalid_states}")
        
        # Validate all regenerable_states are in states
        if self.regenerable_states and self.states:
            invalid_states = set(self.regenerable_states) - set(self.states)
            if invalid_states:
                errors.append(f"regenerable_states contains invalid states: {invalid_states}")
        
        # Validate modifiable and read_only don't overlap
        if self.modifiable_states and self.read_only_states:
            overlap = set(self.modifiable_states) & set(self.read_only_states)
            if overlap:
                errors.append(f"States cannot be both modifiable and read-only: {overlap}")
        
        # Validate all states are classified (modifiable, read_only, or regenerable)
        if self.states and self.modifiable_states is not None and self.read_only_states is not None:
            all_classified = set(self.modifiable_states) | set(self.read_only_states)
            if self.regenerable_states:
                all_classified |= set(self.regenerable_states)
            unclassified = set(self.states) - all_classified
            if unclassified:
                errors.append(f"States must be classified as modifiable or read-only: {unclassified}")
        
        # Validate transitions
        if self.transitions:
            for i, transition in enumerate(self.transitions):
                trans_valid, trans_errors = transition.validate()
                if not trans_valid:
                    errors.extend([f"Transition {i}: {e}" for e in trans_errors])
                
                # Validate transition states are in states list
                if self.states:
                    if transition.from_state not in self.states:
                        errors.append(f"Transition {i}: from_state '{transition.from_state}' not in states list")
                    if transition.to_state not in self.states:
                        errors.append(f"Transition {i}: to_state '{transition.to_state}' not in states list")
        
        return (len(errors) == 0, errors)
    
    def is_valid_transition(self, from_state: str, to_state: str) -> bool:
        """
        Check if transition from one state to another is allowed
        
        Args:
            from_state: Current state
            to_state: Target state
        
        Returns:
            True if transition is valid, False otherwise
        """
        for transition in self.transitions:
            if transition.from_state == from_state and transition.to_state == to_state:
                return True
        return False
    
    def get_allowed_transitions(self, current_state: str) -> List[str]:
        """
        Get list of valid next states from current state
        
        Args:
            current_state: Current state
        
        Returns:
            List of valid next states
        """
        return [t.to_state for t in self.transitions if t.from_state == current_state]
    
    def get_initial_state(self) -> str:
        """
        Get initial state for new artifacts of this type
        
        Returns:
            Initial state
        """
        return self.initial_state
    
    def is_modifiable(self, lifecycle_status: str) -> bool:
        """
        Check if artifact can be modified in given lifecycle state
        
        Args:
            lifecycle_status: Current lifecycle state
        
        Returns:
            True if artifact can be modified, False if read-only
        """
        return lifecycle_status in self.modifiable_states


def validate_state_machine_dict(sm_dict: dict) -> tuple[bool, List[str]]:
    """
    Validate state machine dictionary against schema
    
    Args:
        sm_dict: Dictionary containing state machine definition
    
    Returns:
        (is_valid, error_messages)
    """
    errors = []
    
    # Check required fields exist
    required_fields = [
        'description', 'states', 'initial_state',
        'transitions', 'modifiable_states', 'read_only_states'
    ]
    
    for field in required_fields:
        if field not in sm_dict:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        return (False, errors)
    
    # Parse transitions
    try:
        transitions = []
        for trans_dict in sm_dict.get('transitions', []):
            transition = StateTransition(
                from_state=trans_dict.get('from'),
                to_state=trans_dict.get('to'),
                condition=trans_dict.get('condition', '')
            )
            transitions.append(transition)
        
        # Create state machine object and validate
        # Note: artifact_type should be provided separately
        state_machine = StateMachine(
            artifact_type=sm_dict.get('artifact_type', 'UNKNOWN'),
            description=sm_dict['description'],
            states=sm_dict['states'],
            initial_state=sm_dict['initial_state'],
            transitions=transitions,
            modifiable_states=sm_dict['modifiable_states'],
            read_only_states=sm_dict['read_only_states']
        )
        
        return state_machine.validate()
    
    except Exception as e:
        return (False, [f"Error creating state machine object: {str(e)}"])
