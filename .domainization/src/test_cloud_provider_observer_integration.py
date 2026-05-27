"""
Integration tests for cloud provider detection in Observer 4 (Boundary Awareness)

Verifies that CloudProviderDetector is properly integrated into the
BoundaryAwarenessValidator and generates appropriate warnings for
forbidden cloud provider references.

Requirements: 11.1, 11.2, 11.3, 11.4, 11.7
"""

import pytest
import tempfile
import shutil
import yaml
from pathlib import Path
from artifact_registry import ArtifactRegistry
from domain_registry import DomainRegistry
from observer_boundary_awareness import BoundaryAwarenessValidator
from validation_result import WarningCodes


class TestCloudProviderObserverIntegration:
    """Integration tests for cloud provider detection in Observer 4"""

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

        # Create domain registry
        domain_registry_file = domainization_dir / 'domain_registry.yaml'
        domains_data = {
            'domains': [
                {
                    'domain_id': 'DEPLOY',
                    'name': 'Deployment',
                    'responsibility_scope': 'Deployment infrastructure',
                    'allowed_artifact_types': ['CONFIG', 'RUNTIME'],
                    'cannot_own': [],
                    'priority': 'surface',
                    'authority_level': None
                },
            ]
        }
        with open(domain_registry_file, 'w') as f:
            yaml.dump(domains_data, f)

        yield repo_root

        # Cleanup
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def validator(self, temp_repo):
        """Create boundary awareness validator with registries"""
        artifact_registry_path = temp_repo / '.domainization' / 'artifact_registry.yaml'
        domain_registry_path = temp_repo / '.domainization' / 'domain_registry.yaml'

        artifact_registry = ArtifactRegistry(artifact_registry_path)
        artifact_registry.load()
        domain_registry = DomainRegistry(domain_registry_path)
        domain_registry.load()

        return BoundaryAwarenessValidator(artifact_registry, domain_registry)

    # --- Requirement 11.1: Commit gates scan for forbidden cloud provider references ---

    def test_cloud_provider_detection_triggered_during_scan(self, validator, temp_repo):
        """Test that cloud provider detection is triggered when scanning files"""
        # Create a file with AWS reference
        test_file = temp_repo / 'deploy_config.py'
        test_file.write_text('import boto3\nclient = boto3.client("s3")\n')

        # Scan the file
        warnings = validator.scan_files_for_cloud_providers([test_file])

        # Detection should be triggered and produce warnings
        assert len(warnings) > 0

    def test_scan_empty_file_produces_no_warnings(self, validator, temp_repo):
        """Test that scanning an empty file produces no warnings"""
        test_file = temp_repo / 'empty_module.py'
        test_file.write_text('')

        warnings = validator.scan_files_for_cloud_providers([test_file])

        assert len(warnings) == 0

    def test_scan_multiple_files(self, validator, temp_repo):
        """Test scanning multiple files at once"""
        file1 = temp_repo / 'service_a.py'
        file1.write_text('import boto3\n')

        file2 = temp_repo / 'service_b.py'
        file2.write_text('from azure.storage import blob\n')

        file3 = temp_repo / 'service_c.py'
        file3.write_text('from google.cloud import storage\n')

        warnings = validator.scan_files_for_cloud_providers([file1, file2, file3])

        # file1 and file2 should produce warnings, file3 should not
        assert len(warnings) >= 2
        warning_files = {w.file_path for w in warnings}
        assert str(file1) in warning_files
        assert str(file2) in warning_files
        assert str(file3) not in warning_files

    # --- Requirement 11.2: AWS service references detected (warning mode) ---

    def test_aws_reference_generates_warning(self, validator, temp_repo):
        """Test that AWS references generate warnings, not errors/blocks"""
        test_file = temp_repo / 'aws_usage.py'
        test_file.write_text('import boto3\nclient = boto3.client("dynamodb")\n')

        warnings = validator.scan_files_for_cloud_providers([test_file])

        assert len(warnings) > 0
        for warning in warnings:
            # Verify it's a warning (severity medium), not a blocking error
            assert warning.severity == "medium"
            assert warning.warning_code == WarningCodes.W501_AWS_REFERENCE_DETECTED

    def test_aws_sdk_reference_detected(self, validator, temp_repo):
        """Test detection of AWS SDK references"""
        test_file = temp_repo / 'package_config.json'
        test_file.write_text('{"dependencies": {"@aws-sdk/client-s3": "^3.0.0"}}\n')

        warnings = validator.scan_files_for_cloud_providers([test_file])

        assert len(warnings) > 0
        assert any(w.warning_code == WarningCodes.W501_AWS_REFERENCE_DETECTED for w in warnings)

    # --- Requirement 11.3: Supabase API calls detected (warning mode) ---

    def test_supabase_reference_generates_warning(self, validator, temp_repo):
        """Test that Supabase references generate warnings"""
        test_file = temp_repo / 'auth_service.py'
        test_file.write_text('SUPABASE_URL = "https://xyz.supabase.co"\n')

        warnings = validator.scan_files_for_cloud_providers([test_file])

        assert len(warnings) > 0
        assert any(w.warning_code == WarningCodes.W502_SUPABASE_REFERENCE_DETECTED for w in warnings)

    def test_supabase_js_import_detected(self, validator, temp_repo):
        """Test detection of Supabase JS imports"""
        test_file = temp_repo / 'client.ts'
        test_file.write_text('import { createClient } from "@supabase/supabase-js"\n')

        warnings = validator.scan_files_for_cloud_providers([test_file])

        assert len(warnings) > 0
        assert any(w.warning_code == WarningCodes.W502_SUPABASE_REFERENCE_DETECTED for w in warnings)

    # --- Requirement 11.4: Azure infrastructure references detected (warning mode) ---

    def test_azure_reference_generates_warning(self, validator, temp_repo):
        """Test that Azure references generate warnings"""
        test_file = temp_repo / 'storage_client.py'
        test_file.write_text('from azure.storage.blob import BlobServiceClient\n')

        warnings = validator.scan_files_for_cloud_providers([test_file])

        assert len(warnings) > 0
        assert any(w.warning_code == WarningCodes.W503_AZURE_REFERENCE_DETECTED for w in warnings)

    def test_azure_website_reference_detected(self, validator, temp_repo):
        """Test detection of Azure website references"""
        test_file = temp_repo / 'deploy.yaml'
        test_file.write_text('endpoint: https://myapp.azurewebsites.net\n')

        warnings = validator.scan_files_for_cloud_providers([test_file])

        assert len(warnings) > 0
        assert any(w.warning_code == WarningCodes.W503_AZURE_REFERENCE_DETECTED for w in warnings)

    # --- Google Cloud references do NOT trigger warnings ---

    def test_google_cloud_reference_no_warning(self, validator, temp_repo):
        """Test that Google Cloud references do not trigger warnings"""
        test_file = temp_repo / 'gcp_client.py'
        test_file.write_text(
            'from google.cloud import storage\n'
            'from google.cloud import bigquery\n'
            'bucket = storage.Client().bucket("gs://my-bucket")\n'
        )

        warnings = validator.scan_files_for_cloud_providers([test_file])

        assert len(warnings) == 0

    def test_google_sheets_reference_no_warning(self, validator, temp_repo):
        """Test that Google Sheets API references do not trigger warnings"""
        test_file = temp_repo / 'sheets_client.py'
        test_file.write_text(
            'from googleapiclient.discovery import build\n'
            'service = build("sheets", "v4")\n'
        )

        warnings = validator.scan_files_for_cloud_providers([test_file])

        assert len(warnings) == 0

    def test_firestore_reference_no_warning(self, validator, temp_repo):
        """Test that Firestore references do not trigger warnings"""
        test_file = temp_repo / 'db_client.py'
        test_file.write_text('from google.cloud import firestore\ndb = firestore.Client()\n')

        warnings = validator.scan_files_for_cloud_providers([test_file])

        assert len(warnings) == 0

    # --- Requirement 11.7: Error message specifies provider and location ---

    def test_warning_message_includes_provider_name(self, validator, temp_repo):
        """Test that warning message specifies which provider was detected"""
        test_file = temp_repo / 'infra.py'
        test_file.write_text('import boto3\n')

        warnings = validator.scan_files_for_cloud_providers([test_file])

        assert len(warnings) > 0
        # Warning message should include provider name
        assert 'AWS' in warnings[0].warning_message

    def test_warning_message_includes_file_path(self, validator, temp_repo):
        """Test that warning message includes the file path where provider was found"""
        test_file = temp_repo / 'infra.py'
        test_file.write_text('import boto3\n')

        warnings = validator.scan_files_for_cloud_providers([test_file])

        assert len(warnings) > 0
        # Warning should include file path
        assert str(test_file) in warnings[0].warning_message
        assert str(test_file) == warnings[0].file_path

    def test_warning_message_includes_line_number(self, validator, temp_repo):
        """Test that warning message includes the line number"""
        test_file = temp_repo / 'infra.py'
        test_file.write_text('# comment\n# another comment\nimport boto3\n')

        warnings = validator.scan_files_for_cloud_providers([test_file])

        assert len(warnings) > 0
        # Line number should be 3 (third line)
        assert 'line 3' in warnings[0].warning_message

    def test_warning_suggestion_includes_offending_line(self, validator, temp_repo):
        """Test that the suggestion includes the offending line content"""
        test_file = temp_repo / 'infra.py'
        test_file.write_text('client = boto3.client("s3")\n')

        warnings = validator.scan_files_for_cloud_providers([test_file])

        assert len(warnings) > 0
        # Suggestion should include the line content
        assert 'boto3.client("s3")' in warnings[0].suggestion

    def test_multiple_providers_in_same_file(self, validator, temp_repo):
        """Test detection of multiple different providers in the same file"""
        test_file = temp_repo / 'multi_cloud.py'
        test_file.write_text(
            'import boto3\n'
            'SUPABASE_URL = "https://xyz.supabase.co"\n'
            'from azure.storage import blob\n'
        )

        warnings = validator.scan_files_for_cloud_providers([test_file])

        # Should detect all three providers
        warning_codes = {w.warning_code for w in warnings}
        assert WarningCodes.W501_AWS_REFERENCE_DETECTED in warning_codes
        assert WarningCodes.W502_SUPABASE_REFERENCE_DETECTED in warning_codes
        assert WarningCodes.W503_AZURE_REFERENCE_DETECTED in warning_codes

    # --- Warnings only, never blocking ---

    def test_warnings_never_block(self, validator, temp_repo):
        """Test that cloud provider warnings never block (observability mode)"""
        test_file = temp_repo / 'heavy_aws.py'
        test_file.write_text(
            'import boto3\n'
            'from botocore.config import Config\n'
            's3 = boto3.client("s3")\n'
            'dynamodb = boto3.resource("dynamodb")\n'
        )

        warnings = validator.scan_files_for_cloud_providers([test_file])

        # All warnings should be severity "medium" (not "critical" or "high")
        # This ensures they are observability warnings, not blocking errors
        for warning in warnings:
            assert warning.severity == "medium"

    def test_nonscannable_file_extension_no_warning(self, validator, temp_repo):
        """Test that non-scannable file extensions produce no warnings"""
        test_file = temp_repo / 'image.png'
        test_file.write_bytes(b'import boto3')  # Binary content with AWS text

        warnings = validator.scan_files_for_cloud_providers([test_file])

        # .png is not a scannable extension, should produce no warnings
        assert len(warnings) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
