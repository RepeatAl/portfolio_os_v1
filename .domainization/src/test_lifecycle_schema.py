"""
Unit tests for lifecycle state machine schema
"""

import pytest
from lifecycle_schema import StateTransition, StateMachine, validate_state_machine_dict


class TestStateTransitionValidation:
    """Test StateTransition validation"""
    
    def test_valid_transition_passes_validation(self):
        """Test that valid transition passes validation"""
        transition = StateTransition(
            from_state='draft',
            to_state='review',
            condition='Author completes initial version'
        )
        
        is_valid, errors = transition.validate()
        assert is_valid
        assert len(errors) == 0
    
    def test_missing_from_state_fails_validation(self):
        """Test that missing from_state fails validation"""
        transition = StateTransition(
            from_state='',
            to_state='review',
            condition='Author completes initial version'
        )
        
        is_valid, errors = transition.validate()
        assert not is_valid
        assert any('from_state' in error for error in errors)
    
    def test_missing_to_state_fails_validation(self):
        """Test that missing to_state fails validation"""
        transition = StateTransition(
            from_state='draft',
            to_state='',
            condition='Author completes initial version'
        )
        
        is_valid, errors = transition.validate()
        assert not is_valid
        assert any('to_state' in error for error in errors)
    
    def test_missing_condition_fails_validation(self):
        """Test that missing condition fails validation"""
        transition = StateTransition(
            from_state='draft',
            to_state='review',
            condition=''
        )
        
        is_valid, errors = transition.validate()
        assert not is_valid
        assert any('condition' in error for error in errors)


