"""
Unit tests for lifecycle state machine validation
"""

import pytest
import yaml
from pathlib import Path


def load_lifecycle_state_machines():
    """Load lifecycle state machines from YAML file"""
    sm_path = Path(__file__).parent.parent / "lifecycle_state_machine.yaml"
    with open(sm_path, 'r') as f:
        return yaml.safe_load(f)


class TestStateMachineSchema:
    """Test state machine schema validation"""
    
    def test_state_machines_load_successfully(self):
        """Test that lifecycle state machine YAML is valid and loads"""
        sm = load_lifecycle_state_machines()
        assert sm is not None
        assert 'artifact_types' in sm
    
    def test_all_11_artifact_types_defined(self):
        """Test that all 11 artifact types have state machines"""
        sm = load_lifecycle_state_machines()
        artifact_types = list(sm['artifact_types'].keys())
        
        expected_types = [
            'SSOT', 'ENGINE', 'REPORT_OUT', 'DATA_IN', 'DATA_OUT',
            'RUNTIME', 'DASHBOARD', 'SNAPSHOT', 'CONFIG', 'CALIBRATION', 'STEERING'
        ]
        
        assert set(artifact_types) == set(expected_types)
    
    def test_each_artifact_type_has_required_fields(self):
        """Test that each artifact type has all required fields"""
        sm = load_lifecycle_state_machines()
        required_fields = [
            'description', 'states', 'initial_state', 'transitions',
            'modifiable_states', 'read_only_states'
        ]
        
        for artifact_type, config in sm['artifact_types'].items():
            for field in required_fields:
                assert field in config, \
                    f"Artifact type {artifact_type} missing field: {field}"
    
    def test_states_is_non_empty_list(self):
        """Test that states is a non-empty list"""
        sm = load_lifecycle_state_machines()
        
        for artifact_type, config in sm['artifact_types'].items():
            assert isinstance(config['states'], list)
            assert len(config['states']) > 0
    
    def test_initial_state_is_in_states(self):
        """Test that initial_state is one of the defined states"""
        sm = load_lifecycle_state_machines()
        
        for artifact_type, config in sm['artifact_types'].items():
            assert config['initial_state'] in config['states'], \
                f"{artifact_type}: initial_state '{config['initial_state']}' not in states"
    
    def test_transitions_is_list(self):
        """Test that transitions is a list"""
        sm = load_lifecycle_state_machines()
        
        for artifact_type, config in sm['artifact_types'].items():
            assert isinstance(config['transitions'], list)
    
    def test_each_transition_has_required_fields(self):
        """Test that each transition has from, to, and condition"""
        sm = load_lifecycle_state_machines()
        
        for artifact_type, config in sm['artifact_types'].items():
            for transition in config['transitions']:
                assert 'from' in transition
                assert 'to' in transition
                assert 'condition' in transition
    
    def test_transition_states_are_valid(self):
        """Test that all transition from/to states exist in states list"""
        sm = load_lifecycle_state_machines()
        
        for artifact_type, config in sm['artifact_types'].items():
            valid_states = set(config['states'])
            
            for transition in config['transitions']:
                assert transition['from'] in valid_states, \
                    f"{artifact_type}: transition from '{transition['from']}' not in states"
                assert transition['to'] in valid_states, \
                    f"{artifact_type}: transition to '{transition['to']}' not in states"
    
    def test_modifiable_and_readonly_states_are_valid(self):
        """Test that modifiable and read_only states exist in states list"""
        sm = load_lifecycle_state_machines()
        
        for artifact_type, config in sm['artifact_types'].items():
            valid_states = set(config['states'])
            
            for state in config['modifiable_states']:
                assert state in valid_states, \
                    f"{artifact_type}: modifiable state '{state}' not in states"
            
            for state in config['read_only_states']:
                assert state in valid_states, \
                    f"{artifact_type}: read_only state '{state}' not in states"
    
    def test_no_state_in_both_modifiable_and_readonly(self):
        """Test that no state appears in both modifiable and read_only"""
        sm = load_lifecycle_state_machines()
        
        for artifact_type, config in sm['artifact_types'].items():
            modifiable = set(config['modifiable_states'])
            readonly = set(config['read_only_states'])
            overlap = modifiable & readonly
            
            assert len(overlap) == 0, \
                f"{artifact_type}: states in both modifiable and read_only: {overlap}"


