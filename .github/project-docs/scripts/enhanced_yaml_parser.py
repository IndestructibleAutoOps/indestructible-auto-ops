# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: legacy-scripts
# @GL-audit-trail: ../../engine/gl_platform_universe.gl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
#!/usr/bin/env python3
"""
Enhanced YAML Parser
Handles both single and multi-document YAML files with comprehensive validation
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
# MNGA-002: Import organization needs review
import yaml
import json
from pathlib import Path
from typing import List, Dict, Any, Union
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EnhancedYAMLParser:
    """Enhanced YAML parser that handles both single and multi-document YAML files"""
    
    def __init__(self):
        self.parse_results = []
        self.validation_errors = []
        self.validation_warnings = []
    
    def parse_yaml_file(self, file_path: str) -> Union[Dict, List[Dict], None]:
        """
        Parse YAML file, handling both single and multi-document formats
        
        Args:
            file_path: Path to YAML file
            
        Returns:
            Dict for single document, List[Dict] for multiple documents, None on error
        """
        try:
            logger.info(f"Parsing file: {file_path}")
            
            path = Path(file_path)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if file has multiple documents
            document_count = content.count('---')
            
            # Check if --- is at line 9 (where first document ends)
            lines = content.split('\n')
            first_doc_separator = None
            for idx, line in enumerate(lines):
                if line.strip() == '---':
                    first_doc_separator = idx
                    break
            
            # Better detection: check if file has --- markers
            # If there's at least one --- marker, try safe_load_all first
            # This handles both single and multi-document files correctly
            has_multiple = document_count >= 1
            
            if has_multiple:
                # Multi-document YAML - use safe_load_all
                logger.info(f"Detected multi-document YAML with {document_count} document markers (first at line {first_doc_separator})")
                try:
                    documents = list(yaml.safe_load_all(content))
                    
                    # Filter out None documents (result of trailing ---)
                    documents = [doc for doc in documents if doc is not None]
                    
                    if len(documents) == 0:
                        self.validation_errors.append(f"No valid documents found in {file_path}")
                        return None
                    elif len(documents) == 1:
                        logger.info("Parsed as single document (filtered from multi-document)")
                        return documents[0]
                    else:
                        logger.info(f"Parsed {len(documents)} documents")
                        return documents
                except yaml.YAMLError as e:
                    # If safe_load_all fails, try safe_load as fallback
                    logger.warning(f"safe_load_all failed, trying safe_load: {str(e)}")
                    try:
                        data = yaml.safe_load(content)
                        logger.info("Successfully parsed with safe_load fallback")
                        return data
                    except yaml.YAMLError as e2:
                        raise ValueError(f"Both safe_load_all and safe_load failed: {str(e)}, {str(e2)}")
            else:
                # Single document YAML
                logger.info("Detected single-document YAML")
                data = yaml.safe_load(content)
                return data
                
        except yaml.YAMLError as e:
            error_msg = f"YAML parsing error in {file_path}: {str(e)}"
            logger.error(error_msg)
            self.validation_errors.append(error_msg)
            return None
        except FileNotFoundError:
            error_msg = f"File not found: {file_path}"
            logger.error(error_msg)
            self.validation_errors.append(error_msg)
            return None
        except Exception as e:
            error_msg = f"Error reading {file_path}: {str(e)}"
            logger.error(error_msg)
            self.validation_errors.append(error_msg)
            return None
    
    def validate_yaml_structure(self, data: Union[Dict, List], file_path: str) -> Dict[str, Any]:
        """
        Validate YAML structure and return metadata
        
        Args:
            data: Parsed YAML data
            file_path: Source file path
            
        Returns:
            Validation metadata
        """
        validation_result = {
            'file': file_path,
            'valid': True,
            'type': 'unknown',
            'document_count': 0,
            'metadata_present': False,
            'errors': [],
            'warnings': []
        }
        
        try:
            if isinstance(data, list):
                # Multi-document
                validation_result['type'] = 'multi-document'
                validation_result['document_count'] = len(data)
                validation_result['valid'] = all(doc is not None for doc in data)
                
                # Check each document
                for idx, doc in enumerate(data):
                    if doc is None:
                        validation_result['errors'].append(f"Document {idx + 1} is None")
                    elif isinstance(doc, dict):
                        if 'metadata' in doc:
                            validation_result['metadata_present'] = True
                            self._validate_metadata(doc['metadata'], validation_result)
                    else:
                        validation_result['warnings'].append(f"Document {idx + 1} is not a dictionary")
                
            elif isinstance(data, dict):
                # Single document
                validation_result['type'] = 'single-document'
                validation_result['document_count'] = 1
                validation_result['valid'] = data is not None
                
                # Check for metadata
                if 'metadata' in data:
                    validation_result['metadata_present'] = True
                    self._validate_metadata(data['metadata'], validation_result)
                else:
                    validation_result['warnings'].append("No metadata section found")
                
            else:
                # Unknown type
                validation_result['type'] = 'unknown'
                validation_result['document_count'] = 0
                validation_result['valid'] = False
                validation_result['errors'].append(f"Unknown data type: {type(data)}")
            
            # Store result
            self.parse_results.append(validation_result)
            
        except Exception as e:
            validation_result['valid'] = False
            validation_result['errors'].append(f"Validation error: {str(e)}")
            logger.error(f"Validation error for {file_path}: {str(e)}")
        
        return validation_result
    
    def _validate_metadata(self, metadata: Dict, validation_result: Dict):
        """Validate metadata section"""
        required_fields = ['version', 'description', 'author']
        
        for field in required_fields:
            if field not in metadata:
                validation_result['warnings'].append(f"Missing required metadata field: {field}")
        
        # Validate version format
        if 'version' in metadata:
            version = metadata['version']
            if not isinstance(version, str):
                validation_result['warnings'].append(f"Version should be a string, got {type(version)}")
            elif not version.replace('.', '').isdigit():
                validation_result['warnings'].append(f"Version format may be invalid: {version}")
    
    def parse_and_validate(self, file_path: str) -> Dict[str, Any]:
        """
        Parse and validate YAML file in one operation
        
        Args:
            file_path: Path to YAML file
            
        Returns:
            Combined parse and validation result
        """
        logger.info(f"Parsing and validating: {file_path}")
        
        # Parse file
        data = self.parse_yaml_file(file_path)
        
        # Validate structure
        validation_result = {}
        if data is not None:
            validation_result = self.validate_yaml_structure(data, file_path)
        else:
            validation_result = {
                'file': file_path,
                'valid': False,
                'type': 'error',
                'document_count': 0,
                'metadata_present': False,
                'errors': self.validation_errors[-1:] if self.validation_errors else ["Unknown error"],
                'warnings': []
            }
        
        # Add parsed data to result
        validation_result['data'] = data
        
        return validation_result
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive validation report
        
        Returns:
            Validation report with statistics and details
        """
        total_files = len(self.parse_results)
        valid_files = sum(1 for r in self.parse_results if r['valid'])
        invalid_files = total_files - valid_files
        
        # Count types
        single_doc = sum(1 for r in self.parse_results if r['type'] == 'single-document')
        multi_doc = sum(1 for r in self.parse_results if r['type'] == 'multi-document')
        
        # Metadata presence
        with_metadata = sum(1 for r in self.parse_results if r['metadata_present'])
        
        # Collect all errors and warnings
        all_errors = []
        all_warnings = []
        
        for result in self.parse_results:
            all_errors.extend([f"{result['file']}: {err}" for err in result['errors']])
            all_warnings.extend([f"{result['file']}: {warn}" for warn in result['warnings']])
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_files': total_files,
                'valid_files': valid_files,
                'invalid_files': invalid_files,
                'success_rate': f"{(valid_files/total_files*100):.1f}%" if total_files > 0 else "0%",
                'single_document_files': single_doc,
                'multi_document_files': multi_doc,
                'files_with_metadata': with_metadata
            },
            'errors': all_errors,
            'warnings': all_warnings,
            'details': self.parse_results
        }
        
        return report