class TestStateMachineValidation:
    """Test StateMachine validation"""
    
    def test_valid_state_machine_passes_validation(self):
        """Test that valid state machine passes validation"""
        transitions = [
            StateTransition('draft', 'review', 'Author completes'),
            StateTransition('review', 'canonical', 'Domain owner approves'),
            StateTransition('canonical', 'deprecated', 'Superseded')
        ]
        
        state_machine = StateMachine(
            artifact_type='SSOT',
            description='Single source of truth documents',
            states=['draft', 'review', 'canonical', 'deprecated'],
            initial_state='draft',
            transitions=transitions,
            modifiable_states=['draft', 'review', 'canonical'],
            read_only_states=['deprecated']
        )
        
        is_valid, errors = state_machine.validate()
        assert is_valid
        assert len(errors) == 0
    
    def test_missing_artifact_type_fails_validation(self):
        """Test that missing artifact_type fails validation"""
        state_machine = StateMachine(
            artifact_type='',
            description='Test',
            states=['draft', 'active'],
            initial_state='draft',
            transitions=[],
            modifiable_states=['draft', 'active'],
            read_only_states=[]
        )
        
        is_valid, errors = state_machine.validate()
        assert not is_valid
        assert any('artifact_type' in error for error in errors)
    
    def test_empty_states_fails_validation(self):
        """Test that empty states list fails validation"""
        state_machine = StateMachine(
            artifact_type='TEST',
            description='Test',
            states=[],
            initial_state='draft',
            transitions=[],
            modifiable_states=[],
            read_only_states=[]
        )
        
        is_valid, errors = state_machine.validate()
        assert not is_valid
        assert any('states' in error for error in errors)
    
    def test_initial_state_not_in_states_fails_validation(self):
        """Test that initial_state not in states fails validation"""
        state_machine = StateMachine(
            artifact_type='TEST',
            description='Test',
            states=['draft', 'active'],
            initial_state='invalid',  # Not in states
            transitions=[],
            modifiable_states=['draft', 'active'],
            read_only_states=[]
        )
        
        is_valid, errors = state_machine.validate()
        assert not is_valid
        assert any('initial_state' in error and 'must be in states' in error for error in errors)
    
    def test_invalid_modifiable_state_fails_validation(self):
        """Test that modifiable_state not in states fails validation"""
        state_machine = StateMachine(
            artifact_type='TEST',
            description='Test',
            states=['draft', 'active'],
            initial_state='draft',
            transitions=[],
            modifiable_states=['draft', 'invalid'],  # 'invalid' not in states
            read_only_states=[]
        )
        
        is_valid, errors = state_machine.validate()
        assert not is_valid
        assert any('modifiable_states' in error and 'invalid states' in error for error in errors)
    
    def test_invalid_read_only_state_fails_validation(self):
        """Test that read_only_state not in states fails validation"""
        state_machine = StateMachine(
            artifact_type='TEST',
            description='Test',
            states=['draft', 'active'],
            initial_state='draft',
            transitions=[],
            modifiable_states=['draft'],
            read_only_states=['invalid']  # 'invalid' not in states
        )
        
        is_valid, errors = state_machine.validate()
        assert not is_valid
        assert any('read_only_states' in error and 'invalid states' in error for error in errors)
    
    def test_overlapping_modifiable_and_read_only_fails_validation(self):
        """Test that overlapping modifiable and read_only fails validation"""
        state_machine = StateMachine(
            artifact_type='TEST',
            description='Test',
            states=['draft', 'active'],
            initial_state='draft',
            transitions=[],
            modifiable_states=['draft', 'active'],
            read_only_states=['active']  # Overlap with modifiable
        )
        
        is_valid, errors = state_machine.validate()
        assert not is_valid
        assert any('both modifiable and read-only' in error for error in errors)
    
    def test_unclassified_state_fails_validation(self):
        """Test that state not in modifiable or read_only fails validation"""
        state_machine = StateMachine(
            artifact_type='TEST',
            description='Test',
            states=['draft', 'active', 'deprecated'],
            initial_state='draft',
            transitions=[],
            modifiable_states=['draft'],
            read_only_states=['deprecated']  # 'active' is unclassified
        )
        
        is_valid, errors = state_machine.validate()
        assert not is_valid
        assert any('must be classified' in error for error in errors)
    
    def test_transition_with_invalid_from_state_fails_validation(self):
        """Test that transition with invalid from_state fails validation"""
        transitions = [
            StateTransition('invalid', 'active', 'Test')  # 'invalid' not in states
        ]
        
        state_machine = StateMachine(
            artifact_type='TEST',
            description='Test',
            states=['draft', 'active'],
            initial_state='draft',
            transitions=transitions,
            modifiable_states=['draft', 'active'],
            read_only_states=[]
        )
        
        is_valid, errors = state_machine.validate()
        assert not is_valid
        assert any('from_state' in error and 'not in states' in error for error in errors)
    
    def test_transition_with_invalid_to_state_fails_validation(self):
        """Test that transition with invalid to_state fails validation"""
        transitions = [
            StateTransition('draft', 'invalid', 'Test')  # 'invalid' not in states
        ]
        
        state_machine = StateMachine(
            artifact_type='TEST',
            description='Test',
            states=['draft', 'active'],
            initial_state='draft',
            transitions=transitions,
            modifiable_states=['draft', 'active'],
            read_only_states=[]
        )
        
        is_valid, errors = state_machine.validate()
        assert not is_valid
        assert any('to_state' in error and 'not in states' in error for error in errors)


