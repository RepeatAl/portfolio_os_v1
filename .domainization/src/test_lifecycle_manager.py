"""
Unit tests for lifecycle manager operations
"""

import pytest
from pathlib import Path
from lifecycle_manager import LifecycleManager


class TestLifecycleManagerLoad:
    """Test lifecycle manager loading"""
    
    def test_load_state_machines_successfully(self):
        """Test that state machines load successfully"""
        manager = LifecycleManager()
        manager.load()
        
        artifact_types = manager.list_artifact_types()
        assert len(artifact_types) == 11  # Should have 11 artifact types
    
    def test_load_nonexistent_file_raises_error(self):
        """Test that loading nonexistent file raises error"""
        manager = LifecycleManager(Path("/nonexistent/path.yaml"))
        
        with pytest.raises(FileNotFoundError):
            manager.load()
    
    def test_all_state_machines_have_valid_definitions(self):
        """Test that all loaded state machines are valid"""
        manager = LifecycleManager()
        manager.load()
        
        for artifact_type in manager.list_artifact_types():
            state_machine = manager.get_state_machine(artifact_type)
            assert state_machine is not None
            is_valid, errors = state_machine.validate()
            assert is_valid, f"State machine for {artifact_type} is invalid: {errors}"


class TestLifecycleManagerQuery:
    """Test lifecycle manager query methods"""
    
    def test_get_state_machine_by_type(self):
        """Test retrieving state machine by artifact type"""
        manager = LifecycleManager()
        manager.load()
        
        ssot_sm = manager.get_state_machine('SSOT')
        assert ssot_sm is not None
        assert ssot_sm.artifact_type == 'SSOT'
        assert 'draft' in ssot_sm.states
        assert 'canonical' in ssot_sm.states
    
    def test_get_nonexistent_state_machine_returns_none(self):
        """Test that getting nonexistent state machine returns None"""
        manager = LifecycleManager()
        manager.load()
        
        sm = manager.get_state_machine('NONEXISTENT')
        assert sm is None
    
    def test_list_artifact_types(self):
        """Test listing all artifact types"""
        manager = LifecycleManager()
        manager.load()
        
        types = manager.list_artifact_types()
        
        # Check expected types are present
        expected_types = {
            'SSOT', 'ENGINE', 'REPORT_OUT', 'DATA_IN', 'DATA_OUT',
            'RUNTIME', 'DASHBOARD', 'SNAPSHOT', 'CONFIG', 'CALIBRATION', 'STEERING'
        }
        assert set(types) == expected_types
    
    def test_list_states_for_artifact_type(self):
        """Test listing states for an artifact type"""
        manager = LifecycleManager()
        manager.load()
        
        ssot_states = manager.list_states('SSOT')
        assert 'draft' in ssot_states
        assert 'review' in ssot_states
        assert 'canonical' in ssot_states
        assert 'deprecated' in ssot_states
    
    def test_list_states_for_nonexistent_type_returns_empty(self):
        """Test that listing states for nonexistent type returns empty list"""
        manager = LifecycleManager()
        manager.load()
        
        states = manager.list_states('NONEXISTENT')
        assert states == []


class TestLifecycleManagerTransitions:
    """Test lifecycle transition validation"""
    
    def test_valid_transition(self):
        """Test that valid transition passes"""
        manager = LifecycleManager()
        manager.load()
        
        # SSOT: draft -> review is valid
        is_valid, error = manager.validate_transition('SSOT', 'draft', 'review')
        assert is_valid
        assert error is None
    
    def test_invalid_transition(self):
        """Test that invalid transition fails"""
        manager = LifecycleManager()
        manager.load()
        
        # SSOT: draft -> canonical is not a direct transition
        is_valid, error = manager.validate_transition('SSOT', 'draft', 'canonical')
        assert not is_valid
        assert error is not None
        assert 'Invalid transition' in error
    
    def test_validate_transition_for_nonexistent_type(self):
        """Test that validating transition for nonexistent type fails"""
        manager = LifecycleManager()
        manager.load()
        
        is_valid, error = manager.validate_transition('NONEXISTENT', 'draft', 'active')
        assert not is_valid
        assert error is not None
        assert 'No state machine' in error
    
    def test_get_allowed_transitions(self):
        """Test getting allowed transitions from a state"""
        manager = LifecycleManager()
        manager.load()
        
        # SSOT: from draft, can go to review
        allowed = manager.get_allowed_transitions('SSOT', 'draft')
        assert 'review' in allowed
    
    def test_get_allowed_transitions_for_terminal_state(self):
        """Test getting allowed transitions from terminal state"""
        manager = LifecycleManager()
        manager.load()
        
        # SSOT: deprecated has no outgoing transitions
        allowed = manager.get_allowed_transitions('SSOT', 'deprecated')
        assert len(allowed) == 0
    
    def test_get_allowed_transitions_for_nonexistent_type(self):
        """Test that getting allowed transitions for nonexistent type returns empty"""
        manager = LifecycleManager()
        manager.load()
        
        allowed = manager.get_allowed_transitions('NONEXISTENT', 'draft')
        assert allowed == []


