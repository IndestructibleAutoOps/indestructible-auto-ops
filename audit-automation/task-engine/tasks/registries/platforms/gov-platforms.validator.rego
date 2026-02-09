package gl.platforms.validator

# GL Platforms Validator - 命名與結構驗證器
# 用於驗證平台命名、結構、位置與合規性

# 規則定義
deny[msg] {
    # GL-PD-001: 命名格式驗證
    platform := input.platform_id
    not regex.match("^gl\\.[a-z]+\\.[a-z]+-platform$", platform)
    msg := sprintf("GL-PD-001: 平台名稱 '%s' 必須符合 gl.{domain}.{capability}-platform 格式", [platform])
}

deny[msg] {
    # GL-PD-002: 單一位置驗證
    platform_id := input.platform_id
    locations := [loc | input.platforms[loc].platform_id == platform_id]
    count(locations) > 1
    msg := sprintf("GL-PD-002: 平台 '%s' 在多個位置重複存在：%v", [platform_id, locations])
}

deny[msg] {
    # GL-PD-003: 契約註冊驗證
    platform := input.platform_id
    input.platform_type == "contract"
    not contains(input.contract_platforms, platform)
    msg := sprintf("GL-PD-003: 契約平台 '%s' 必須在 gl-platforms.yaml 中註冊", [platform])
}

deny[msg] {
    # GL-PD-004: Manifest 存在驗證
    platform := input.platform_id
    input.platform_type == "contract"
    not input.manifests[platform]
    msg := sprintf("GL-PD-004: 平台 '%s' 必須在 registry 中有 manifest 檔案", [platform])
}

deny[msg] {
    # GL-PD-005: 目錄結構驗證
    platform := input.platform_id
    input.platform_type == "contract"
    not input.platform_structure[platform].standard_subdirectories
    msg := sprintf("GL-PD-005: 平台 '%s' 目錄必須包含標準子目錄", [platform])
}

deny[msg] {
    # GL-PD-006: Capabilities 定義驗證
    platform := input.platform_id
    count(input.platforms[platform].capabilities) == 0
    msg := sprintf("GL-PD-006: 平台 '%s' 必須定義至少一個能力", [platform])
}

deny[msg] {
    # GL-PD-007: 治理層級驗證
    platform := input.platform_id
    count(input.platforms[platform].governance) == 0
    msg := sprintf("GL-PD-007: 平台 '%s' 必須聲明遵循的治理層級", [platform])
}

deny[msg] {
    # GL-PD-008: 擴展框架支援驗證
    platform := input.platform_id
    not input.platforms[platform].extension_support
    msg := sprintf("GL-PD-008: 平台 '%s' 應支援 GL81-83 擴展框架", [platform])
}

# PR-001: 契約平台位置規則
deny[msg] {
    platform := input.platform_id
    input.platforms[platform].contract_compliant == true
    input.platforms[platform].location != "platforms/"
    msg := sprintf("PR-001: 契約平台 '%s' 必須位於 platforms/ 目錄", [platform])
}

# PR-002: 自定義平台位置規則
warn[msg] {
    platform := input.platform_id
    input.platforms[platform].contract_compliant == false
    not contains(["root/", "custom/"], input.platforms[platform].location)
    msg := sprintf("PR-002: 自定義平台 '%s' 建議放置於 root/ 或 custom/ 目錄", [platform])
}

# PR-003: 實驗性平台規則
warn[msg] {
    platform := input.platform_id
    input.platforms[platform].domain == "gl.experimental"
    input.platforms[platform].location != "platforms/experimental/"
    msg := sprintf("PR-003: 實驗性平台 '%s' 建議放置於 platforms/experimental/ 目錄", [platform])
}

# PR-004: 已退役平台規則
deny[msg] {
    platform := input.platform_id
    input.platforms[platform].status == "deprecated"
    input.platforms[platform].location != "platforms/deprecated/"
    msg := sprintf("PR-004: 已退役平台 '%s' 必須移至 platforms/deprecated/ 目錄", [platform])
}

# PR-005: 重複平台規則 (已由 GL-PD-002 覆蓋，保留作為參考)
deny[msg] {
    platform_id := input.platform_id
    locations := [loc | input.platforms[loc].platform_id == platform_id]
    count(locations) > 1
    msg := sprintf("PR-005: 平台 '%s' 不能在多個位置重複存在（違反 SSOT 原則）", [platform_id])
}

# PR-006: 平台狀態驗證
warn[msg] {
    platform := input.platform_id
    input.platforms[platform].status == "active"
    input.platforms[platform].location == "platforms/deprecated/"
    msg := sprintf("PR-006: 平台 '%s' 狀態為 active 但位於 deprecated 目錄", [platform])
}

# PR-007: 命名空間驗證 (已由 GL-PD-001 覆蓋，保留作為參考)
deny[msg] {
    platform := input.platform_id
    not regex.match("^gl\\.[a-z]+\\.[a-z]+-platform$", platform)
    msg := sprintf("PR-007: 平台名稱 '%s' 必須符合 gl.{domain}.{capability}-platform 格式", [platform])
}

# PR-008: 目錄結構驗證 (已由 GL-PD-005 覆蓋，保留作為參考)
warn[msg] {
    platform := input.platform_id
    input.platform_type == "contract"
    not input.platform_structure[platform].standard_subdirectories
    msg := sprintf("PR-008: 平台 '%s' 目錄必須包含標準子目錄", [platform])
}

# PR-009: Manifest 註冊規則 (已由 GL-PD-004 覆蓋，保留作為參考)
warn[msg] {
    platform := input.platform_id
    not input.manifests[platform]
    msg := sprintf("PR-009: 平台 '%s' 必須在 registry/platform-registry/ 中註冊 manifest", [platform])
}

# PR-010: 治理層級驗證 (已由 GL-PD-007 覆蓋，保留作為參考)
warn[msg] {
    platform := input.platform_id
    count(input.platforms[platform].governance) == 0
    msg := sprintf("PR-010: 平台 '%s' 必須聲明遵循的治理層級", [platform])
}

# 輔助函數
contains(array, value) {
    array[_] == value
}

# 驗證報告生成
report = {
    "platform_id": input.platform_id,
    "compliance": {
        "naming": not deny["GL-PD-001"],
        "location": not deny["GL-PD-002"] and not deny["PR-001"],
        "structure": not deny["GL-PD-005"],
        "registry": not deny["GL-PD-004"],
        "governance": not deny["GL-PD-007"],
        "extension": not deny["GL-PD-008"]
    },
    "warnings": [msg | warn[msg]],
    "errors": [msg | deny[msg]]
}

# 批量驗證
batch_report = {
    "total_platforms": count(input.platforms),
    "compliant_platforms": count([p | input.platforms[p].contract_compliant == true]),
    "non_compliant_platforms": count([p | input.platforms[p].contract_compliant == false]),
    "duplicate_platforms": count([p | count([l | input.platforms[l].platform_id == p]) > 1]),
    "platforms": [report | p := input.platforms[p].platform_id]
}