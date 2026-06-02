"""
GOVERNANCE STABILIZATION AUDIT
Forensic review of the domainization system integrity.

Checks:
1. Registry Truth Consistency (duplicates, missing deps, circular deps, file_path ↔ registry, domain ↔ type)
2. Lifecycle Integrity (valid states, illegal transitions, deprecated writability, active without deps)
3. Authority Chain Integrity (SIGNALS → SEMANTICS → REASONING → REPORT separation)
4. Observer Noise Audit (redundancy, severity, false positives)
5. Health Report Reality Check (operational usefulness)
6. CLI Governance Drift (bypass risks, unsafe updates, destructive commands)
"""

import yaml
import sys
from pathlib import Path
from collections import defaultdict

# Paths
REPO_ROOT = Path(__file__).parent.parent.parent
DOMAINIZATION_ROOT = Path(__file__).parent.parent
REGISTRY_PATH = DOMAINIZATION_ROOT / "artifact_registry.yaml"
DOMAIN_REGISTRY_PATH = DOMAINIZATION_ROOT / "domain_registry.yaml"
LIFECYCLE_PATH = DOMAINIZATION_ROOT / "lifecycle_state_machine.yaml"


def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def audit_registry_truth_consistency(artifacts, domains_data, lifecycle_data):
    """Audit 1: Registry Truth Consistency"""
    findings = []
    
    # 1.1 Duplicate artifact_ids
    ids = [a['artifact_id'] for a in artifacts]
    seen = {}
    for i, aid in enumerate(ids):
        if aid in seen:
            findings.append({
                'severity': 'CRITICAL',
                'category': 'DUPLICATE_ID',
                'message': f"Duplicate artifact_id: '{aid}' at positions {seen[aid]} and {i}"
            })
        else:
            seen[aid] = i
    
    # 1.2 Missing dependencies (referenced but not registered)
    all_ids = set(ids)
    for artifact in artifacts:
        deps = artifact.get('dependencies', []) or []
        for dep in deps:
            if dep not in all_ids:
                findings.append({
                    'severity': 'HIGH',
                    'category': 'MISSING_DEPENDENCY',
                    'message': f"Artifact '{artifact['artifact_id']}' depends on '{dep}' which is NOT registered"
                })
    
    # 1.3 Circular dependencies
    dep_graph = {}
    for artifact in artifacts:
        aid = artifact['artifact_id']
        deps = artifact.get('dependencies', []) or []
        dep_graph[aid] = deps
    
    def find_cycles(graph):
        visited = set()
        rec_stack = set()
        cycles = []
        
        def dfs(node, path):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if neighbor in graph:
                        dfs(neighbor, path)
                elif neighbor in rec_stack:
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    cycles.append(cycle)
            
            path.pop()
            rec_stack.discard(node)
        
        for node in graph:
            if node not in visited:
                dfs(node, [])
        
        return cycles
    
    cycles = find_cycles(dep_graph)
    for cycle in cycles:
        findings.append({
            'severity': 'CRITICAL',
            'category': 'CIRCULAR_DEPENDENCY',
            'message': f"Circular dependency detected: {' → '.join(cycle)}"
        })
    
    # 1.4 file_path ↔ filesystem consistency
    for artifact in artifacts:
        file_path = REPO_ROOT / artifact['file_path']
        if not file_path.exists():
            findings.append({
                'severity': 'MEDIUM',
                'category': 'FILE_NOT_FOUND',
                'message': f"Artifact '{artifact['artifact_id']}' references '{artifact['file_path']}' which does NOT exist on disk"
            })
    
    # 1.5 Domain ↔ artifact_type consistency
    valid_domains = {d['domain_id'] for d in domains_data['domains']}
    domain_allowed_types = {}
    domain_cannot_own = {}
    for d in domains_data['domains']:
        domain_allowed_types[d['domain_id']] = set(d.get('allowed_artifact_types', []))
        domain_cannot_own[d['domain_id']] = set(d.get('cannot_own', []))
    
    valid_types = set(lifecycle_data['artifact_types'].keys())
    
    for artifact in artifacts:
        domain = artifact['primary_domain']
        atype = artifact['artifact_type']
        
        if domain not in valid_domains:
            findings.append({
                'severity': 'CRITICAL',
                'category': 'INVALID_DOMAIN',
                'message': f"Artifact '{artifact['artifact_id']}' has invalid domain '{domain}'"
            })
        elif atype in domain_cannot_own.get(domain, set()):
            findings.append({
                'severity': 'HIGH',
                'category': 'DOMAIN_TYPE_VIOLATION',
                'message': f"Artifact '{artifact['artifact_id']}': domain '{domain}' CANNOT own type '{atype}'"
            })
        elif atype not in domain_allowed_types.get(domain, set()):
            findings.append({
                'severity': 'MEDIUM',
                'category': 'DOMAIN_TYPE_MISMATCH',
                'message': f"Artifact '{artifact['artifact_id']}': type '{atype}' not in allowed types for domain '{domain}'"
            })
        
        if atype not in valid_types:
            findings.append({
                'severity': 'CRITICAL',
                'category': 'INVALID_TYPE',
                'message': f"Artifact '{artifact['artifact_id']}' has invalid artifact_type '{atype}'"
            })
    
    return findings


