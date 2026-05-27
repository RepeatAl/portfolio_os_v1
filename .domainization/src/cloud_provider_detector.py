"""
Cloud Provider Pattern Detector

Scans files for forbidden cloud provider references (AWS, Supabase, Azure)
while allowing Google Cloud Platform references. All detection operates in
observability/warning mode only - no blocking.

Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Set


@dataclass
class ProviderMatch:
    """Represents a detected cloud provider reference"""
    
    provider: str  # "aws" | "supabase" | "azure"
    pattern: str  # The pattern that matched
    line_number: int  # Line number where match was found
    line_content: str  # Content of the matching line
    file_path: Optional[str] = None  # File path where match was found
    
    def __str__(self) -> str:
        location = f"{self.file_path}:" if self.file_path else ""
        return f"{location}{self.line_number}: [{self.provider}] matched '{self.pattern}' in: {self.line_content.strip()}"


@dataclass
class ScanResult:
    """Result from scanning a file or content for provider references"""
    
    file_path: Optional[str] = None
    forbidden_matches: List[ProviderMatch] = field(default_factory=list)
    allowed_matches: List[ProviderMatch] = field(default_factory=list)
    
    @property
    def has_forbidden_references(self) -> bool:
        """Check if any forbidden provider references were found"""
        return len(self.forbidden_matches) > 0
    
    @property
    def forbidden_providers(self) -> Set[str]:
        """Get set of forbidden providers detected"""
        return {m.provider for m in self.forbidden_matches}
    
    def summary(self) -> str:
        """Generate human-readable summary of scan results"""
        if not self.has_forbidden_references:
            return f"No forbidden cloud provider references found"
        
        providers = ', '.join(sorted(self.forbidden_providers))
        return (
            f"Found {len(self.forbidden_matches)} forbidden cloud provider "
            f"reference(s) [{providers}] in {self.file_path or 'content'}"
        )


class CloudProviderDetector:
    """
    Detects cloud provider references in source files.
    
    Identifies forbidden providers (AWS, Supabase, Azure) and allowed
    providers (Google Cloud Platform). Operates in observability mode
    only - generates warnings, never blocks.
    """
    
    # Forbidden patterns grouped by provider
    FORBIDDEN_PATTERNS = {
        'aws': [
            r'\baws\.',
            r'\baws-',
            r'\.amazonaws\.com',
            r'\bboto3\b',
            r'\bbotocore\b',
            r'\bs3://',
            r'\bdynamodb\b',
            r'\baws_access_key',
            r'\baws_secret_key',
            r'\baws_session_token',
            r'\bAWS_ACCESS_KEY',
            r'\bAWS_SECRET_KEY',
            r'\bAWS_SESSION_TOKEN',
            r'\bAWS_REGION\b',
            r'\baws_region\b',
            r'\baws-sdk\b',
            r'\b@aws-sdk\b',
            r'\baws-cdk\b',
            r'\baws-lambda\b',
            r'\baws_lambda\b',
            r'\bamazon-s3\b',
            r'\bcloudformation\b',
            r'\bsagemaker\b',
            r'\baws-amplify\b',
        ],
        'supabase': [
            r'\bsupabase\.',
            r'\bsupabase-',
            r'\bsupabase\.co\b',
            r'\bsupabase_url\b',
            r'\bSUPABASE_URL\b',
            r'\bsupabase_key\b',
            r'\bSUPABASE_KEY\b',
            r'\bsupabase_anon_key\b',
            r'\bSUPABASE_ANON_KEY\b',
            r'\b@supabase/',
            r'\bsupabase-js\b',
            r'\bcreateClient\b.*supabase',
            r'\bfrom\s+[\'"]@supabase',
        ],
        'azure': [
            r'\bazure\.',
            r'\bazure-',
            r'\.azure\.com',
            r'\.azurewebsites\.net',
            r'\.blob\.core\.windows\.net',
            r'\bazure_storage\b',
            r'\bAZURE_STORAGE\b',
            r'\bazure_subscription',
            r'\bAZURE_SUBSCRIPTION',
            r'@azure/',
            r'\bazure-sdk\b',
            r'\bazure-functions\b',
            r'\bazure_functions\b',
            r'\bcosmosdb\b',
            r'\bazure-devops\b',
        ],
    }
    
    # Allowed patterns (Google Cloud Platform)
    ALLOWED_PATTERNS = {
        'google': [
            r'\bgoogle\.',
            r'\bgoogle-',
            r'\bgoogleapis\.com',
            r'\bgcp\.',
            r'\bgcp-',
            r'\bgoogle-cloud\b',
            r'\b@google-cloud/',
            r'\bgoogle\.cloud\b',
            r'\bfirestore\b',
            r'\bbigquery\b',
            r'\bgoogle-auth\b',
            r'\bgoogle\.auth\b',
            r'\bgoogle\.sheets\b',
            r'\bgoogle-sheets\b',
            r'\bgoogleapiclient\b',
            r'\bgoogle_auth\b',
            r'\bcloud\.google\.com',
            r'\bgcloud\b',
            r'\bgsutil\b',
            r'\bgs://',
            r'\bpubsub\b',
            r'\bcloud-functions\b',
            r'\bcloud-run\b',
            r'\bcloud-storage\b',
            r'\bvertex-ai\b',
            r'\bvertexai\b',
        ],
    }

    # File extensions to scan (source code and config files)
    SCANNABLE_EXTENSIONS = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.mjs', '.cjs',
        '.yaml', '.yml', '.json', '.toml', '.ini', '.cfg',
        '.env', '.sh', '.bash', '.zsh',
        '.tf', '.hcl',  # Terraform/HCL
        '.dockerfile', '.docker-compose',
        '.md',  # Documentation may reference providers
    }
    
    # Files/directories to skip during scanning
    SKIP_PATTERNS = {
        '__pycache__', '.git', '.venv', 'node_modules',
        '.pytest_cache', '.mypy_cache', '.tox',
        'venv', 'env', '.env.example',
    }
    
    def __init__(self):
        """Initialize the cloud provider detector with compiled regex patterns"""
        self._forbidden_compiled = {}
        self._allowed_compiled = {}
        
        # Compile forbidden patterns
        for provider, patterns in self.FORBIDDEN_PATTERNS.items():
            self._forbidden_compiled[provider] = [
                re.compile(pattern, re.IGNORECASE) for pattern in patterns
            ]
        
        # Compile allowed patterns
        for provider, patterns in self.ALLOWED_PATTERNS.items():
            self._allowed_compiled[provider] = [
                re.compile(pattern, re.IGNORECASE) for pattern in patterns
            ]
    
    def get_forbidden_patterns(self) -> dict:
        """
        Return dictionary of forbidden patterns grouped by provider.
        
        Returns:
            Dict mapping provider name to list of pattern strings
        """
        return dict(self.FORBIDDEN_PATTERNS)
    
    def get_allowed_patterns(self) -> dict:
        """
        Return dictionary of allowed patterns grouped by provider.
        
        Returns:
            Dict mapping provider name to list of pattern strings
        """
        return dict(self.ALLOWED_PATTERNS)
    
    def is_forbidden_provider(self, reference: str) -> bool:
        """
        Check if a text reference matches any forbidden cloud provider pattern.
        
        Args:
            reference: Text string to check against forbidden patterns
            
        Returns:
            True if the reference matches a forbidden provider pattern
        """
        for provider, compiled_patterns in self._forbidden_compiled.items():
            for pattern in compiled_patterns:
                if pattern.search(reference):
                    # Check it's not also an allowed pattern (e.g., google.cloud)
                    if not self._is_allowed_reference(reference):
                        return True
        return False
    
    def is_allowed_provider(self, reference: str) -> bool:
        """
        Check if a text reference matches any allowed cloud provider pattern.
        
        Args:
            reference: Text string to check against allowed patterns
            
        Returns:
            True if the reference matches an allowed provider pattern
        """
        return self._is_allowed_reference(reference)
    
    def _is_allowed_reference(self, text: str) -> bool:
        """Check if text matches any allowed pattern"""
        for provider, compiled_patterns in self._allowed_compiled.items():
            for pattern in compiled_patterns:
                if pattern.search(text):
                    return True
        return False
    
    def scan_content(self, content: str, file_path: Optional[str] = None) -> ScanResult:
        """
        Scan content string for cloud provider references.
        
        Args:
            content: Text content to scan
            file_path: Optional file path for context in results
            
        Returns:
            ScanResult with forbidden and allowed matches
        """
        result = ScanResult(file_path=file_path)
        
        lines = content.splitlines()
        for line_number, line in enumerate(lines, start=1):
            # Skip empty lines and comment-only lines for efficiency
            stripped = line.strip()
            if not stripped:
                continue
            
            # Check for forbidden patterns
            for provider, compiled_patterns in self._forbidden_compiled.items():
                for i, pattern in enumerate(compiled_patterns):
                    if pattern.search(line):
                        # Verify it's not also an allowed reference
                        if not self._is_allowed_reference(line):
                            match = ProviderMatch(
                                provider=provider,
                                pattern=self.FORBIDDEN_PATTERNS[provider][i],
                                line_number=line_number,
                                line_content=line,
                                file_path=file_path,
                            )
                            result.forbidden_matches.append(match)
                            break  # One match per provider per line is enough
            
            # Check for allowed patterns
            for provider, compiled_patterns in self._allowed_compiled.items():
                for i, pattern in enumerate(compiled_patterns):
                    if pattern.search(line):
                        match = ProviderMatch(
                            provider=provider,
                            pattern=self.ALLOWED_PATTERNS[provider][i],
                            line_number=line_number,
                            line_content=line,
                            file_path=file_path,
                        )
                        result.allowed_matches.append(match)
                        break  # One match per provider per line is enough
        
        return result
    
    def scan_file(self, file_path: Path) -> ScanResult:
        """
        Scan a single file for cloud provider references.
        
        Args:
            file_path: Path to the file to scan
            
        Returns:
            ScanResult with forbidden and allowed matches
        """
        file_path = Path(file_path)
        
        # Check if file should be scanned
        if not self._should_scan_file(file_path):
            return ScanResult(file_path=str(file_path))
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
        except (OSError, IOError):
            return ScanResult(file_path=str(file_path))
        
        return self.scan_content(content, file_path=str(file_path))
    
    def scan_directory(self, directory: Path, recursive: bool = True) -> List[ScanResult]:
        """
        Scan all eligible files in a directory for provider references.
        
        Args:
            directory: Path to directory to scan
            recursive: Whether to scan subdirectories
            
        Returns:
            List of ScanResult objects (one per file with matches)
        """
        directory = Path(directory)
        results = []
        
        if not directory.is_dir():
            return results
        
        iterator = directory.rglob('*') if recursive else directory.glob('*')
        
        for file_path in iterator:
            if not file_path.is_file():
                continue
            
            # Skip files in excluded directories
            if self._should_skip_path(file_path):
                continue
            
            result = self.scan_file(file_path)
            if result.has_forbidden_references or result.allowed_matches:
                results.append(result)
        
        return results
    
    def _should_scan_file(self, file_path: Path) -> bool:
        """Check if a file should be scanned based on extension"""
        # Handle files without extension (e.g., Dockerfile)
        if file_path.suffix == '':
            name_lower = file_path.name.lower()
            return name_lower in {'dockerfile', 'makefile', 'procfile'}
        
        return file_path.suffix.lower() in self.SCANNABLE_EXTENSIONS
    
    def _should_skip_path(self, file_path: Path) -> bool:
        """Check if a path should be skipped"""
        parts = file_path.parts
        for part in parts:
            if part in self.SKIP_PATTERNS:
                return True
        return False