class TestLifecycleManagerModifiability:
    """Test artifact modifiability checks"""
    
    def test_is_modifiable_for_modifiable_state(self):
        """Test that modifiable state is recognized"""
        manager = LifecycleManager()
        manager.load()
        
        # SSOT: draft is modifiable
        assert manager.is_modifiable('SSOT', 'draft')
        assert manager.is_modifiable('SSOT', 'review')
        assert manager.is_modifiable('SSOT', 'canonical')
    
    def test_is_not_modifiable_for_read_only_state(self):
        """Test that read-only state is recognized"""
        manager = LifecycleManager()
        manager.load()
        
        # SSOT: deprecated is read-only
        assert not manager.is_modifiable('SSOT', 'deprecated')
    
    def test_is_modifiable_for_nonexistent_type_returns_true(self):
        """Test that nonexistent type defaults to modifiable"""
        manager = LifecycleManager()
        manager.load()
        
        # If no state machine defined, assume modifiable
        assert manager.is_modifiable('NONEXISTENT', 'any_state')
    
    def test_engine_modifiability(self):
        """Test ENGINE artifact modifiability"""
        manager = LifecycleManager()
        manager.load()
        
        # ENGINE: planned, development, active are modifiable
        assert manager.is_modifiable('ENGINE', 'planned')
        assert manager.is_modifiable('ENGINE', 'development')
        assert manager.is_modifiable('ENGINE', 'active')
        
        # ENGINE: deprecated is read-only
        assert not manager.is_modifiable('ENGINE', 'deprecated')
    
    def test_report_out_not_modifiable(self):
        """Test that REPORT_OUT artifacts are never modifiable"""
        manager = LifecycleManager()
        manager.load()
        
        # REPORT_OUT: all states are read-only (generated reports)
        assert not manager.is_modifiable('REPORT_OUT', 'generated')
        assert not manager.is_modifiable('REPORT_OUT', 'current')
        assert not manager.is_modifiable('REPORT_OUT', 'archived')


class TestLifecycleManagerInitialState:
    """Test initial state retrieval"""
    
    def test_get_initial_state_for_ssot(self):
        """Test getting initial state for SSOT"""
        manager = LifecycleManager()
        manager.load()
        
        initial = manager.get_initial_state('SSOT')
        assert initial == 'draft'
    
    def test_get_initial_state_for_engine(self):
        """Test getting initial state for ENGINE"""
        manager = LifecycleManager()
        manager.load()
        
        initial = manager.get_initial_state('ENGINE')
        assert initial == 'planned'
    
    def test_get_initial_state_for_report_out(self):
        """Test getting initial state for REPORT_OUT"""
        manager = LifecycleManager()
        manager.load()
        
        initial = manager.get_initial_state('REPORT_OUT')
        assert initial == 'generated'
    
    def test_get_initial_state_for_nonexistent_type_returns_none(self):
        """Test that getting initial state for nonexistent type returns None"""
        manager = LifecycleManager()
        manager.load()
        
        initial = manager.get_initial_state('NONEXISTENT')
        assert initial is None


class TestLifecycleManagerStateMachineDetails:
    """Test specific state machine details"""
    
    def test_ssot_state_machine(self):
        """Test SSOT state machine details"""
        manager = LifecycleManager()
        manager.load()
        
        ssot = manager.get_state_machine('SSOT')
        
        # Check states
        assert set(ssot.states) == {'draft', 'review', 'canonical', 'deprecated'}
        
        # Check initial state
        assert ssot.initial_state == 'draft'
        
        # Check modifiable states
        assert 'draft' in ssot.modifiable_states
        assert 'review' in ssot.modifiable_states
        assert 'canonical' in ssot.modifiable_states
        
        # Check read-only states
        assert 'deprecated' in ssot.read_only_states
    
    def test_engine_state_machine(self):
        """Test ENGINE state machine details"""
        manager = LifecycleManager()
        manager.load()
        
        engine = manager.get_state_machine('ENGINE')
        
        # Check states
        assert set(engine.states) == {'planned', 'development', 'active', 'deprecated'}
        
        # Check initial state
        assert engine.initial_state == 'planned'
        
        # Check that development can loop to itself
        assert engine.is_valid_transition('development', 'development')
    
    def test_snapshot_state_machine(self):
        """Test SNAPSHOT state machine details"""
        manager = LifecycleManager()
        manager.load()
        
        snapshot = manager.get_state_machine('SNAPSHOT')
        
        # Check states
        assert set(snapshot.states) == {'captured', 'archived'}
        
        # Check initial state
        assert snapshot.initial_state == 'captured'
        
        # Check state classification
        # captured = regenerable (accumulates over time)
        # archived = read-only (frozen forever)
        assert len(snapshot.modifiable_states) == 0
        assert 'captured' in snapshot.regenerable_states
        assert 'archived' in snapshot.read_only_states


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
