"""
Unit tests for domain definition schema
"""

import pytest
from domain_schema import DomainDefinition, validate_domain_dict


class TestDomainDefinitionValidation:
    """Test DomainDefinition validation"""
    
    def test_valid_core_domain_passes_validation(self):
        """Test that valid core domain passes validation"""
        domain = DomainDefinition(
            domain_id='SIGNALS',
            name='Signal Generation',
            responsibility_scope='Raw signal calculation',
            allowed_artifact_types=['SSOT', 'ENGINE', 'DATA_OUT'],
            cannot_own=['REPORT_OUT', 'DASHBOARD'],
            priority='core',
            authority_level=1
        )
        
        is_valid, errors = domain.validate()
        assert is_valid
        assert len(errors) == 0
    
    def test_valid_surface_domain_passes_validation(self):
        """Test that valid surface domain passes validation"""
        domain = DomainDefinition(
            domain_id='STATE',
            name='Portfolio State',
            responsibility_scope='Portfolio holdings management',
            allowed_artifact_types=['SSOT', 'DATA_IN', 'DATA_OUT'],
            cannot_own=['ENGINE', 'REPORT_OUT'],
            priority='surface',
            authority_level=None
        )
        
        is_valid, errors = domain.validate()
        assert is_valid
        assert len(errors) == 0
    
    def test_missing_domain_id_fails_validation(self):
        """Test that missing domain_id fails validation"""
        domain = DomainDefinition(
            domain_id='',
            name='Test Domain',
            responsibility_scope='Test',
            allowed_artifact_types=['SSOT'],
            cannot_own=[],
            priority='surface'
        )
        
        is_valid, errors = domain.validate()
        assert not is_valid
        assert any('domain_id' in error for error in errors)
    
    def test_invalid_priority_fails_validation(self):
        """Test that invalid priority fails validation"""
        domain = DomainDefinition(
            domain_id='TEST',
            name='Test Domain',
            responsibility_scope='Test',
            allowed_artifact_types=['SSOT'],
            cannot_own=[],
            priority='invalid'
        )
        
        is_valid, errors = domain.validate()
        assert not is_valid
        assert any('priority' in error for error in errors)
    
    def test_core_domain_without_authority_level_fails_validation(self):
        """Test that core domain without authority_level fails validation"""
        domain = DomainDefinition(
            domain_id='SIGNALS',
            name='Signal Generation',
            responsibility_scope='Raw signal calculation',
            allowed_artifact_types=['SSOT', 'ENGINE'],
            cannot_own=[],
            priority='core',
            authority_level=None
        )
        
        is_valid, errors = domain.validate()
        assert not is_valid
        assert any('authority_level' in error for error in errors)
    
    def test_surface_domain_with_authority_level_fails_validation(self):
        """Test that surface domain with authority_level fails validation"""
        domain = DomainDefinition(
            domain_id='STATE',
            name='Portfolio State',
            responsibility_scope='Portfolio holdings',
            allowed_artifact_types=['SSOT'],
            cannot_own=[],
            priority='surface',
            authority_level=1
        )
        
        is_valid, errors = domain.validate()
        assert not is_valid
        assert any('surface domains' in error for error in errors)
    
    def test_invalid_authority_level_fails_validation(self):
        """Test that invalid authority_level fails validation"""
        domain = DomainDefinition(
            domain_id='SIGNALS',
            name='Signal Generation',
            responsibility_scope='Raw signal calculation',
            allowed_artifact_types=['SSOT'],
            cannot_own=[],
            priority='core',
            authority_level=5  # Invalid: must be 1-4
        )
        
        is_valid, errors = domain.validate()
        assert not is_valid
        assert any('between 1 and 4' in error for error in errors)
    
    def test_conflicting_allowed_and_cannot_own_fails_validation(self):
        """Test that conflicts between allowed and cannot_own fail validation"""
        domain = DomainDefinition(
            domain_id='TEST',
            name='Test Domain',
            responsibility_scope='Test',
            allowed_artifact_types=['SSOT', 'ENGINE'],
            cannot_own=['ENGINE'],  # Conflict!
            priority='surface'
        )
        
        is_valid, errors = domain.validate()
        assert not is_valid
        assert any('both allowed and forbidden' in error for error in errors)


