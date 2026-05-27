"""
Unit tests for Cloud Provider Pattern Detector

Tests pattern detection for forbidden (AWS, Supabase, Azure) and
allowed (Google Cloud Platform) cloud provider references.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from cloud_provider_detector import CloudProviderDetector, ProviderMatch, ScanResult


class TestCloudProviderDetector:
    """Test suite for CloudProviderDetector"""
    
    @pytest.fixture
    def detector(self):
        """Create a CloudProviderDetector instance"""
        return CloudProviderDetector()
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for file scanning tests"""
        temp = tempfile.mkdtemp()
        yield Path(temp)
        shutil.rmtree(temp)
    
    # --- Pattern Definition Tests ---
    
    def test_get_forbidden_patterns_returns_all_providers(self, detector):
        """Test that forbidden patterns include AWS, Supabase, and Azure"""
        patterns = detector.get_forbidden_patterns()
        assert 'aws' in patterns
        assert 'supabase' in patterns
        assert 'azure' in patterns
    
    def test_get_forbidden_patterns_has_entries(self, detector):
        """Test that each forbidden provider has at least one pattern"""
        patterns = detector.get_forbidden_patterns()
        for provider, provider_patterns in patterns.items():
            assert len(provider_patterns) > 0, f"Provider {provider} has no patterns"
    
    def test_get_allowed_patterns_returns_google(self, detector):
        """Test that allowed patterns include Google"""
        patterns = detector.get_allowed_patterns()
        assert 'google' in patterns
    
    def test_get_allowed_patterns_has_entries(self, detector):
        """Test that allowed provider has at least one pattern"""
        patterns = detector.get_allowed_patterns()
        for provider, provider_patterns in patterns.items():
            assert len(provider_patterns) > 0, f"Provider {provider} has no patterns"
    
    # --- is_forbidden_provider Tests ---
    
    def test_detect_aws_service_reference(self, detector):
        """Test detection of AWS service references (Requirement 11.2)"""
        assert detector.is_forbidden_provider("import boto3")
        assert detector.is_forbidden_provider("aws.s3.get_object()")
        assert detector.is_forbidden_provider("bucket.amazonaws.com")
        assert detector.is_forbidden_provider("s3://my-bucket/path")
        assert detector.is_forbidden_provider("from aws-sdk import client")
    
    def test_detect_supabase_reference(self, detector):
        """Test detection of Supabase API references (Requirement 11.3)"""
        assert detector.is_forbidden_provider("supabase.auth.signIn()")
        assert detector.is_forbidden_provider("https://project.supabase.co")
        assert detector.is_forbidden_provider("SUPABASE_URL=https://example.supabase.co")
        assert detector.is_forbidden_provider("SUPABASE_KEY=abc123")
        assert detector.is_forbidden_provider("from @supabase/supabase-js")
    
    def test_detect_azure_reference(self, detector):
        """Test detection of Azure infrastructure references (Requirement 11.4)"""
        assert detector.is_forbidden_provider("azure.storage.blob")
        assert detector.is_forbidden_provider("myapp.azurewebsites.net")
        assert detector.is_forbidden_provider("account.blob.core.windows.net")
        assert detector.is_forbidden_provider("AZURE_SUBSCRIPTION_ID=abc")
        assert detector.is_forbidden_provider("from @azure/storage-blob")
    
    def test_allow_google_cloud_reference(self, detector):
        """Test that Google Cloud references are allowed (Requirement 11.5)"""
        assert not detector.is_forbidden_provider("from google.cloud import storage")
        assert not detector.is_forbidden_provider("googleapis.com/sheets/v4")
        assert not detector.is_forbidden_provider("gcp.project_id = 'my-project'")
        assert not detector.is_forbidden_provider("google-cloud-storage==2.0.0")
    
    def test_allow_google_sheets_reference(self, detector):
        """Test that Google Sheets API references are allowed (Requirement 11.6)"""
        assert not detector.is_forbidden_provider("google.sheets.v4")
        assert not detector.is_forbidden_provider("from googleapiclient.discovery import build")
        assert not detector.is_forbidden_provider("google-sheets-api")
    
    def test_non_provider_text_not_flagged(self, detector):
        """Test that non-provider text is not flagged"""
        assert not detector.is_forbidden_provider("hello world")
        assert not detector.is_forbidden_provider("def calculate_total():")
        assert not detector.is_forbidden_provider("import pandas as pd")
        assert not detector.is_forbidden_provider("x = 42")

    # --- is_allowed_provider Tests ---
    
    def test_is_allowed_google_cloud(self, detector):
        """Test that Google Cloud references are identified as allowed"""
        assert detector.is_allowed_provider("google.cloud.storage")
        assert detector.is_allowed_provider("googleapis.com")
        assert detector.is_allowed_provider("gcp.project")
        assert detector.is_allowed_provider("firestore")
        assert detector.is_allowed_provider("bigquery")
        assert detector.is_allowed_provider("gs://bucket/path")
    
    def test_is_not_allowed_aws(self, detector):
        """Test that AWS references are not identified as allowed"""
        assert not detector.is_allowed_provider("boto3")
        assert not detector.is_allowed_provider("s3://bucket")
        assert not detector.is_allowed_provider("amazonaws.com")
    
    # --- scan_content Tests ---
    
    def test_scan_content_detects_aws(self, detector):
        """Test scanning content for AWS references"""
        content = """
import boto3
client = boto3.client('s3')
bucket = 'my-bucket.s3.amazonaws.com'
"""
        result = detector.scan_content(content, file_path="test.py")
        
        assert result.has_forbidden_references
        assert 'aws' in result.forbidden_providers
        assert result.file_path == "test.py"
    
    def test_scan_content_detects_supabase(self, detector):
        """Test scanning content for Supabase references"""
        content = """
const supabase = createClient(
    'https://project.supabase.co',
    'anon-key'
)
"""
        result = detector.scan_content(content, file_path="app.ts")
        
        assert result.has_forbidden_references
        assert 'supabase' in result.forbidden_providers
    
    def test_scan_content_detects_azure(self, detector):
        """Test scanning content for Azure references"""
        content = """
from azure.storage.blob import BlobServiceClient
connection_string = "DefaultEndpointsProtocol=https;AccountName=myaccount.blob.core.windows.net"
"""
        result = detector.scan_content(content, file_path="storage.py")
        
        assert result.has_forbidden_references
        assert 'azure' in result.forbidden_providers
    
    def test_scan_content_allows_google(self, detector):
        """Test scanning content with only Google references"""
        content = """
from google.cloud import storage
from googleapiclient.discovery import build

client = storage.Client()
service = build('sheets', 'v4')
"""
        result = detector.scan_content(content, file_path="gcp_client.py")
        
        assert not result.has_forbidden_references
        assert len(result.allowed_matches) > 0
    
    def test_scan_content_mixed_providers(self, detector):
        """Test scanning content with both forbidden and allowed references"""
        content = """
from google.cloud import storage  # allowed
import boto3  # forbidden
client = boto3.client('s3')  # forbidden
gcs_client = storage.Client()  # allowed
"""
        result = detector.scan_content(content, file_path="mixed.py")
        
        assert result.has_forbidden_references
        assert 'aws' in result.forbidden_providers
        assert len(result.allowed_matches) > 0
    
    def test_scan_content_empty(self, detector):
        """Test scanning empty content"""
        result = detector.scan_content("", file_path="empty.py")
        
        assert not result.has_forbidden_references
        assert len(result.forbidden_matches) == 0
        assert len(result.allowed_matches) == 0
    
    def test_scan_content_line_numbers(self, detector):
        """Test that line numbers are correctly reported"""
        content = """line 1
line 2
import boto3
line 4
"""
        result = detector.scan_content(content, file_path="test.py")
        
        assert result.has_forbidden_references
        assert result.forbidden_matches[0].line_number == 3
    
    def test_scan_content_multiple_providers_same_file(self, detector):
        """Test detection of multiple forbidden providers in same content"""
        content = """
import boto3
SUPABASE_URL = "https://project.supabase.co"
from azure.storage.blob import BlobClient
"""
        result = detector.scan_content(content, file_path="multi.py")
        
        assert result.has_forbidden_references
        providers = result.forbidden_providers
        assert 'aws' in providers
        assert 'supabase' in providers
        assert 'azure' in providers
    
    # --- scan_file Tests ---
    
    def test_scan_file_python(self, detector, temp_dir):
        """Test scanning a Python file"""
        test_file = temp_dir / "test_app.py"
        test_file.write_text("import boto3\nclient = boto3.client('s3')\n")
        
        result = detector.scan_file(test_file)
        
        assert result.has_forbidden_references
        assert 'aws' in result.forbidden_providers
    
    def test_scan_file_yaml(self, detector, temp_dir):
        """Test scanning a YAML file"""
        test_file = temp_dir / "config.yaml"
        test_file.write_text("database_url: https://project.supabase.co/rest/v1\n")
        
        result = detector.scan_file(test_file)
        
        assert result.has_forbidden_references
        assert 'supabase' in result.forbidden_providers
    
    def test_scan_file_skips_unsupported_extension(self, detector, temp_dir):
        """Test that unsupported file extensions are skipped"""
        test_file = temp_dir / "image.png"
        test_file.write_text("boto3 fake content in binary file")
        
        result = detector.scan_file(test_file)
        
        assert not result.has_forbidden_references
    
    def test_scan_file_nonexistent(self, detector):
        """Test scanning a nonexistent file"""
        result = detector.scan_file(Path("/nonexistent/file.py"))
        
        assert not result.has_forbidden_references
    
    def test_scan_file_clean(self, detector, temp_dir):
        """Test scanning a clean file with no provider references"""
        test_file = temp_dir / "clean.py"
        test_file.write_text("def hello():\n    return 'world'\n")
        
        result = detector.scan_file(test_file)
        
        assert not result.has_forbidden_references
    
    # --- scan_directory Tests ---
    
    def test_scan_directory_finds_violations(self, detector, temp_dir):
        """Test scanning a directory for violations"""
        # Create files with violations
        (temp_dir / "app.py").write_text("import boto3\n")
        (temp_dir / "config.yaml").write_text("url: https://project.supabase.co\n")
        (temp_dir / "clean.py").write_text("x = 42\n")
        
        results = detector.scan_directory(temp_dir)
        
        # Should find violations in app.py and config.yaml
        forbidden_results = [r for r in results if r.has_forbidden_references]
        assert len(forbidden_results) == 2
    
    def test_scan_directory_skips_excluded(self, detector, temp_dir):
        """Test that excluded directories are skipped"""
        # Create a __pycache__ directory with violations
        cache_dir = temp_dir / "__pycache__"
        cache_dir.mkdir()
        (cache_dir / "module.py").write_text("import boto3\n")
        
        # Create a .git directory with violations
        git_dir = temp_dir / ".git"
        git_dir.mkdir()
        (git_dir / "config").write_text("aws.region = us-east-1\n")
        
        results = detector.scan_directory(temp_dir)
        
        # Should not find any violations (all in excluded dirs)
        forbidden_results = [r for r in results if r.has_forbidden_references]
        assert len(forbidden_results) == 0
    
    def test_scan_directory_recursive(self, detector, temp_dir):
        """Test recursive directory scanning"""
        # Create nested structure
        sub_dir = temp_dir / "src" / "services"
        sub_dir.mkdir(parents=True)
        (sub_dir / "storage.py").write_text("from azure.storage.blob import BlobClient\n")
        
        results = detector.scan_directory(temp_dir, recursive=True)
        
        forbidden_results = [r for r in results if r.has_forbidden_references]
        assert len(forbidden_results) == 1
        assert 'azure' in forbidden_results[0].forbidden_providers
    
    def test_scan_directory_non_recursive(self, detector, temp_dir):
        """Test non-recursive directory scanning"""
        # Create file in root
        (temp_dir / "root.py").write_text("import boto3\n")
        
        # Create file in subdirectory
        sub_dir = temp_dir / "sub"
        sub_dir.mkdir()
        (sub_dir / "nested.py").write_text("import boto3\n")
        
        results = detector.scan_directory(temp_dir, recursive=False)
        
        # Should only find root.py
        forbidden_results = [r for r in results if r.has_forbidden_references]
        assert len(forbidden_results) == 1


