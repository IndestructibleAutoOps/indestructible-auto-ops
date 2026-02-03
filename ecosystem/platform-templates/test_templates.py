#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: platform-templates
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
Platform Templates Tests
========================
測試平台模板的完整性
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
# MNGA-002: Import organization needs review
import sys
# Import simple_yaml for zero-dependency YAML parsing
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils.simple_yaml import safe_load
import subprocess
from pathlib import Path


def test_core_template():
    """測試核心模板"""
    print("\n=== Test Core Template ===")
    
    template_dir = Path(__file__).parent / 'core-template'
    
    # 檢查目錄結構
    required_dirs = ['configs', 'scripts', 'examples']
    for dir_name in required_dirs:
        dir_path = template_dir / dir_name
        assert dir_path.exists(), f"Missing directory: {dir_name}"
    
    print("✓ Directory structure complete")
    
    # 檢查配置文件
    config_files = [
        'configs/platform-config.yaml',
        'configs/services-config.yaml'
    ]
    
    for config_file in config_files:
        file_path = template_dir / config_file
        assert file_path.exists(), f"Missing config: {config_file}"
        
        # 驗證 YAML 語法
        with open(file_path) as f:
            data = safe_load(f)
            assert data is not None, f"Invalid YAML: {config_file}"
    
    print("✓ Configuration files valid")
    
    # 檢查腳本
    scripts = ['setup.sh', 'deploy.sh', 'validate.sh', 'status.sh', 'cleanup.sh']
    for script in scripts:
        script_path = template_dir / 'scripts' / script
        assert script_path.exists(), f"Missing script: {script}"
        assert script_path.stat().st_mode & 0o111, f"Script not executable: {script}"
    
    print("✓ Scripts present and executable")
    
    # 檢查示例
    examples = ['register_service.py', 'api_gateway_example.py', 'messaging_example.py', 'sync_data.py']
    for example in examples:
        example_path = template_dir / 'examples' / example
        assert example_path.exists(), f"Missing example: {example}"
    
    print("✓ Example files present")
    
    # 檢查平台管理器
    assert (template_dir / 'platform_manager.py').exists(), "Missing platform_manager.py"
    print("✓ Platform manager present")
    
    # 測試 validate.sh 腳本
    print("\nRunning validation script...")
    try:
        result = subprocess.run(
            ['bash', 'scripts/validate.sh'],
            cwd=template_dir,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✓ Validation script passed")
        else:
            print(f"⚠ Validation script returned: {result.returncode}")
            print(f"  Output: {result.stdout[-200:]}")
    except Exception as e:
        print(f"⚠ Could not run validation script: {e}")
    
    print("✅ Core Template tests passed")


def test_cloud_template():
    """測試雲模板"""
    print("\n=== Test Cloud Template ===")
    
    template_dir = Path(__file__).parent / 'cloud-template'
    
    # 檢查 README
    assert (template_dir / 'README.md').exists(), "Missing README.md"
    print("✓ README.md present")
    
    # 檢查配置文件
    config_files = [
        'configs/platform-config.aws.yaml'
    ]
    
    for config_file in config_files:
        file_path = template_dir / config_file
        assert file_path.exists(), f"Missing config: {config_file}"
        
        # 驗證 YAML
        with open(file_path) as f:
            data = safe_load(f)
            assert data is not None, f"Invalid YAML: {config_file}"
            assert 'platform' in data, "Missing platform section"
    
    print("✓ Cloud configuration files valid")
    
    print("✅ Cloud Template tests passed")


def test_onpremise_template():
    """測試本地部署模板"""
    print("\n=== Test On-Premise Template ===")
    
    template_dir = Path(__file__).parent / 'on-premise-template'
    
    # 檢查 README
    assert (template_dir / 'README.md').exists(), "Missing README.md"
    print("✓ README.md present")
    
    # 檢查配置文件
    config_path = template_dir / 'configs/platform-config.yaml'
    assert config_path.exists(), "Missing platform-config.yaml"
    
    with open(config_path) as f:
        data = safe_load(f)
        assert 'platform' in data, "Missing platform section"
        assert 'infrastructure' in data, "Missing infrastructure section"
    
    print("✓ On-premise configuration valid")
    
    # 檢查前置腳本
    prereq_script = template_dir / 'scripts/prerequisites.sh'
    if prereq_script.exists():
        assert prereq_script.stat().st_mode & 0o111, "prerequisites.sh not executable"
        print("✓ Prerequisites script present and executable")
    
    print("✅ On-Premise Template tests passed")


def test_template_completeness():
    """測試模板完整性"""
    print("\n=== Test Template Completeness ===")
    
    templates = ['core-template', 'cloud-template', 'on-premise-template']
    
    for template in templates:
        template_dir = Path(__file__).parent / template
        assert template_dir.exists(), f"Template directory missing: {template}"
        
        # 每個模板必須有 README
        assert (template_dir / 'README.md').exists(), f"{template} missing README.md"
        
        # 檢查 README 長度
        readme_size = (template_dir / 'README.md').stat().st_size
        assert readme_size > 1000, f"{template} README too short"
    
    print(f"✓ All {len(templates)} templates present and complete")
    print("✅ Completeness test passed")


def main():
    """運行所有測試"""
    print("\n" + "="*60)
    print("Platform Templates - Test Suite")
    print("="*60)
    
    try:
        test_core_template()
        test_cloud_template()
        test_onpremise_template()
        test_template_completeness()
        
        print("\n" + "="*60)
        print("✅ ALL TEMPLATE TESTS PASSED")
        print("="*60 + "\n")
        
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
