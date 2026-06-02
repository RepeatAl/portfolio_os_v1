"""
Unit tests for Observer 4: Boundary Awareness Validator
"""

import pytest
import tempfile
import shutil
import yaml
from pathlib import Path
from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from artifact_schema import ArtifactMetadata
from observer_boundary_awareness import BoundaryAwarenessValidator
from validation_result import WarningCodes


class TestBoundaryAwarenessValidator:
    """Test suite for BoundaryAwarenessValidator"""
    
    @pytest.fixture
    def temp_repo(self):
        """Create temporary repository structure"""
        temp_dir = tempfile.mkdtemp()
        repo_root = Path(temp_dir)
        
        # Create .domainization directory
        domainization_dir = repo_root / '.domainization'
        domainization_dir.mkdir()
        
        # Create empty artifact registry
        artifact_registry_file = domainization_dir / 'artifact_registry.yaml'
        artifact_registry_file.write_text('artifacts: []\n')
        
        # Create domain registry with core reasoning domains
        domain_registry_file = domainization_dir / 'domain_registry.yaml'
        domains_data = {
            'domains': [
                {
                    'domain_id': 'SIGNALS',
                    'name': 'Signal Generation',
                    'responsibility_scope': 'Generate structured signals',
                    'allowed_artifact_types': ['ENGINE', 'SSOT', 'DATA_OUT'],
                    'cannot_own': ['REPORT_OUT', 'SEMANTIC_STATE'],
                    'priority': 'core',
                    'authority_level': 1
                },
                {
                    'domain_id': 'SEMANTICS',
                    'name': 'Semantic Interpretation',
                    'responsibility_scope': 'Interpret signals semantically',
                    'allowed_artifact_types': ['ENGINE', 'SSOT', 'SEMANTIC_STATE'],
                    'cannot_own': ['SIGNAL', 'REPORT_OUT'],
                    'priority': 'core',
                    'authority_level': 2
                },
                {
                    'domain_id': 'REASONING',
                    'name': 'Reasoning Logic',
                    'responsibility_scope': 'Apply reasoning',
                    'allowed_artifact_types': ['ENGINE', 'SSOT', 'REASONING_OBJECT'],
                    'cannot_own': ['SIGNAL', 'SEMANTIC_STATE', 'REPORT_OUT'],
                    'priority': 'core',
                    'authority_level': 3
                },
                {
                    'domain_id': 'REPORT',
                    'name': 'Report Generation',
                    'responsibility_scope': 'Generate reports',
                    'allowed_artifact_types': ['ENGINE', 'REPORT_OUT', 'SSOT'],
                    'cannot_own': ['SIGNAL', 'SEMANTIC_STATE', 'REASONING_OBJECT'],
                    'priority': 'core',
                    'authority_level': 4
                },
                {
                    'domain_id': 'ARCH',
                    'name': 'Architecture',
                    'responsibility_scope': 'System architecture',
                    'allowed_artifact_types': ['SSOT', 'ENGINE', 'CONFIG'],
                    'cannot_own': [],
                    'priority': 'surface',
                    'authority_level': None
                }
            ]
        }
        with open(domain_registry_file, 'w') as f:
            yaml.dump(domains_data, f)
        
        yield repo_root
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def artifact_registry(self, temp_repo):
        """Create artifact registry"""
        registry_path = temp_repo / '.domainization' / 'artifact_registry.yaml'
        registry = ArtifactRegistry(registry_path)
        registry.load()
        return registry
    
    @pytest.fixture
    def domain_registry(self, temp_repo):
        """Create domain registry"""
        registry_path = temp_repo / '.domainization' / 'domain_registry.yaml'
        registry = DomainRegistry(registry_path)
        registry.load()
        return registry
    
    @pytest.fixture
    def validator(self, artifact_registry, domain_registry):
        """Create boundary awareness validator"""
        return BoundaryAwarenessValidator(artifact_registry, domain_registry)
    
    def test_detect_signals_writes_semantic(self, validator, artifact_registry):
        """Test detection of SIGNALS domain writing semantic artifacts"""
        # Register artifact where SIGNALS writes SEMANTIC_STATE
        metadata = ArtifactMetadata(
            artifact_id='semantic_state_py',
            file_path='semantic_state.py',
            primary_domain='SIGNALS',  # Wrong domain
            artifact_type='SEMANTIC_STATE',
            lifecycle_status='active',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='none',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata)
        
        # Validate
        result = validator.validate()
        
        # Should have warning
        assert result.has_warnings()
        assert len(result.warnings) == 1
        assert result.warnings[0].warning_code == WarningCodes.W301_SIGNALS_WRITES_NON_SIGNAL
    
    def test_detect_signals_writes_report(self, validator, artifact_registry):
        """Test detection of SIGNALS domain writing report artifacts"""
        # Register artifact where SIGNALS writes REPORT_OUT
        metadata = ArtifactMetadata(
            artifact_id='report_txt',
            file_path='report.txt',
            primary_domain='SIGNALS',  # Wrong domain
            artifact_type='REPORT_OUT',
            lifecycle_status='current',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='none',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata)
        
        # Validate
        result = validator.validate()
        
        # Should have warning
        assert result.has_warnings()
        assert result.warnings[0].warning_code == WarningCodes.W301_SIGNALS_WRITES_NON_SIGNAL
    
    def test_detect_semantics_writes_signal(self, validator, artifact_registry):
        """Test detection of SEMANTICS domain writing signal artifacts"""
        # Register artifact where SEMANTICS writes SIGNAL
        metadata = ArtifactMetadata(
            artifact_id='signal_py',
            file_path='signal.py',
            primary_domain='SEMANTICS',  # Wrong domain
            artifact_type='SIGNAL',
            lifecycle_status='active',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='none',
            allowed_writers=['SEMANTICS'],
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata)
        
        # Validate
        result = validator.validate()
        
        # Should have warning
        assert result.has_warnings()
        assert result.warnings[0].warning_code == WarningCodes.W302_SEMANTICS_WRITES_NON_SEMANTIC
    
    def test_detect_reasoning_writes_semantic(self, validator, artifact_registry):
        """Test detection of REASONING domain writing semantic artifacts"""
        # Register artifact where REASONING writes SEMANTIC_STATE
        metadata = ArtifactMetadata(
            artifact_id='semantic_py',
            file_path='semantic.py',
            primary_domain='REASONING',  # Wrong domain
            artifact_type='SEMANTIC_STATE',
            lifecycle_status='active',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='none',
            allowed_writers=['REASONING'],
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata)
        
        # Validate
        result = validator.validate()
        
        # Should have warning
        assert result.has_warnings()
        assert result.warnings[0].warning_code == WarningCodes.W303_REASONING_WRITES_NON_REASONING
    
    def test_detect_report_writes_business_logic(self, validator, artifact_registry):
        """Test detection of REPORT domain writing business logic"""
        # Register artifact where REPORT writes SIGNAL
        metadata = ArtifactMetadata(
            artifact_id='signal_py',
            file_path='signal.py',
            primary_domain='REPORT',  # Wrong domain
            artifact_type='SIGNAL',
            lifecycle_status='active',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='none',
            allowed_writers=['REPORT'],
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata)
        
        # Validate
        result = validator.validate()
        
        # Should have warning
        assert result.has_warnings()
        assert result.warnings[0].warning_code == WarningCodes.W304_REPORT_WRITES_BUSINESS_LOGIC
    
    def test_allow_report_engine_for_reports(self, validator, artifact_registry):
        """Test that REPORT domain can have report generation engines"""
        # Register report engine in REPORT domain
        metadata = ArtifactMetadata(
            artifact_id='report_engine_py',
            file_path='engines/report_engine.py',
            primary_domain='REPORT',  # Correct
            artifact_type='ENGINE',
            lifecycle_status='active',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='implementation',
            allowed_writers=['REPORT'],
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata)
        
        # Validate
        result = validator.validate()
        
        # Should have no warnings (report engines are allowed)
        assert not result.has_warnings()
    
    def test_warn_report_engine_for_business_logic(self, validator, artifact_registry):
        """Test warning for REPORT domain having business logic engines"""
        # Register non-report engine in REPORT domain
        metadata = ArtifactMetadata(
            artifact_id='calculation_engine_py',
            file_path='engines/calculation_engine.py',
            primary_domain='REPORT',  # Wrong - business logic
            artifact_type='ENGINE',
            lifecycle_status='active',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='implementation',
            allowed_writers=['REPORT'],
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata)
        
        # Validate
        result = validator.validate()
        
        # Should have warning
        assert result.has_warnings()
        assert result.warnings[0].warning_code == WarningCodes.W304_REPORT_WRITES_BUSINESS_LOGIC
    
    def test_valid_authority_chain(self, validator, artifact_registry):
        """Test valid authority chain assignments"""
        # Register artifacts in correct domains
        metadata1 = ArtifactMetadata(
            artifact_id='signal_engine_py',
            file_path='signal_engine.py',
            primary_domain='SIGNALS',  # Correct
            artifact_type='ENGINE',
            lifecycle_status='active',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='implementation',
            allowed_writers=['SIGNALS'],
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata1)
        
        metadata2 = ArtifactMetadata(
            artifact_id='semantic_engine_py',
            file_path='semantic_engine.py',
            primary_domain='SEMANTICS',  # Correct
            artifact_type='ENGINE',
            lifecycle_status='active',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='implementation',
            allowed_writers=['SEMANTICS'],
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata2)
        
        # Validate
        result = validator.validate()
        
        # Should have no warnings
        assert not result.has_warnings()
    
    def test_detect_cross_domain_write(self, validator, artifact_registry):
        """Test detection of cross-domain write attempt"""
        # Register artifact owned by SIGNALS
        metadata = ArtifactMetadata(
            artifact_id='signal_engine_py',
            file_path='signal_engine.py',
            primary_domain='SIGNALS',
            artifact_type='ENGINE',
            lifecycle_status='active',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Engineer',
            ssot_relationship='implementation',
            allowed_writers=['SIGNALS'],  # Only SIGNALS can write
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata)
        
        # Validate with REPORT trying to modify
        result = validator.validate(
            changed_files=[Path('signal_engine.py')],
            modifier_domain='REPORT'
        )
        
        # Should have warning
        assert result.has_warnings()
        assert result.warnings[0].warning_code == WarningCodes.W305_CROSS_DOMAIN_WRITE
    
    def test_allow_authorized_cross_domain_write(self, validator, artifact_registry):
        """Test that authorized cross-domain writes are allowed"""
        # Register artifact with multiple allowed writers
        metadata = ArtifactMetadata(
            artifact_id='shared_config_yaml',
            file_path='shared_config.yaml',
            primary_domain='ARCH',
            artifact_type='CONFIG',
            lifecycle_status='active',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Architect',
            ssot_relationship='none',
            allowed_writers=['ARCH', 'SIGNALS', 'REPORT'],  # Multiple writers
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata)
        
        # Validate with SIGNALS modifying (authorized)
        result = validator.validate(
            changed_files=[Path('shared_config.yaml')],
            modifier_domain='SIGNALS'
        )
        
        # Should have no warnings
        assert not result.has_warnings()
    
    def test_surface_domains_not_checked(self, validator, artifact_registry):
        """Test that surface domains are not checked for authority chain"""
        # Register artifact in surface domain (ARCH)
        metadata = ArtifactMetadata(
            artifact_id='arch_doc_md',
            file_path='arch_doc.md',
            primary_domain='ARCH',  # Surface domain
            artifact_type='SSOT',
            lifecycle_status='canonical',
            created_date='2026-01-01',
            last_modified='2026-01-01',
            owner_role='Architect',
            ssot_relationship='canonical',
            allowed_writers=['ARCH'],
            allowed_readers=['ALL']
        )
        artifact_registry.register_artifact(metadata)
        
        # Validate
        result = validator.validate()
        
        # Should have no warnings (surface domains don't participate in authority chain)
        assert not result.has_warnings()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