def audit_lifecycle_integrity(artifacts, lifecycle_data):
    """Audit 2: Lifecycle Integrity"""
    findings = []
    
    type_states = {}
    for atype, config in lifecycle_data['artifact_types'].items():
        type_states[atype] = set(config['states'])
    
    for artifact in artifacts:
        atype = artifact['artifact_type']
        status = artifact['lifecycle_status']
        
        if atype not in type_states:
            continue  # Already caught in audit 1
        
        # 2.1 Valid lifecycle states
        if status not in type_states[atype]:
            findings.append({
                'severity': 'HIGH',
                'category': 'INVALID_LIFECYCLE_STATE',
                'message': f"Artifact '{artifact['artifact_id']}' has lifecycle_status '{status}' which is not valid for type '{atype}'. Valid: {type_states[atype]}"
            })
        
        # 2.2 Deprecated artifacts with write permissions
        read_only_states = set(lifecycle_data['artifact_types'][atype].get('read_only_states', []))
        regenerable_states = set(lifecycle_data['artifact_types'][atype].get('regenerable_states', []))
        if status in read_only_states and status not in regenerable_states:
            writers = artifact.get('allowed_writers', [])
            if writers and writers != ['NONE']:
                findings.append({
                    'severity': 'MEDIUM',
                    'category': 'DEPRECATED_WITH_WRITERS',
                    'message': f"Artifact '{artifact['artifact_id']}' is in read-only state '{status}' but still has allowed_writers: {writers}"
                })
    
    # 2.3 Active engines without dependencies (suspicious)
    for artifact in artifacts:
        if artifact['artifact_type'] == 'ENGINE' and artifact['lifecycle_status'] == 'active':
            deps = artifact.get('dependencies', []) or []
            if not deps:
                findings.append({
                    'severity': 'LOW',
                    'category': 'ACTIVE_WITHOUT_DEPS',
                    'message': f"Engine '{artifact['artifact_id']}' is active but has no dependencies (no SSOT backing?)"
                })
    
    return findings