class TestProviderMatch:
    """Test suite for ProviderMatch dataclass"""
    
    def test_str_with_file_path(self):
        """Test string representation with file path"""
        match = ProviderMatch(
            provider="aws",
            pattern=r"\bboto3\b",
            line_number=5,
            line_content="import boto3",
            file_path="app.py"
        )
        result = str(match)
        assert "app.py" in result
        assert "5" in result
        assert "aws" in result
    
    def test_str_without_file_path(self):
        """Test string representation without file path"""
        match = ProviderMatch(
            provider="supabase",
            pattern=r"\bsupabase\.",
            line_number=10,
            line_content="supabase.auth.signIn()",
            file_path=None
        )
        result = str(match)
        assert "10" in result
        assert "supabase" in result


class TestScanResult:
    """Test suite for ScanResult dataclass"""
    
    def test_has_forbidden_references_true(self):
        """Test has_forbidden_references when matches exist"""
        result = ScanResult(
            file_path="test.py",
            forbidden_matches=[
                ProviderMatch("aws", r"\bboto3\b", 1, "import boto3", "test.py")
            ]
        )
        assert result.has_forbidden_references
    
    def test_has_forbidden_references_false(self):
        """Test has_forbidden_references when no matches"""
        result = ScanResult(file_path="test.py")
        assert not result.has_forbidden_references
    
    def test_forbidden_providers_set(self):
        """Test forbidden_providers returns correct set"""
        result = ScanResult(
            file_path="test.py",
            forbidden_matches=[
                ProviderMatch("aws", r"\bboto3\b", 1, "import boto3", "test.py"),
                ProviderMatch("aws", r"\bs3://", 2, "s3://bucket", "test.py"),
                ProviderMatch("azure", r"\bazure\.", 3, "azure.storage", "test.py"),
            ]
        )
        assert result.forbidden_providers == {'aws', 'azure'}
    
    def test_summary_no_violations(self):
        """Test summary with no violations"""
        result = ScanResult(file_path="clean.py")
        assert "No forbidden" in result.summary()
    
    def test_summary_with_violations(self):
        """Test summary with violations"""
        result = ScanResult(
            file_path="app.py",
            forbidden_matches=[
                ProviderMatch("aws", r"\bboto3\b", 1, "import boto3", "app.py")
            ]
        )
        summary = result.summary()
        assert "1" in summary
        assert "aws" in summary
        assert "app.py" in summary


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
