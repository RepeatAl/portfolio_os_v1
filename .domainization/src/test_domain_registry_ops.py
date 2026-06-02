"""
Unit tests for domain registry operations
"""

import pytest
from pathlib import Path
from domain_registry import DomainRegistry


class TestDomainRegistryLoad:
    """Test domain registry loading"""
    
    def test_load_registry_successfully(self):
        """Test that registry loads successfully"""
        registry = DomainRegistry()
        registry.load()
        
        domains = registry.list_domains()
        assert len(domains) == 12  # Should have exactly 12 canonical domains
    
    def test_load_nonexistent_registry_raises_error(self):
        """Test that loading nonexistent registry raises error"""
        registry = DomainRegistry(Path("/nonexistent/path.yaml"))
        
        with pytest.raises(FileNotFoundError):
            registry.load()
    
    def test_all_domains_have_valid_definitions(self):
        """Test that all loaded domains have valid definitions"""
        registry = DomainRegistry()
        registry.load()
        
        for domain in registry.list_domains():
            is_valid, errors = domain.validate()
            assert is_valid, f"Domain {domain.domain_id} is invalid: {errors}"


class TestDomainRegistryQuery:
    """Test domain query methods"""
    
    def test_get_domain_by_id(self):
        """Test retrieving domain by ID"""
        registry = DomainRegistry()
        registry.load()
        
        signals = registry.get_domain('SIGNALS')
        assert signals is not None
        assert signals.domain_id == 'SIGNALS'
        assert signals.name == 'Signal Generation'
    
    def test_get_nonexistent_domain_returns_none(self):
        """Test that getting nonexistent domain returns None"""
        registry = DomainRegistry()
        registry.load()
        
        domain = registry.get_domain('NONEXISTENT')
        assert domain is None
    
    def test_list_all_domains(self):
        """Test listing all domains"""
        registry = DomainRegistry()
        registry.load()
        
        domains = registry.list_domains()
        assert len(domains) == 12
        
        # Check all expected domains are present
        domain_ids = {d.domain_id for d in domains}
        expected_ids = {
            'GOV', 'ARCH', 'SIGNALS', 'SEMANTICS', 'REASONING', 'REPORT',
            'STATE', 'DATA', 'USER', 'DEPLOY', 'MEMORY', 'SIM'
        }
        assert domain_ids == expected_ids
    
    def test_list_core_domains(self):
        """Test listing core reasoning domains"""
        registry = DomainRegistry()
        registry.load()
        
        core_domains = registry.list_core_domains()
        
        # Should have exactly 4 core domains
        assert len(core_domains) == 4
        
        # Check core domain IDs
        core_ids = {d.domain_id for d in core_domains}
        assert core_ids == {'SIGNALS', 'SEMANTICS', 'REASONING', 'REPORT'}
        
        # All should have priority='core'
        for domain in core_domains:
            assert domain.priority == 'core'
            assert domain.is_core_domain()
    
    def test_list_surface_domains(self):
        """Test listing surface domains"""
        registry = DomainRegistry()
        registry.load()
        
        surface_domains = registry.list_surface_domains()
        
        # Should have exactly 8 surface domains
        assert len(surface_domains) == 8
        
        # Check surface domain IDs
        surface_ids = {d.domain_id for d in surface_domains}
        assert surface_ids == {'GOV', 'ARCH', 'STATE', 'DATA', 'USER', 'DEPLOY', 'MEMORY', 'SIM'}
        
        # All should have priority='surface'
        for domain in surface_domains:
            assert domain.priority == 'surface'
            assert not domain.is_core_domain()


class TestDomainRegistryValidation:
    """Test domain assignment validation"""
    
    def test_valid_domain_assignment(self):
        """Test that valid domain assignment passes"""
        registry = DomainRegistry()
        registry.load()
        
        # SIGNALS can own ENGINE
        is_valid, error = registry.validate_domain_assignment('ENGINE', 'SIGNALS')
        assert is_valid
        assert error is None
    
    def test_invalid_domain_assignment(self):
        """Test that invalid domain assignment fails"""
        registry = DomainRegistry()
        registry.load()
        
        # REPORT cannot own DATA_OUT
        is_valid, error = registry.validate_domain_assignment('DATA_OUT', 'REPORT')
        assert not is_valid
        assert error is not None
        assert 'cannot own' in error
    
    def test_nonexistent_domain_assignment(self):
        """Test that nonexistent domain fails validation"""
        registry = DomainRegistry()
        registry.load()
        
        is_valid, error = registry.validate_domain_assignment('ENGINE', 'NONEXISTENT')
        assert not is_valid
        assert error is not None
        assert 'does not exist' in error
    
    def test_get_valid_domains_for_type(self):
        """Test getting valid domains for artifact type"""
        registry = DomainRegistry()
        registry.load()
        
        # Get valid domains for ENGINE
        valid_domains = registry.get_valid_domains_for_type('ENGINE')
        
        # Should include SIGNALS, SEMANTICS, REASONING, REPORT, DATA, MEMORY, SIM, ARCH
        assert 'SIGNALS' in valid_domains
        assert 'SEMANTICS' in valid_domains
        assert 'REASONING' in valid_domains
        assert 'REPORT' in valid_domains
        assert 'DATA' in valid_domains
        
        # Should NOT include USER, DEPLOY, STATE, GOV
        assert 'USER' not in valid_domains
        assert 'DEPLOY' not in valid_domains
        assert 'STATE' not in valid_domains
        assert 'GOV' not in valid_domains
    
    def test_get_valid_domains_for_ssot(self):
        """Test getting valid domains for SSOT type"""
        registry = DomainRegistry()
        registry.load()
        
        valid_domains = registry.get_valid_domains_for_type('SSOT')
        
        # Most domains can own SSOT (except DEPLOY)
        assert len(valid_domains) >= 10
        assert 'DEPLOY' not in valid_domains