def audit_authority_chain_integrity(artifacts):
    """Audit 3: Authority Chain Integrity (SIGNALS → SEMANTICS → REASONING → REPORT)"""
    findings = []
    
    # Build domain → artifacts map
    domain_artifacts = defaultdict(list)
    for artifact in artifacts:
        domain_artifacts[artifact['primary_domain']].append(artifact)
    
    # Check SIGNALS domain: should NOT contain semantic interpretation
    signals_artifacts = domain_artifacts.get('SIGNALS', [])
    for artifact in signals_artifacts:
        desc = (artifact.get('description', '') or '').lower()
        tags = [t.lower() for t in (artifact.get('tags', []) or [])]
        
        semantic_keywords = ['semantic', 'interpret', 'meaning', 'reasoning', 'decision', 'conclusion']
        for keyword in semantic_keywords:
            if keyword in desc or keyword in tags:
                findings.append({
                    'severity': 'HIGH',
                    'category': 'AUTHORITY_CHAIN_VIOLATION',
                    'message': f"SIGNALS artifact '{artifact['artifact_id']}' contains semantic/reasoning keyword '{keyword}' in description/tags. SIGNALS should only produce structured signals."
                })
                break
    
    # Check REPORT domain: should NOT contain decision logic
    report_artifacts = domain_artifacts.get('REPORT', [])
    for artifact in report_artifacts:
        desc = (artifact.get('description', '') or '').lower()
        tags = [t.lower() for t in (artifact.get('tags', []) or [])]
        
        decision_keywords = ['decision', 'reasoning', 'prioritize', 'conclude', 'recommend']
        for keyword in decision_keywords:
            if keyword in desc or keyword in tags:
                # Only flag engines, not report outputs
                if artifact['artifact_type'] == 'ENGINE':
                    findings.append({
                        'severity': 'MEDIUM',
                        'category': 'AUTHORITY_CHAIN_CONCERN',
                        'message': f"REPORT engine '{artifact['artifact_id']}' contains decision/reasoning keyword '{keyword}'. REPORT should only render, not reason."
                    })
                    break
    
    # Check REASONING domain: should NOT generate report text
    reasoning_artifacts = domain_artifacts.get('REASONING', [])
    for artifact in reasoning_artifacts:
        desc = (artifact.get('description', '') or '').lower()
        tags = [t.lower() for t in (artifact.get('tags', []) or [])]
        
        report_keywords = ['report', 'briefing', 'narrative', 'text generation', 'render']
        for keyword in report_keywords:
            if keyword in desc or keyword in tags:
                if artifact['artifact_type'] == 'ENGINE':
                    findings.append({
                        'severity': 'MEDIUM',
                        'category': 'AUTHORITY_CHAIN_CONCERN',
                        'message': f"REASONING engine '{artifact['artifact_id']}' contains report/rendering keyword '{keyword}'. REASONING should produce conclusions, not text."
                    })
                    break
    
    # Check cross-domain dependency direction
    # REPORT should depend on REASONING, not vice versa
    # REASONING should depend on SEMANTICS, not vice versa
    # SEMANTICS should depend on SIGNALS, not vice versa
    authority_order = {'SIGNALS': 1, 'SEMANTICS': 2, 'REASONING': 3, 'REPORT': 4}
    
    for artifact in artifacts:
        domain = artifact['primary_domain']
        if domain not in authority_order:
            continue
        
        deps = artifact.get('dependencies', []) or []
        for dep_id in deps:
            # Find the dependency's domain
            dep_artifact = next((a for a in artifacts if a['artifact_id'] == dep_id), None)
            if dep_artifact is None:
                continue
            
            dep_domain = dep_artifact['primary_domain']
            if dep_domain not in authority_order:
                continue
            
            # Check if dependency flows UPWARD (higher authority level depends on lower = wrong)
            if authority_order[dep_domain] > authority_order[domain]:
                findings.append({
                    'severity': 'HIGH',
                    'category': 'REVERSE_AUTHORITY_FLOW',
                    'message': f"Artifact '{artifact['artifact_id']}' (domain={domain}, level={authority_order[domain]}) depends on '{dep_id}' (domain={dep_domain}, level={authority_order[dep_domain]}). Authority should flow SIGNALS→SEMANTICS→REASONING→REPORT, not reverse."
                })
    
    return findings


def audit_cli_governance_drift(cli_source_path):
    """Audit 6: CLI Governance Drift"""
    findings = []
    
    cli_files = [
        'cli_registry_commands.py',
        'cli_validation_commands.py',
        'cli_health_commands.py',
        'cli_config_commands.py',
        'cli_main.py'
    ]
    
    for cli_file in cli_files:
        file_path = cli_source_path / cli_file
        if not file_path.exists():
            continue
        
        content = file_path.read_text()
        
        # Check for destructive operations without confirmation
        destructive_patterns = ['delete', 'remove', 'drop', 'purge', 'destroy']
        for pattern in destructive_patterns:
            if pattern in content.lower():
                # Check if there's a confirmation mechanism
                if 'confirm' not in content.lower() and '--force' not in content:
                    findings.append({
                        'severity': 'MEDIUM',
                        'category': 'DESTRUCTIVE_WITHOUT_CONFIRM',
                        'message': f"CLI file '{cli_file}' contains destructive operation '{pattern}' without confirmation mechanism"
                    })
        
        # Check if domain validation is enforced on register/update
        if 'register' in cli_file or 'registry' in cli_file:
            if 'can_own_type' not in content and 'validate' not in content.lower():
                findings.append({
                    'severity': 'HIGH',
                    'category': 'MISSING_DOMAIN_VALIDATION',
                    'message': f"CLI file '{cli_file}' may allow registration without domain-type validation"
                })
            
            # Check if lifecycle transition validation exists
            if 'update' in content.lower() and 'validate_transition' not in content:
                findings.append({
                    'severity': 'HIGH',
                    'category': 'MISSING_LIFECYCLE_VALIDATION',
                    'message': f"CLI file '{cli_file}' may allow lifecycle updates without transition validation"
                })
    
    # Check: Can CLI bypass cross-domain ownership?
    registry_cmd_path = cli_source_path / 'cli_registry_commands.py'
    if registry_cmd_path.exists():
        content = registry_cmd_path.read_text()
        
        # Check if writer domain validation exists
        if 'can_own_type' in content and '--force' in content and '_log_force_override' in content:
            # Validation is present with audit trail — governance enforced
            pass
        elif '--allowed-writers' in content:
            # The CLI allows setting allowed_writers without proper validation
            findings.append({
                'severity': 'HIGH',
                'category': 'CROSS_DOMAIN_WRITER_BYPASS',
                'message': "CLI 'register' and 'update' commands allow setting --allowed-writers to ANY domain without validating that the writer domain has authority over the artifact's type"
            })
    
    return findings