class TestStateMachineMethods:
    """Test StateMachine methods"""
    
    def test_is_valid_transition_for_valid_transition(self):
        """Test that valid transition is recognized"""
        transitions = [
            StateTransition('draft', 'review', 'Author completes'),
            StateTransition('review', 'canonical', 'Domain owner approves'),
            StateTransition('canonical', 'deprecated', 'Superseded')
        ]
        
        state_machine = StateMachine(
            artifact_type='SSOT',
            description='Test',
            states=['draft', 'review', 'canonical', 'deprecated'],
            initial_state='draft',
            transitions=transitions,
            modifiable_states=['draft', 'review', 'canonical'],
            read_only_states=['deprecated']
        )
        
        assert state_machine.is_valid_transition('draft', 'review')
        assert state_machine.is_valid_transition('review', 'canonical')
        assert state_machine.is_valid_transition('canonical', 'deprecated')
    
    def test_is_valid_transition_for_invalid_transition(self):
        """Test that invalid transition is rejected"""
        transitions = [
            StateTransition('draft', 'review', 'Author completes'),
            StateTransition('review', 'canonical', 'Domain owner approves')
        ]
        
        state_machine = StateMachine(
            artifact_type='SSOT',
            description='Test',
            states=['draft', 'review', 'canonical'],
            initial_state='draft',
            transitions=transitions,
            modifiable_states=['draft', 'review', 'canonical'],
            read_only_states=[]
        )
        
        assert not state_machine.is_valid_transition('draft', 'canonical')  # No direct transition
        assert not state_machine.is_valid_transition('canonical', 'draft')  # No reverse transition
    
    def test_get_allowed_transitions(self):
        """Test getting allowed transitions from a state"""
        transitions = [
            StateTransition('draft', 'review', 'Author completes'),
            StateTransition('draft', 'deprecated', 'Abandoned'),
            StateTransition('review', 'canonical', 'Approved'),
            StateTransition('review', 'draft', 'Revisions needed')
        ]
        
        state_machine = StateMachine(
            artifact_type='SSOT',
            description='Test',
            states=['draft', 'review', 'canonical', 'deprecated'],
            initial_state='draft',
            transitions=transitions,
            modifiable_states=['draft', 'review', 'canonical'],
            read_only_states=['deprecated']
        )
        
        draft_transitions = state_machine.get_allowed_transitions('draft')
        assert set(draft_transitions) == {'review', 'deprecated'}
        
        review_transitions = state_machine.get_allowed_transitions('review')
        assert set(review_transitions) == {'canonical', 'draft'}
        
        canonical_transitions = state_machine.get_allowed_transitions('canonical')
        assert len(canonical_transitions) == 0  # No transitions defined
    
    def test_get_initial_state(self):
        """Test getting initial state"""
        state_machine = StateMachine(
            artifact_type='SSOT',
            description='Test',
            states=['draft', 'review', 'canonical'],
            initial_state='draft',
            transitions=[],
            modifiable_states=['draft', 'review', 'canonical'],
            read_only_states=[]
        )
        
        assert state_machine.get_initial_state() == 'draft'
    
    def test_is_modifiable_for_modifiable_state(self):
        """Test that modifiable state is recognized"""
        state_machine = StateMachine(
            artifact_type='SSOT',
            description='Test',
            states=['draft', 'active', 'deprecated'],
            initial_state='draft',
            transitions=[],
            modifiable_states=['draft', 'active'],
            read_only_states=['deprecated']
        )
        
        assert state_machine.is_modifiable('draft')
        assert state_machine.is_modifiable('active')
    
    def test_is_modifiable_for_read_only_state(self):
        """Test that read-only state is recognized"""
        state_machine = StateMachine(
            artifact_type='SSOT',
            description='Test',
            states=['draft', 'active', 'deprecated'],
            initial_state='draft',
            transitions=[],
            modifiable_states=['draft', 'active'],
            read_only_states=['deprecated']
        )
        
        assert not state_machine.is_modifiable('deprecated')


class TestValidateStateMachineDict:
    """Test validate_state_machine_dict function"""
    
    def test_valid_state_machine_dict_passes_validation(self):
        """Test that valid state machine dict passes validation"""
        sm_dict = {
            'artifact_type': 'SSOT',
            'description': 'Single source of truth documents',
            'states': ['draft', 'review', 'canonical'],
            'initial_state': 'draft',
            'transitions': [
                {'from': 'draft', 'to': 'review', 'condition': 'Author completes'}
            ],
            'modifiable_states': ['draft', 'review', 'canonical'],
            'read_only_states': []
        }
        
        is_valid, errors = validate_state_machine_dict(sm_dict)
        assert is_valid
        assert len(errors) == 0
    
    def test_missing_required_field_fails_validation(self):
        """Test that missing required field fails validation"""
        sm_dict = {
            'artifact_type': 'SSOT',
            'description': 'Test',
            'states': ['draft', 'active'],
            # Missing initial_state
            'transitions': [],
            'modifiable_states': ['draft', 'active'],
            'read_only_states': []
        }
        
        is_valid, errors = validate_state_machine_dict(sm_dict)
        assert not is_valid
        assert any('initial_state' in error for error in errors)
    
    def test_invalid_state_machine_dict_fails_validation(self):
        """Test that invalid state machine dict fails validation"""
        sm_dict = {
            'artifact_type': 'SSOT',
            'description': 'Test',
            'states': ['draft', 'active'],
            'initial_state': 'invalid',  # Not in states
            'transitions': [],
            'modifiable_states': ['draft', 'active'],
            'read_only_states': []
        }
        
        is_valid, errors = validate_state_machine_dict(sm_dict)
        assert not is_valid
        assert any('initial_state' in error for error in errors)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
