# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: legacy-scripts
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
#!/usr/bin/env python3
"""
GL00-09 一致性問題修復腳本
修復8個已識別的一致性問題
"""

import json
import yaml
from datetime import datetime
from pathlib import Path

class ConsistencyFixer:
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.fixes_applied = []
        self.issues_found = {}
    
    def load_json(self, filepath):
        """載入 JSON 文件"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_json(self, filepath, data):
        """保存 JSON 文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_yaml(self, filepath):
        """載入 YAML 文件"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def save_yaml(self, filepath, data):
        """保存 YAML 文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
    
    def analyze_issue_001(self):
        """
        ISSUE-001: 數據一致性 - GL01 和 GL99 之間的風險等級
        """
        print("分析 ISSUE-001: 數據一致性 - 風險等級")
        
        gl01_path = self.base_path / "GL01-risk-registry.json"
        gl99_path = self.base_path / "GL99-unified-charter.json"
        
        gl01_data = self.load_json(gl01_path)
        gl99_data = self.load_json(gl99_path)
        
        # 檢查 GL01 的風險等級
        risk_levels_in_gl01 = set()
        if 'content' in gl01_data and 'risks' in gl01_data['content']:
            for risk in gl01_data['content']['risks']:
                if 'level' in risk:
                    risk_levels_in_gl01.add(risk['level'])
        
        # 檢查 GL99 的風險處理流程
        risk_levels_in_gl99 = set()
        if 'content' in gl99_data and 'governance_processes' in gl99_data['content']:
            for process in gl99_data['content']['governance_processes']:
                if process.get('name') == '風險管理' and 'stages' in process:
                    for stage in process['stages']:
                        if 'thresholds' in stage:
                            risk_levels_in_gl99.update(stage['thresholds'].keys())
        
        self.issues_found['ISSUE-001'] = {
            'gl01_risk_levels': list(risk_levels_in_gl01),
            'gl99_risk_levels': list(risk_levels_in_gl99),
            'inconsistent': risk_levels_in_gl01 != risk_levels_in_gl99
        }
        
        print(f"  GL01 風險等級: {risk_levels_in_gl01}")
        print(f"  GL99 風險等級: {risk_levels_in_gl99}")
        print(f"  一致性: {'✅' if not self.issues_found['ISSUE-001']['inconsistent'] else '❌'}")
        
        return self.issues_found['ISSUE-001']
    
    def fix_issue_001(self):
        """
        修復 ISSUE-001: 統一風險等級標準
        """
        print("\n修復 ISSUE-001: 統一風險等級標準")
        
        gl01_path = self.base_path / "GL01-risk-registry.json"
        gl99_path = self.base_path / "GL99-unified-charter.json"
        
        gl01_data = self.load_json(gl01_path)
        gl99_data = self.load_json(gl99_path)
        
        # 修復 GL01 的風險等級
        if 'content' in gl01_data and 'risks' in gl01_data['content']:
            for risk in gl01_data['content']['risks']:
                if 'level' in risk:
                    old_level = risk['level']
                    # 確保使用標準化的小寫格式
                    risk['level'] = old_level.lower()
                    self.fixes_applied.append(f"GL01 風險 '{risk.get('id', 'unknown')}' 等級標準化: {old_level} → {risk['level']}")
        
        # 修復 GL99 的風險處理流程閾值
        if 'content' in gl99_data and 'governance_processes' in gl99_data['content']:
            for process in gl99_data['content']['governance_processes']:
                if process.get('name') == '風險管理' and 'stages' in process:
                    for stage in process['stages']:
                        if 'thresholds' in stage:
                            # 標準化閾值鍵名
                            stage['thresholds'] = {
                                'critical': stage['thresholds'].get('critical', {}),
                                'high': stage['thresholds'].get('high', {}),
                                'medium': stage['thresholds'].get('medium', {}),
                                'low': stage['thresholds'].get('low', {})
                            }
                            self.fixes_applied.append("GL99 風險管理流程閾值標準化")
        
        self.save_json(gl01_path, gl01_data)
        self.save_json(gl99_path, gl99_data)
        
        print("  ✅ ISSUE-001 修復完成")
        return True
    
    def analyze_issue_002(self):
        """
        ISSUE-002: 模式一致性 - GL02 結構與 schema
        """
        print("\n分析 ISSUE-002: 模式一致性 - GL02 結構")
        
        gl02_path = self.base_path / "GL02-success-metrics.json"
        
        gl02_data = self.load_json(gl02_path)
        
        # 檢查 GL02 是否符合 schema 定義
        required_fields = ['id', 'type', 'version', 'created_at', 'content']
        missing_fields = [f for f in required_fields if f not in gl02_data]
        
        # 檢查 content 結構
        content_issues = []
        if 'content' in gl02_data:
            if 'metrics' not in gl02_data['content']:
                content_issues.append("缺少 'metrics' 字段")
            if 'categories' not in gl02_data['content']:
                content_issues.append("缺少 'categories' 字段")
        
        self.issues_found['ISSUE-002'] = {
            'missing_fields': missing_fields,
            'content_issues': content_issues,
            'has_issues': bool(missing_fields or content_issues)
        }
        
        print(f"  缺失字段: {missing_fields if missing_fields else '無'}")
        print(f"  Content 問題: {content_issues if content_issues else '無'}")
        print(f"  一致性: {'✅' if not self.issues_found['ISSUE-002']['has_issues'] else '❌'}")
        
        return self.issues_found['ISSUE-002']
    
    def fix_issue_002(self):
        """
        修復 ISSUE-002: 確保 GL02 符合 schema
        """
        print("\n修復 ISSUE-002: 確保 GL02 符合 schema")
        
        gl02_path = self.base_path / "GL02-success-metrics.json"
        
        gl02_data = self.load_json(gl02_path)
        
        # 確保所有必需字段存在
        if 'id' not in gl02_data:
            gl02_data['id'] = 'GL02'
            self.fixes_applied.append("添加 'id' 字段")
        
        if 'type' not in gl02_data:
            gl02_data['type'] = 'success-metrics'
            self.fixes_applied.append("添加 'type' 字段")
        
        if 'version' not in gl02_data:
            gl02_data['version'] = '1.0.0'
            self.fixes_applied.append("添加 'version' 字段")
        
        if 'created_at' not in gl02_data:
            gl02_data['created_at'] = datetime.now().isoformat()
            self.fixes_applied.append("添加 'created_at' 字段")
        
        # 確保 content 結構完整
        if 'content' not in gl02_data:
            gl02_data['content'] = {}
        
        if 'metrics' not in gl02_data['content']:
            gl02_data['content']['metrics'] = []
            self.fixes_applied.append("添加 'content.metrics' 字段")
        
        if 'categories' not in gl02_data['content']:
            gl02_data['content']['categories'] = []
            self.fixes_applied.append("添加 'content.categories' 字段")
        
        self.save_json(gl02_path, gl02_data)
        
        print("  ✅ ISSUE-002 修復完成")
        return True
    
    def analyze_issue_003(self):
        """
        ISSUE-003: 參考一致性 - Index 路徑不匹配
        """
        print("\n分析 ISSUE-003: 參考一致性 - Index 路徑")
        
        index_path = self.base_path / ".gl-index.json"
        index_data = self.load_json(index_path)
        
        # 檢查索引中的路徑是否存在
        path_issues = []
        if 'content' in index_data and 'artifacts' in index_data['content']:
            for artifact in index_data['content']['artifacts']:
                if 'path' in artifact:
                    artifact_path = self.base_path / artifact['path']
                    if not artifact_path.exists():
                        path_issues.append(f"路徑不存在: {artifact['path']}")
        
        self.issues_found['ISSUE-003'] = {
            'path_issues': path_issues,
            'has_issues': bool(path_issues)
        }
        
        print(f"  路徑問題: {len(path_issues)} 個")
        if path_issues:
            for issue in path_issues[:5]:  # 只顯示前5個
                print(f"    - {issue}")
        print(f"  一致性: {'✅' if not self.issues_found['ISSUE-003']['has_issues'] else '❌'}")
        
        return self.issues_found['ISSUE-003']
    
    def fix_issue_003(self):
        """
        修復 ISSUE-003: 修正索引路徑
        """
        print("\n修復 ISSUE-003: 修正索引路徑")
        
        index_path = self.base_path / ".gl-index.json"
        index_data = self.load_json(index_path)
        
        # 獲取實際存在的 GL 文件
        gl_files = list(self.base_path.glob("GL*.json"))
        valid_paths = [f.name for f in gl_files]
        
        # 更新索引
        if 'content' in index_data and 'artifacts' in index_data['content']:
            for artifact in index_data['content']['artifacts']:
                if 'path' in artifact:
                    filename = Path(artifact['path']).name
                    if filename not in valid_paths:
                        # 嘗試找到正確的文件
                        matching_files = [f for f in gl_files if filename in f.name]
                        if matching_files:
                            artifact['path'] = matching_files[0].name
                            self.fixes_applied.append(f"修正路徑: {artifact['path']}")
        
        self.save_json(index_path, index_data)
        
        print("  ✅ ISSUE-003 修復完成")
        return True
    
    def analyze_issue_004(self):
        """
        ISSUE-004: 元數據一致性 - 版本號格式
        """
        print("\n分析 ISSUE-004: 元數據一致性 - 版本號格式")
        
        version_issues = []
        gl_files = list(self.base_path.glob("GL*.json"))
        
        for gl_file in gl_files:
            data = self.load_json(gl_file)
            if 'version' in data:
                version = data['version']
                # 檢查是否符合 semver 格式
                import re
                if not re.match(r'^\d+\.\d+\.\d+', version):
                    version_issues.append({
                        'file': gl_file.name,
                        'version': version,
                        'issue': '不符合 semver 格式'
                    })
        
        self.issues_found['ISSUE-004'] = {
            'version_issues': version_issues,
            'has_issues': bool(version_issues)
        }
        
        print(f"  版本號問題: {len(version_issues)} 個")
        if version_issues:
            for issue in version_issues[:5]:
                print(f"    - {issue['file']}: {issue['version']}")
        print(f"  一致性: {'✅' if not self.issues_found['ISSUE-004']['has_issues'] else '❌'}")
        
        return self.issues_found['ISSUE-004']
    
    def fix_issue_004(self):
        """
        修復 ISSUE-004: 標準化版本號格式
        """
        print("\n修復 ISSUE-004: 標準化版本號格式")
        
        gl_files = list(self.base_path.glob("GL*.json"))
        
        for gl_file in gl_files:
            data = self.load_json(gl_file)
            if 'version' in data:
                old_version = data['version']
                # 轉換為標準 semver 格式
                import re
                # 移除前導 'v'
                version = re.sub(r'^v', '', old_version)
                # 確保三段式格式
                parts = version.split('.')
                if len(parts) < 3:
                    parts.extend(['0'] * (3 - len(parts)))
                data['version'] = '.'.join(parts[:3])
                
                if old_version != data['version']:
                    self.save_json(gl_file, data)
                    self.fixes_applied.append(f"{gl_file.name}: {old_version} → {data['version']}")
        
        print("  ✅ ISSUE-004 修復完成")
        return True
    
    def analyze_issue_005(self):
        """
        ISSUE-005: 語義一致性 - 類別標籤
        """
        print("\n分析 ISSUE-005: 語義一致性 - 類別標籤")
        
        gl02_path = self.base_path / "GL02-success-metrics.json"
        gl02_data = self.load_json(gl02_path)
        
        # 檢查指標類別的一致性
        category_issues = []
        if 'content' in gl02_data and 'metrics' in gl02_data['content']:
            categories_in_use = set()
            for metric in gl02_data['content']['metrics']:
                if 'category' in metric:
                    categories_in_use.add(metric['category'])
            
            if 'content' in gl02_data and 'categories' in gl02_data['content']:
                defined_categories = set(cat['id'] for cat in gl02_data['content']['categories'])
                undefined = categories_in_use - defined_categories
                if undefined:
                    category_issues.extend(list(undefined))
        
        self.issues_found['ISSUE-005'] = {
            'undefined_categories': category_issues,
            'has_issues': bool(category_issues)
        }
        
        print(f"  未定義的類別: {category_issues if category_issues else '無'}")
        print(f"  一致性: {'✅' if not self.issues_found['ISSUE-005']['has_issues'] else '❌'}")
        
        return self.issues_found['ISSUE-005']
    
    def fix_issue_005(self):
        """
        修復 ISSUE-005: 統一類別標籤
        """
        print("\n修復 ISSUE-005: 統一類別標籤")
        
        gl02_path = self.base_path / "GL02-success-metrics.json"
        gl02_data = self.load_json(gl02_path)
        
        # 定義標準類別映射
        category_mapping = {
            'strategic': 'strategic',
            'Strategic': 'strategic',
            'STRATEGIC': 'strategic',
            'customer': 'customer',
            'Customer': 'customer',
            'operational': 'operational',
            'Operational': 'operational',
            'quality': 'quality',
            'Quality': 'quality',
            'technical': 'technical',
            'Technical': 'technical',
            'talent': 'talent',
            'Talent': 'talent',
            'security': 'security',
            'Security': 'security',
            'compliance': 'compliance',
            'Compliance': 'compliance',
            'financial': 'financial',
            'Financial': 'financial',
            'innovation': 'innovation',
            'Innovation': 'innovation'
        }
        
        # 標準化指標類別
        if 'content' in gl02_data and 'metrics' in gl02_data['content']:
            for metric in gl02_data['content']['metrics']:
                if 'category' in metric:
                    old_category = metric['category']
                    new_category = category_mapping.get(old_category, old_category.lower())
                    if old_category != new_category:
                        metric['category'] = new_category
                        self.fixes_applied.append(f"指標 '{metric.get('id', 'unknown')}' 類別: {old_category} → {new_category}")
        
        # 確保所有使用的類別都在定義中
        if 'content' in gl02_data and 'metrics' in gl02_data['content']:
            categories_in_use = set()
            for metric in gl02_data['content']['metrics']:
                if 'category' in metric:
                    categories_in_use.add(metric['category'])
            
            if 'content' not in gl02_data:
                gl02_data['content'] = {}
            if 'categories' not in gl02_data['content']:
                gl02_data['content']['categories'] = []
            
            existing_category_ids = set(cat['id'] for cat in gl02_data['content']['categories'])
            for cat_id in categories_in_use:
                if cat_id not in existing_category_ids:
                    gl02_data['content']['categories'].append({
                        'id': cat_id,
                        'name': cat_id.title(),
                        'description': f'{cat_id.title()} metrics'
                    })
                    self.fixes_applied.append(f"添加類別定義: {cat_id}")
        
        self.save_json(gl02_path, gl02_data)
        
        print("  ✅ ISSUE-005 修復完成")
        return True
    
    def analyze_issue_006(self):
        """
        ISSUE-006: 數據格式一致性 - 日期格式
        """
        print("\n分析 ISSUE-006: 數據格式一致性 - 日期格式")
        
        date_issues = []
        gl_files = list(self.base_path.glob("GL*.json"))
        
        date_fields = ['created_at', 'updated_at', 'last_reviewed', 'effective_date']
        
        for gl_file in gl_files:
            data = self.load_json(gl_file)
            for field in date_fields:
                if field in data:
                    date_value = data[field]
                    # 檢查是否符合 ISO 8601 格式
                    try:
                        from datetime import datetime
                        datetime.fromisoformat(date_value.replace('Z', '+00:00'))
                    except (ValueError, AttributeError):
                        date_issues.append({
                            'file': gl_file.name,
                            'field': field,
                            'value': date_value,
                            'issue': '不符合 ISO 8601 格式'
                        })
        
        self.issues_found['ISSUE-006'] = {
            'date_issues': date_issues,
            'has_issues': bool(date_issues)
        }
        
        print(f"  日期格式問題: {len(date_issues)} 個")
        if date_issues:
            for issue in date_issues[:5]:
                print(f"    - {issue['file']}.{issue['field']}: {issue['value']}")
        print(f"  一致性: {'✅' if not self.issues_found['ISSUE-006']['has_issues'] else '❌'}")
        
        return self.issues_found['ISSUE-006']
    
    def fix_issue_006(self):
        """
        修復 ISSUE-006: 標準化日期格式為 ISO 8601
        """
        print("\n修復 ISSUE-006: 標準化日期格式為 ISO 8601")
        
        gl_files = list(self.base_path.glob("GL*.json"))
        
        date_fields = ['created_at', 'updated_at', 'last_reviewed', 'effective_date']
        
        for gl_file in gl_files:
            data = self.load_json(gl_file)
            modified = False
            for field in date_fields:
                if field in data:
                    old_value = data[field]
                    # 轉換為 ISO 8601 格式
                    try:
                        from datetime import datetime
                        # 嘗試解析常見格式
                        for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y']:
                            try:
                                parsed = datetime.strptime(old_value.split()[0], fmt)
                                data[field] = parsed.isoformat()
                                if old_value != data[field]:
                                    self.fixes_applied.append(f"{gl_file.name}.{field}: {old_value} → {data[field]}")
                                    modified = True
                                break
                            except ValueError:
                                continue
                    except Exception:
                        print(f"  警告: 無法轉換 {gl_file.name}.{field} = {old_value}")
            
            if modified:
                self.save_json(gl_file, data)
        
        print("  ✅ ISSUE-006 修復完成")
        return True
    
    def analyze_issue_007(self):
        """
        ISSUE-007: 交叉引用一致性 - GL99 角色定義
        """
        print("\n分析 ISSUE-007: 交叉引用一致性 - GL99 角色定義")
        
        gl99_path = self.base_path / "GL99-unified-charter.json"
        gl99_data = self.load_json(gl99_path)
        
        reference_issues = []
        if 'content' in gl99_data:
            # 檢查角色定義是否完整
            if 'roles' in gl99_data['content']:
                for role in gl99_data['content']['roles']:
                    if 'id' not in role or 'name' not in role:
                        reference_issues.append({
                            'role': role.get('id', 'unknown'),
                            'issue': '缺少必需字段 (id 或 name)'
                        })
            
            # 檢查治理流程中的角色引用
            if 'governance_processes' in gl99_data['content']:
                defined_roles = set()
                if 'roles' in gl99_data['content']:
                    defined_roles = set(role['id'] for role in gl99_data['content']['roles'])
                
                for process in gl99_data['content']['governance_processes']:
                    if 'stages' in process:
                        for stage in process['stages']:
                            if 'responsible' in stage:
                                for role_id in stage['responsible']:
                                    if role_id not in defined_roles:
                                        reference_issues.append({
                                            'process': process.get('name', 'unknown'),
                                            'role_id': role_id,
                                            'issue': '引用的未定義角色'
                                        })
        
        self.issues_found['ISSUE-007'] = {
            'reference_issues': reference_issues,
            'has_issues': bool(reference_issues)
        }
        
        print(f"  交叉引用問題: {len(reference_issues)} 個")
        if reference_issues:
            for issue in reference_issues[:5]:
                print(f"    - {issue}")
        print(f"  一致性: {'✅' if not self.issues_found['ISSUE-007']['has_issues'] else '❌'}")
        
        return self.issues_found['ISSUE-007']
    
    def fix_issue_007(self):
        """
        修復 ISSUE-007: 修正角色定義和引用
        """
        print("\n修復 ISSUE-007: 修正角色定義和引用")
        
        gl99_path = self.base_path / "GL99-unified-charter.json"
        gl99_data = self.load_json(gl99_path)
        
        # 確保所有角色都有必需字段
        if 'content' in gl99_data and 'roles' in gl99_data['content']:
            for role in gl99_data['content']['roles']:
                if 'id' not in role:
                    role['id'] = role.get('name', 'unknown').lower().replace(' ', '_')
                    self.fixes_applied.append(f"添加角色 ID: {role['id']}")
                if 'name' not in role:
                    role['name'] = role.get('id', 'Unknown').title().replace('_', ' ')
                    self.fixes_applied.append(f"添加角色名稱: {role['name']}")
        
        self.save_json(gl99_path, gl99_data)
        
        print("  ✅ ISSUE-007 修復完成")
        return True
    
    def analyze_issue_008(self):
        """
        ISSUE-008: 命名約定一致性 - 統一命名規則
        """
        print("\n分析 ISSUE-008: 命名約定一致性 - 命名規則")
        
        naming_issues = []
        gl_files = list(self.base_path.glob("GL*.json"))
        
        for gl_file in gl_files:
            data = self.load_json(gl_file)
            
            # 檢查 ID 格式
            if 'id' in data:
                file_id = gl_file.stem.upper()
                data_id = data['id'].upper()
                if file_id != data_id:
                    naming_issues.append({
                        'file': gl_file.name,
                        'file_id': file_id,
                        'data_id': data_id,
                        'issue': '文件名與 ID 不匹配'
                    })
        
        self.issues_found['ISSUE-008'] = {
            'naming_issues': naming_issues,
            'has_issues': bool(naming_issues)
        }
        
        print(f"  命名問題: {len(naming_issues)} 個")
        if naming_issues:
            for issue in naming_issues[:5]:
                print(f"    - {issue['file']}: {issue['file_id']} vs {issue['data_id']}")
        print(f"  一致性: {'✅' if not self.issues_found['ISSUE-008']['has_issues'] else '❌'}")
        
        return self.issues_found['ISSUE-008']
    
    def fix_issue_008(self):
        """
        修復 ISSUE-008: 統一命名規則
        """
        print("\n修復 ISSUE-008: 統一命名規則")
        
        gl_files = list(self.base_path.glob("GL*.json"))
        
        for gl_file in gl_files:
            data = self.load_json(gl_file)
            
            # 確保 ID 與文件名一致
            if 'id' in data:
                file_id = gl_file.stem.upper()
                old_id = data['id']
                if file_id != old_id.upper():
                    data['id'] = file_id
                    self.save_json(gl_file, data)
                    self.fixes_applied.append(f"{gl_file.name}: ID {old_id} → {file_id}")
        
        print("  ✅ ISSUE-008 修復完成")
        return True
    
    def run_all_analyses(self):
        """運行所有分析"""
        print("=" * 60)
        print("GL00-09 一致性問題分析")
        print("=" * 60)
        
        results = {}
        for i in range(1, 9):
            method_name = f'analyze_issue_{i:03d}'
            if hasattr(self, method_name):
                method = getattr(self, method_name)
                results[f'ISSUE-{i:03d}'] = method()
        
        return results
    
    def run_all_fixes(self):
        """運行所有修復"""
        print("\n" + "=" * 60)
        print("GL00-09 一致性問題修復")
        print("=" * 60)
        
        results = {}
        for i in range(1, 9):
            method_name = f'fix_issue_{i:03d}'
            if hasattr(self, method_name):
                method = getattr(self, method_name)
                results[f'ISSUE-{i:03d}'] = method()
        
        print("\n" + "=" * 60)
        print("修復總結")
        print("=" * 60)
        print(f"應用的修復: {len(self.fixes_applied)} 項")
        for fix in self.fixes_applied[:10]:  # 顯示前10項
            print(f"  - {fix}")
        if len(self.fixes_applied) > 10:
            print(f"  ... 還有 {len(self.fixes_applied) - 10} 項修復")
        
        return results

def main():
    """主函數"""
    # 初始化修復器
    fixer = ConsistencyFixer(base_path="/workspace/machine-native-ops")
    
    # 運行分析
    print("開始分析...")
    analysis_results = fixer.run_all_analyses()
    
    # 保存分析結果
    results_file = "/workspace/machine-native-ops/consistency_analysis_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'analysis_results': analysis_results,
            'issues_found': fixer.issues_found
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n分析結果已保存到: {results_file}")
    
    # 運行修復
    print("\n開始修復...")
    fix_results = fixer.run_all_fixes()
    
    # 保存修復結果
    fixes_file = "/workspace/machine-native-ops/consistency_fixes_applied.json"
    with open(fixes_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'fixes_applied': fixer.fixes_applied,
            'fix_results': fix_results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n修復結果已保存到: {fixes_file}")
    
    # 統計
    issues_with_problems = sum(1 for v in fixer.issues_found.values() if v.get('has_issues', False))
    print("\n" + "=" * 60)
    print("統計")
    print("=" * 60)
    print(f"發現問題的問題: {issues_with_problems}/8")
    print(f"應用的修復數量: {len(fixer.fixes_applied)}")
    print("\n所有修復已完成！")

if __name__ == "__main__":
    main()