class TestCoreReasoningChain:
    """Test core reasoning chain"""
    
    def test_get_core_reasoning_chain(self):
        """Test getting core reasoning chain in order"""
        registry = DomainRegistry()
        registry.load()
        
        chain = registry.get_core_reasoning_chain()
        
        # Should have 4 domains
        assert len(chain) == 4
        
        # Should be in authority order: SIGNALS (1) → SEMANTICS (2) → REASONING (3) → REPORT (4)
        assert chain[0].domain_id == 'SIGNALS'
        assert chain[0].authority_level == 1
        
        assert chain[1].domain_id == 'SEMANTICS'
        assert chain[1].authority_level == 2
        
        assert chain[2].domain_id == 'REASONING'
        assert chain[2].authority_level == 3
        
        assert chain[3].domain_id == 'REPORT'
        assert chain[3].authority_level == 4
    
    def test_authority_levels_are_sequential(self):
        """Test that authority levels are sequential 1-4"""
        registry = DomainRegistry()
        registry.load()
        
        chain = registry.get_core_reasoning_chain()
        
        authority_levels = [d.authority_level for d in chain]
        assert authority_levels == [1, 2, 3, 4]
    
    def test_surface_domains_have_no_authority_level(self):
        """Test that surface domains have no authority level"""
        registry = DomainRegistry()
        registry.load()
        
        surface_domains = registry.list_surface_domains()
        
        for domain in surface_domains:
            assert domain.authority_level is None
            assert domain.get_authority_level() == 999  # Default for surface domains


class TestDomainArtifactTypeRules:
    """Test domain artifact type ownership rules"""
    
    def test_signals_can_own_signal_artifacts(self):
        """Test that SIGNALS can own signal-related artifacts"""
        registry = DomainRegistry()
        registry.load()
        
        signals = registry.get_domain('SIGNALS')
        
        assert signals.can_own_type('SSOT')
        assert signals.can_own_type('ENGINE')
        assert signals.can_own_type('DATA_OUT')
        assert signals.can_own_type('CONFIG')
    
    def test_signals_cannot_own_report_artifacts(self):
        """Test that SIGNALS cannot own report artifacts"""
        registry = DomainRegistry()
        registry.load()
        
        signals = registry.get_domain('SIGNALS')
        
        assert not signals.can_own_type('REPORT_OUT')
        assert not signals.can_own_type('DASHBOARD')
    
    def test_report_can_own_report_artifacts(self):
        """Test that REPORT can own report artifacts"""
        registry = DomainRegistry()
        registry.load()
        
        report = registry.get_domain('REPORT')
        
        assert report.can_own_type('SSOT')
        assert report.can_own_type('ENGINE')
        assert report.can_own_type('REPORT_OUT')
        assert report.can_own_type('CONFIG')
    
    def test_report_cannot_own_data_artifacts(self):
        """Test that REPORT cannot own data artifacts"""
        registry = DomainRegistry()
        registry.load()
        
        report = registry.get_domain('REPORT')
        
        assert not report.can_own_type('DATA_OUT')
        assert not report.can_own_type('DASHBOARD')
    
    def test_deploy_can_only_own_runtime_and_config(self):
        """Test that DEPLOY can only own RUNTIME and CONFIG"""
        registry = DomainRegistry()
        registry.load()
        
        deploy = registry.get_domain('DEPLOY')
        
        assert deploy.can_own_type('RUNTIME')
        assert deploy.can_own_type('CONFIG')
        
        # Cannot own anything else
        assert not deploy.can_own_type('SSOT')
        assert not deploy.can_own_type('ENGINE')
        assert not deploy.can_own_type('REPORT_OUT')
        assert not deploy.can_own_type('DATA_OUT')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