class TestDomainDefinitionMethods:
    """Test DomainDefinition methods"""
    
    def test_can_own_type_for_allowed_type(self):
        """Test that domain can own allowed artifact type"""
        domain = DomainDefinition(
            domain_id='SIGNALS',
            name='Signal Generation',
            responsibility_scope='Raw signal calculation',
            allowed_artifact_types=['SSOT', 'ENGINE', 'DATA_OUT'],
            cannot_own=['REPORT_OUT'],
            priority='core',
            authority_level=1
        )
        
        assert domain.can_own_type('SSOT')
        assert domain.can_own_type('ENGINE')
        assert domain.can_own_type('DATA_OUT')
    
    def test_cannot_own_type_for_forbidden_type(self):
        """Test that domain cannot own forbidden artifact type"""
        domain = DomainDefinition(
            domain_id='SIGNALS',
            name='Signal Generation',
            responsibility_scope='Raw signal calculation',
            allowed_artifact_types=['SSOT', 'ENGINE', 'DATA_OUT'],
            cannot_own=['REPORT_OUT', 'DASHBOARD'],
            priority='core',
            authority_level=1
        )
        
        assert not domain.can_own_type('REPORT_OUT')
        assert not domain.can_own_type('DASHBOARD')
    
    def test_cannot_own_type_for_not_allowed_type(self):
        """Test that domain cannot own type not in allowed list"""
        domain = DomainDefinition(
            domain_id='SIGNALS',
            name='Signal Generation',
            responsibility_scope='Raw signal calculation',
            allowed_artifact_types=['SSOT', 'ENGINE'],
            cannot_own=[],
            priority='core',
            authority_level=1
        )
        
        assert not domain.can_own_type('DASHBOARD')
        assert not domain.can_own_type('RUNTIME')
    
    def test_is_core_domain_for_core_domain(self):
        """Test that core domain is identified correctly"""
        domain = DomainDefinition(
            domain_id='SIGNALS',
            name='Signal Generation',
            responsibility_scope='Raw signal calculation',
            allowed_artifact_types=['SSOT'],
            cannot_own=[],
            priority='core',
            authority_level=1
        )
        
        assert domain.is_core_domain()
    
    def test_is_core_domain_for_surface_domain(self):
        """Test that surface domain is identified correctly"""
        domain = DomainDefinition(
            domain_id='STATE',
            name='Portfolio State',
            responsibility_scope='Portfolio holdings',
            allowed_artifact_types=['SSOT'],
            cannot_own=[],
            priority='surface'
        )
        
        assert not domain.is_core_domain()
    
    def test_get_authority_level_for_core_domain(self):
        """Test that authority level is returned for core domain"""
        domain = DomainDefinition(
            domain_id='SIGNALS',
            name='Signal Generation',
            responsibility_scope='Raw signal calculation',
            allowed_artifact_types=['SSOT'],
            cannot_own=[],
            priority='core',
            authority_level=1
        )
        
        assert domain.get_authority_level() == 1
    
    def test_get_authority_level_for_surface_domain(self):
        """Test that surface domain returns 999 for authority level"""
        domain = DomainDefinition(
            domain_id='STATE',
            name='Portfolio State',
            responsibility_scope='Portfolio holdings',
            allowed_artifact_types=['SSOT'],
            cannot_own=[],
            priority='surface'
        )
        
        assert domain.get_authority_level() == 999
    
    def test_authority_level_ordering(self):
        """Test that authority levels are ordered correctly"""
        signals = DomainDefinition(
            domain_id='SIGNALS',
            name='Signal Generation',
            responsibility_scope='Raw signal calculation',
            allowed_artifact_types=['SSOT'],
            cannot_own=[],
            priority='core',
            authority_level=1
        )
        
        semantics = DomainDefinition(
            domain_id='SEMANTICS',
            name='Semantic Interpretation',
            responsibility_scope='Semantic state creation',
            allowed_artifact_types=['SSOT'],
            cannot_own=[],
            priority='core',
            authority_level=2
        )
        
        reasoning = DomainDefinition(
            domain_id='REASONING',
            name='Reasoning Logic',
            responsibility_scope='Decision logic',
            allowed_artifact_types=['SSOT'],
            cannot_own=[],
            priority='core',
            authority_level=3
        )
        
        report = DomainDefinition(
            domain_id='REPORT',
            name='Report Generation',
            responsibility_scope='Human-readable reports',
            allowed_artifact_types=['SSOT'],
            cannot_own=[],
            priority='core',
            authority_level=4
        )
        
        # Lower authority_level = higher authority
        assert signals.get_authority_level() < semantics.get_authority_level()
        assert semantics.get_authority_level() < reasoning.get_authority_level()
        assert reasoning.get_authority_level() < report.get_authority_level()


class TestValidateDomainDict:
    """Test validate_domain_dict function"""
    
    def test_valid_domain_dict_passes_validation(self):
        """Test that valid domain dict passes validation"""
        domain_dict = {
            'domain_id': 'SIGNALS',
            'name': 'Signal Generation',
            'responsibility_scope': 'Raw signal calculation',
            'allowed_artifact_types': ['SSOT', 'ENGINE'],
            'cannot_own': ['REPORT_OUT'],
            'priority': 'core',
            'authority_level': 1
        }
        
        is_valid, errors = validate_domain_dict(domain_dict)
        assert is_valid
        assert len(errors) == 0
    
    def test_missing_required_field_fails_validation(self):
        """Test that missing required field fails validation"""
        domain_dict = {
            'domain_id': 'SIGNALS',
            'name': 'Signal Generation',
            # Missing responsibility_scope
            'allowed_artifact_types': ['SSOT'],
            'cannot_own': [],
            'priority': 'core',
            'authority_level': 1
        }
        
        is_valid, errors = validate_domain_dict(domain_dict)
        assert not is_valid
        assert any('responsibility_scope' in error for error in errors)
    
    def test_invalid_domain_dict_fails_validation(self):
        """Test that invalid domain dict fails validation"""
        domain_dict = {
            'domain_id': 'SIGNALS',
            'name': 'Signal Generation',
            'responsibility_scope': 'Raw signal calculation',
            'allowed_artifact_types': ['SSOT'],
            'cannot_own': [],
            'priority': 'invalid_priority',  # Invalid
            'authority_level': 1
        }
        
        is_valid, errors = validate_domain_dict(domain_dict)
        assert not is_valid
        assert any('priority' in error for error in errors)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
