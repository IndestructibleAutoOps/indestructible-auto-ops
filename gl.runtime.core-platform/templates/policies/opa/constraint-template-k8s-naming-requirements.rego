# OPA Gatekeeper 約束模板 - Kubernetes 命名要求

package k8snamingrequirements

import data.lib.exclude

# 檢查命名規範違規
violation[{"msg": msg}] {
    # 檢查命名空間名稱長度
    count(input.review.object.metadata.name) > input.parameters.maxLength
    msg := sprintf("命名空間名稱 '%v' 超過最大長度 %v", [input.review.object.metadata.name, input.parameters.maxLength])
}

violation[{"msg": msg}] {
    # 檢查命名模式
    not regex.match(input.parameters.namingPattern, input.review.object.metadata.name)
    msg := sprintf("命名空間名稱 '%v' 不符合命名模式 '%v'", [input.review.object.metadata.name, input.parameters.namingPattern])
}

violation[{"msg": msg}] {
    # 檢查禁用模式
    some i
    forbidden := input.parameters.forbiddenPatterns[i]
    regex.match(forbidden, input.review.object.metadata.name)
    msg := sprintf("命名空間名稱 '%v' 包含禁用模式 '%v'", [input.review.object.metadata.name, forbidden])
}

violation[{"msg": msg}] {
    # 檢查必要標籤
    some i
    required_label := input.parameters.requiredLabels[i]
    not input.review.object.metadata.labels[required_label]
    msg := sprintf("命名空間缺少必要標籤: %v", [required_label])
}

violation[{"msg": msg}] {
    # 檢查保留字
    some i
    reserved := input.parameters.reservedWords[i]
    input.review.object.metadata.name == reserved
    msg := sprintf("命名空間名稱 '%v' 是保留字，不能使用", [reserved])
}