class TestSSOTStateMachine:
    """Test SSOT artifact type state machine"""
    
    def test_ssot_has_correct_states(self):
        """Test SSOT has draft, review, canonical, deprecated states"""
        sm = load_lifecycle_state_machines()
        ssot = sm['artifact_types']['SSOT']
        
        expected_states = ['draft', 'review', 'canonical', 'deprecated']
        assert set(ssot['states']) == set(expected_states)
    
    def test_ssot_initial_state_is_draft(self):
        """Test SSOT initial state is draft"""
        sm = load_lifecycle_state_machines()
        ssot = sm['artifact_types']['SSOT']
        
        assert ssot['initial_state'] == 'draft'
    
    def test_ssot_deprecated_is_readonly(self):
        """Test SSOT deprecated state is read-only"""
        sm = load_lifecycle_state_machines()
        ssot = sm['artifact_types']['SSOT']
        
        assert 'deprecated' in ssot['read_only_states']
        assert 'deprecated' not in ssot['modifiable_states']
    
    def test_ssot_can_transition_draft_to_review(self):
        """Test SSOT can transition from draft to review"""
        sm = load_lifecycle_state_machines()
        ssot = sm['artifact_types']['SSOT']
        
        transitions = [(t['from'], t['to']) for t in ssot['transitions']]
        assert ('draft', 'review') in transitions
    
    def test_ssot_can_transition_review_to_canonical(self):
        """Test SSOT can transition from review to canonical"""
        sm = load_lifecycle_state_machines()
        ssot = sm['artifact_types']['SSOT']
        
        transitions = [(t['from'], t['to']) for t in ssot['transitions']]
        assert ('review', 'canonical') in transitions
    
    def test_ssot_can_transition_canonical_to_deprecated(self):
        """Test SSOT can transition from canonical to deprecated"""
        sm = load_lifecycle_state_machines()
        ssot = sm['artifact_types']['SSOT']
        
        transitions = [(t['from'], t['to']) for t in ssot['transitions']]
        assert ('canonical', 'deprecated') in transitions


class TestEngineStateMachine:
    """Test ENGINE artifact type state machine"""
    
    def test_engine_has_correct_states(self):
        """Test ENGINE has planned, development, active, deprecated states"""
        sm = load_lifecycle_state_machines()
        engine = sm['artifact_types']['ENGINE']
        
        expected_states = ['planned', 'development', 'active', 'deprecated']
        assert set(engine['states']) == set(expected_states)
    
    def test_engine_initial_state_is_planned(self):
        """Test ENGINE initial state is planned"""
        sm = load_lifecycle_state_machines()
        engine = sm['artifact_types']['ENGINE']
        
        assert engine['initial_state'] == 'planned'
    
    def test_engine_deprecated_is_readonly(self):
        """Test ENGINE deprecated state is read-only"""
        sm = load_lifecycle_state_machines()
        engine = sm['artifact_types']['ENGINE']
        
        assert 'deprecated' in engine['read_only_states']
        assert 'deprecated' not in engine['modifiable_states']
    
    def test_engine_allows_iterative_development(self):
        """Test ENGINE allows development -> development transitions"""
        sm = load_lifecycle_state_machines()
        engine = sm['artifact_types']['ENGINE']
        
        transitions = [(t['from'], t['to']) for t in engine['transitions']]
        assert ('development', 'development') in transitions


class TestReportOutStateMachine:
    """Test REPORT_OUT artifact type state machine"""
    
    def test_report_out_has_correct_states(self):
        """Test REPORT_OUT has extended lifecycle states for governance-aware deprecation (HARDENING 11)"""
        sm = load_lifecycle_state_machines()
        report = sm['artifact_types']['REPORT_OUT']
        
        expected_states = ['generated', 'current', 'deprecated', 'sunset_pending', 'archived', 'superseded']
        assert set(report['states']) == set(expected_states)
    
    def test_report_out_initial_state_is_generated(self):
        """Test REPORT_OUT initial state is generated"""
        sm = load_lifecycle_state_machines()
        report = sm['artifact_types']['REPORT_OUT']
        
        assert report['initial_state'] == 'generated'
    
    def test_report_out_modifiable_states(self):
        """Test REPORT_OUT deprecated and sunset_pending are modifiable (metadata updates during sunset evaluation)"""
        sm = load_lifecycle_state_machines()
        report = sm['artifact_types']['REPORT_OUT']
        
        assert set(report['modifiable_states']) == {'deprecated', 'sunset_pending'}
    
    def test_report_out_regenerable_states(self):
        """Test REPORT_OUT has regenerable states for daily regeneration"""
        sm = load_lifecycle_state_machines()
        report = sm['artifact_types']['REPORT_OUT']
        
        assert set(report['regenerable_states']) == {'generated', 'current'}
    
    def test_report_out_read_only_states(self):
        """Test REPORT_OUT archived and superseded are read-only"""
        sm = load_lifecycle_state_machines()
        report = sm['artifact_types']['REPORT_OUT']
        
        assert set(report['read_only_states']) == {'archived', 'superseded'}
    
    def test_report_out_deprecation_transition(self):
        """Test REPORT_OUT can transition from current to deprecated"""
        sm = load_lifecycle_state_machines()
        report = sm['artifact_types']['REPORT_OUT']
        
        transitions = [(t['from'], t['to']) for t in report['transitions']]
        assert ('current', 'deprecated') in transitions
    
    def test_report_out_sunset_pending_transition(self):
        """Test REPORT_OUT can transition from deprecated to sunset_pending"""
        sm = load_lifecycle_state_machines()
        report = sm['artifact_types']['REPORT_OUT']
        
        transitions = [(t['from'], t['to']) for t in report['transitions']]
        assert ('deprecated', 'sunset_pending') in transitions
    
    def test_report_out_sunset_to_archived_transition(self):
        """Test REPORT_OUT can transition from sunset_pending to archived"""
        sm = load_lifecycle_state_machines()
        report = sm['artifact_types']['REPORT_OUT']
        
        transitions = [(t['from'], t['to']) for t in report['transitions']]
        assert ('sunset_pending', 'archived') in transitions
    
    def test_report_out_superseded_transition(self):
        """Test REPORT_OUT can transition from current to superseded"""
        sm = load_lifecycle_state_machines()
        report = sm['artifact_types']['REPORT_OUT']
        
        transitions = [(t['from'], t['to']) for t in report['transitions']]
        assert ('current', 'superseded') in transitions
    
    def test_report_out_legacy_archival_transition(self):
        """Test REPORT_OUT retains legacy current to archived transition"""
        sm = load_lifecycle_state_machines()
        report = sm['artifact_types']['REPORT_OUT']
        
        transitions = [(t['from'], t['to']) for t in report['transitions']]
        assert ('current', 'archived') in transitions
    
    def test_report_out_current_state_valid(self):
        """Test that 'current' remains a valid state (existing artifacts won't break)"""
        sm = load_lifecycle_state_machines()
        report = sm['artifact_types']['REPORT_OUT']
        
        assert 'current' in report['states']


