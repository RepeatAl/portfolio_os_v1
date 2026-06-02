"""
Unit tests for domain registry validation
"""

import pytest
import yaml
from pathlib import Path


def load_domain_registry():
    """Load domain registry from YAML file"""
    registry_path = Path(__file__).parent.parent / "domain_registry.yaml"
    with open(registry_path, 'r') as f:
        return yaml.safe_load(f)


class TestDomainRegistrySchema:
    """Test domain registry schema validation"""
    
    def test_registry_loads_successfully(self):
        """Test that domain registry YAML is valid and loads"""
        registry = load_domain_registry()
        assert registry is not None
        assert 'domains' in registry
    
    def test_has_12_canonical_domains(self):
        """Test that exactly 12 domains are defined"""
        registry = load_domain_registry()
        domains = registry['domains']
        assert len(domains) == 12
    
    def test_all_required_domain_ids_present(self):
        """Test that all 12 canonical domain IDs exist"""
        registry = load_domain_registry()
        domain_ids = [d['domain_id'] for d in registry['domains']]
        
        expected_ids = [
            'GOV', 'ARCH', 'SIGNALS', 'SEMANTICS', 'REASONING', 
            'REPORT', 'STATE', 'DATA', 'USER', 'DEPLOY', 'MEMORY', 'SIM'
        ]
        
        assert set(domain_ids) == set(expected_ids)
    
    def test_each_domain_has_required_fields(self):
        """Test that each domain has all required fields"""
        registry = load_domain_registry()
        required_fields = [
            'domain_id', 'name', 'responsibility_scope', 
            'allowed_artifact_types', 'cannot_own', 'priority', 'authority_level'
        ]
        
        for domain in registry['domains']:
            for field in required_fields:
                assert field in domain, f"Domain {domain.get('domain_id')} missing field: {field}"
    
    def test_domain_ids_are_unique(self):
        """Test that domain IDs are unique"""
        registry = load_domain_registry()
        domain_ids = [d['domain_id'] for d in registry['domains']]
        assert len(domain_ids) == len(set(domain_ids))
    
    def test_allowed_artifact_types_is_list(self):
        """Test that allowed_artifact_types is a list"""
        registry = load_domain_registry()
        for domain in registry['domains']:
            assert isinstance(domain['allowed_artifact_types'], list)
            assert len(domain['allowed_artifact_types']) > 0
    
    def test_cannot_own_is_list(self):
        """Test that cannot_own is a list"""
        registry = load_domain_registry()
        for domain in registry['domains']:
            assert isinstance(domain['cannot_own'], list)
    
    def test_priority_is_valid(self):
        """Test that priority is either 'core' or 'surface'"""
        registry = load_domain_registry()
        valid_priorities = ['core', 'surface']
        
        for domain in registry['domains']:
            assert domain['priority'] in valid_priorities


class TestCoreReasoningChain:
    """Test core reasoning chain configuration"""
    
    def test_core_domains_identified(self):
        """Test that core reasoning domains are marked as priority='core'"""
        registry = load_domain_registry()
        core_domain_ids = ['SIGNALS', 'SEMANTICS', 'REASONING', 'REPORT']
        
        for domain in registry['domains']:
            if domain['domain_id'] in core_domain_ids:
                assert domain['priority'] == 'core'
    
    def test_surface_domains_identified(self):
        """Test that surface domains are marked as priority='surface'"""
        registry = load_domain_registry()
        surface_domain_ids = ['GOV', 'ARCH', 'STATE', 'DATA', 'USER', 'DEPLOY', 'MEMORY', 'SIM']
        
        for domain in registry['domains']:
            if domain['domain_id'] in surface_domain_ids:
                assert domain['priority'] == 'surface'
    
    def test_authority_levels_defined_for_core_domains(self):
        """Test that core reasoning domains have authority levels 1-4"""
        registry = load_domain_registry()
        authority_mapping = {
            'SIGNALS': 1,
            'SEMANTICS': 2,
            'REASONING': 3,
            'REPORT': 4
        }
        
        for domain in registry['domains']:
            if domain['domain_id'] in authority_mapping:
                expected_level = authority_mapping[domain['domain_id']]
                assert domain['authority_level'] == expected_level
    
    def test_surface_domains_have_no_authority_level(self):
        """Test that surface domains have null authority_level"""
        registry = load_domain_registry()
        surface_domain_ids = ['GOV', 'ARCH', 'STATE', 'DATA', 'USER', 'DEPLOY', 'MEMORY', 'SIM']
        
        for domain in registry['domains']:
            if domain['domain_id'] in surface_domain_ids:
                assert domain['authority_level'] is None


class TestDomainBoundaries:
    """Test domain boundary definitions"""
    
    def test_signals_domain_boundaries(self):
        """Test SIGNALS domain can only write structured signals"""
        registry = load_domain_registry()
        signals = next(d for d in registry['domains'] if d['domain_id'] == 'SIGNALS')
        
        # SIGNALS should be able to create signal outputs
        assert 'DATA_OUT' in signals['allowed_artifact_types']
        
        # SIGNALS should NOT be able to create reports or dashboards
        assert 'REPORT_OUT' in signals['cannot_own']
        assert 'DASHBOARD' in signals['cannot_own']
    
    def test_report_domain_boundaries(self):
        """Test REPORT domain can only write human-readable text"""
        registry = load_domain_registry()
        report = next(d for d in registry['domains'] if d['domain_id'] == 'REPORT')
        
        # REPORT should be able to create report outputs
        assert 'REPORT_OUT' in report['allowed_artifact_types']
        
        # REPORT should NOT be able to create data outputs or dashboards
        assert 'DATA_OUT' in report['cannot_own']
        assert 'DASHBOARD' in report['cannot_own']
    
    def test_deploy_domain_boundaries(self):
        """Test DEPLOY domain can only manage runtime and config"""
        registry = load_domain_registry()
        deploy = next(d for d in registry['domains'] if d['domain_id'] == 'DEPLOY')
        
        # DEPLOY should be able to create runtime artifacts
        assert 'RUNTIME' in deploy['allowed_artifact_types']
        
        # DEPLOY should NOT be able to create SSOTs, engines, reports, or data
        assert 'SSOT' in deploy['cannot_own']
        assert 'ENGINE' in deploy['cannot_own']
        assert 'REPORT_OUT' in deploy['cannot_own']
        assert 'DATA_OUT' in deploy['cannot_own']


class TestArtifactTypeConsistency:
    """Test artifact type consistency across domains"""
    
    def test_no_artifact_type_in_both_allowed_and_cannot_own(self):
        """Test that no artifact type appears in both allowed and cannot_own for same domain"""
        registry = load_domain_registry()
        
        for domain in registry['domains']:
            allowed = set(domain['allowed_artifact_types'])
            cannot = set(domain['cannot_own'])
            overlap = allowed & cannot
            
            assert len(overlap) == 0, \
                f"Domain {domain['domain_id']} has overlap: {overlap}"
    
    def test_ssot_allowed_for_most_domains(self):
        """Test that SSOT is allowed for domains that define specifications"""
        registry = load_domain_registry()
        
        # Domains that should be able to create SSOT documents
        ssot_domains = ['GOV', 'ARCH', 'SIGNALS', 'SEMANTICS', 'REASONING', 
                        'REPORT', 'STATE', 'DATA', 'USER', 'MEMORY', 'SIM']
        
        for domain in registry['domains']:
            if domain['domain_id'] in ssot_domains:
                assert 'SSOT' in domain['allowed_artifact_types']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