def test_parser_on_files(file_paths: List[str]) -> Dict[str, Any]:
    """
    Test the enhanced parser on a list of files
    
    Args:
        file_paths: List of file paths to test
        
    Returns:
        Test results report
    """
    parser = EnhancedYAMLParser()
    
    print("\n" + "="*60)
    print("Enhanced YAML Parser - Testing")
    print("="*60 + "\n")
    
    for file_path in file_paths:
        result = parser.parse_and_validate(file_path)
        
        status = "✓ PASSED" if result['valid'] else "✗ FAILED"
        print(f"{status} | {file_path}")
        print(f"  Type: {result['type']}")
        print(f"  Documents: {result['document_count']}")
        print(f"  Metadata: {'Yes' if result['metadata_present'] else 'No'}")
        
        if result['errors']:
            print(f"  Errors: {len(result['errors'])}")
            for error in result['errors']:
                print(f"    - {error}")
        
        if result['warnings']:
            print(f"  Warnings: {len(result['warnings'])}")
            for warning in result['warnings']:
                print(f"    - {warning}")
        
        print()
    
    # Generate report
    report = parser.generate_report()
    
    print("="*60)
    print("Test Summary")
    print("="*60)
    print(f"Total Files: {report['summary']['total_files']}")
    print(f"Valid: {report['summary']['valid_files']}")
    print(f"Invalid: {report['summary']['invalid_files']}")
    print(f"Success Rate: {report['summary']['success_rate']}")
    print(f"Single Document: {report['summary']['single_document_files']}")
    print(f"Multi Document: {report['summary']['multi_document_files']}")
    print(f"With Metadata: {report['summary']['files_with_metadata']}")
    print(f"Total Errors: {len(report['errors'])}")
    print(f"Total Warnings: {len(report['warnings'])}")
    print("="*60 + "\n")
    
    return report


def main():
    """Main execution function"""
    
    # Test on the problematic files
    problematic_files = [
        "/workspace/machine-native-ops/gl_platform_universe.gl_platform_universe.governance/naming-gl_platform_universe.gl_platform_universe.governance-v1.0.0-extended/gl_platform_universe.gl_platform_universe.governance/naming/naming-gl_platform_universe.gl_platform_universe.governance-core.yaml",
        "/workspace/machine-native-ops/gl_platform_universe.gl_platform_universe.governance/naming-gl_platform_universe.gl_platform_universe.governance-v1.0.0-extended/monitoring/prometheus-rules.yaml",
        "/workspace/machine-native-ops/gl_platform_universe.gl_platform_universe.governance/policies/gatekeeper/namespace-constraints.yaml",
        "/workspace/machine-native-ops/gl_platform_universe.gl_platform_universe.governance/quantum-naming-v4-0-0/deployment/quantum-deployment-manifest.yaml"
    ]
    
    # Filter to existing files
    existing_files = [f for f in problematic_files if Path(f).exists()]
    
    if not existing_files:
        print("No files found to test")
        return
    
    # Run tests
    report = test_parser_on_files(existing_files)
    
    # Save report
    report_path = Path("/workspace/machine-native-ops/workspace/enhanced_parser_test_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✓ Test report saved to: {report_path}")


if __name__ == "__main__":
    main()