class TestDataStateMachines:
    """Test DATA_IN and DATA_OUT state machines"""
    
    def test_data_in_has_correct_states(self):
        """Test DATA_IN has active, stale, archived states"""
        sm = load_lifecycle_state_machines()
        data_in = sm['artifact_types']['DATA_IN']
        
        expected_states = ['active', 'stale', 'archived']
        assert set(data_in['states']) == set(expected_states)
    
    def test_data_out_has_correct_states(self):
        """Test DATA_OUT has generated, current, archived states"""
        sm = load_lifecycle_state_machines()
        data_out = sm['artifact_types']['DATA_OUT']
        
        expected_states = ['generated', 'current', 'archived']
        assert set(data_out['states']) == set(expected_states)
    
    def test_data_out_all_states_readonly(self):
        """Test DATA_OUT all states are read-only (generated artifacts)"""
        sm = load_lifecycle_state_machines()
        data_out = sm['artifact_types']['DATA_OUT']
        
        assert len(data_out['modifiable_states']) == 0


class TestRuntimeAndDashboardStateMachines:
    """Test RUNTIME and DASHBOARD state machines"""
    
    def test_runtime_has_correct_states(self):
        """Test RUNTIME has development, active, deprecated states"""
        sm = load_lifecycle_state_machines()
        runtime = sm['artifact_types']['RUNTIME']
        
        expected_states = ['development', 'active', 'deprecated']
        assert set(runtime['states']) == set(expected_states)
    
    def test_dashboard_has_correct_states(self):
        """Test DASHBOARD has development, active, deprecated states"""
        sm = load_lifecycle_state_machines()
        dashboard = sm['artifact_types']['DASHBOARD']
        
        expected_states = ['development', 'active', 'deprecated']
        assert set(dashboard['states']) == set(expected_states)


class TestSnapshotStateMachine:
    """Test SNAPSHOT artifact type state machine"""
    
    def test_snapshot_has_correct_states(self):
        """Test SNAPSHOT has captured, archived states"""
        sm = load_lifecycle_state_machines()
        snapshot = sm['artifact_types']['SNAPSHOT']
        
        expected_states = ['captured', 'archived']
        assert set(snapshot['states']) == set(expected_states)
    
    def test_snapshot_all_states_readonly(self):
        """Test SNAPSHOT all states are read-only (historical data)"""
        sm = load_lifecycle_state_machines()
        snapshot = sm['artifact_types']['SNAPSHOT']
        
        assert len(snapshot['modifiable_states']) == 0


class TestConfigAndCalibrationStateMachines:
    """Test CONFIG and CALIBRATION state machines"""
    
    def test_config_has_correct_states(self):
        """Test CONFIG has draft, active, deprecated states"""
        sm = load_lifecycle_state_machines()
        config = sm['artifact_types']['CONFIG']
        
        expected_states = ['draft', 'active', 'deprecated']
        assert set(config['states']) == set(expected_states)
    
    def test_calibration_has_correct_states(self):
        """Test CALIBRATION has draft, active, superseded states"""
        sm = load_lifecycle_state_machines()
        calibration = sm['artifact_types']['CALIBRATION']
        
        expected_states = ['draft', 'active', 'superseded']
        assert set(calibration['states']) == set(expected_states)


class TestSteeringStateMachine:
    """Test STEERING artifact type state machine"""
    
    def test_steering_has_correct_states(self):
        """Test STEERING has draft, active, deprecated states"""
        sm = load_lifecycle_state_machines()
        steering = sm['artifact_types']['STEERING']
        
        expected_states = ['draft', 'active', 'deprecated']
        assert set(steering['states']) == set(expected_states)
    
    def test_steering_deprecated_is_readonly(self):
        """Test STEERING deprecated state is read-only"""
        sm = load_lifecycle_state_machines()
        steering = sm['artifact_types']['STEERING']
        
        assert 'deprecated' in steering['read_only_states']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