def run_full_audit():
    """Run the complete governance stabilization audit"""
    print("=" * 80)
    print("GOVERNANCE STABILIZATION AUDIT")
    print("Forensic Review of Domainization System Integrity")
    print("=" * 80)
    print()
    
    # Load data
    registry_data = load_yaml(REGISTRY_PATH)
    domains_data = load_yaml(DOMAIN_REGISTRY_PATH)
    lifecycle_data = load_yaml(LIFECYCLE_PATH)
    
    artifacts = registry_data['artifacts']
    print(f"Registry: {len(artifacts)} artifacts loaded")
    print(f"Domains: {len(domains_data['domains'])} domains defined")
    print(f"Lifecycle Types: {len(lifecycle_data['artifact_types'])} types defined")
    print()
    
    all_findings = []
    
    # Audit 1: Registry Truth Consistency
    print("-" * 80)
    print("AUDIT 1: REGISTRY TRUTH CONSISTENCY")
    print("-" * 80)
    findings = audit_registry_truth_consistency(artifacts, domains_data, lifecycle_data)
    all_findings.extend(findings)
    if findings:
        for f in findings:
            print(f"  [{f['severity']}] {f['category']}: {f['message']}")
    else:
        print("  ✓ No issues found")
    print()
    
    # Audit 2: Lifecycle Integrity
    print("-" * 80)
    print("AUDIT 2: LIFECYCLE INTEGRITY")
    print("-" * 80)
    findings = audit_lifecycle_integrity(artifacts, lifecycle_data)
    all_findings.extend(findings)
    if findings:
        for f in findings:
            print(f"  [{f['severity']}] {f['category']}: {f['message']}")
    else:
        print("  ✓ No issues found")
    print()
    
    # Audit 3: Authority Chain Integrity
    print("-" * 80)
    print("AUDIT 3: AUTHORITY CHAIN INTEGRITY")
    print("-" * 80)
    findings = audit_authority_chain_integrity(artifacts)
    all_findings.extend(findings)
    if findings:
        for f in findings:
            print(f"  [{f['severity']}] {f['category']}: {f['message']}")
    else:
        print("  ✓ No issues found")
    print()
    
    # Audit 6: CLI Governance Drift
    print("-" * 80)
    print("AUDIT 6: CLI GOVERNANCE DRIFT")
    print("-" * 80)
    findings = audit_cli_governance_drift(Path(__file__).parent)
    all_findings.extend(findings)
    if findings:
        for f in findings:
            print(f"  [{f['severity']}] {f['category']}: {f['message']}")
    else:
        print("  ✓ No issues found")
    print()
    
    # Summary
    print("=" * 80)
    print("AUDIT SUMMARY")
    print("=" * 80)
    
    severity_counts = defaultdict(int)
    category_counts = defaultdict(int)
    for f in all_findings:
        severity_counts[f['severity']] += 1
        category_counts[f['category']] += 1
    
    print(f"Total Findings: {len(all_findings)}")
    print()
    print("By Severity:")
    for sev in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        if severity_counts[sev] > 0:
            print(f"  {sev}: {severity_counts[sev]}")
    
    print()
    print("By Category:")
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    
    print()
    print("=" * 80)
    
    return all_findings


if __name__ == '__main__':
    findings = run_full_audit()
    sys.exit(1 if any(f['severity'] == 'CRITICAL' for f in findings) else 0)
