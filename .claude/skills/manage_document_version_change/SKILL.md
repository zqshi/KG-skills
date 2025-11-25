---
name: manage_document_version_change
description: 管理文档版本变更，支持单个知识条目更新和文档级批量版本管理，提供版本备份、变更历史记录和一致性验证
tools: [Read, Write, Edit]
---

# manage_document_version_change - 文档版本变更管理器

## 🎯 核心功能

管理文档版本变更，支持两种模式：
1. **单条目更新模式**：更新单个知识条目的内容和元数据，验证权限并备份原内容
2. **文档级变更模式**：管理文档级别的批量版本变更，协调多个相关组件的更新

## 📋 工作流SOP

**工作流SOP**：
```
1. 接收变更请求
2. 识别变更模式（单条目/文档级）
3. 验证更新权限
4. 备份原内容
5. 应用更新内容
6. 更新版本信息
7. 验证更新一致性
8. 记录变更历史
9. 返回更新状态
```

### 详细流程说明

**步骤1：接收变更请求**
- 验证知识ID或文档ID的有效性和存在性
- 检查更新内容的完整性和格式
- 解析变更原因和版本说明
- 记录变更请求基本信息

**步骤2：识别变更模式**
- **单条目更新模式**：单个知识条目的原子更新
- **文档级变更模式**：文档级别的批量版本变更
- 根据输入参数自动识别模式
- 生成模式识别结果

**步骤3：验证更新权限**
- 检查用户的更新权限
- 验证知识条目的锁定状态
- 确认更新操作的合法性
- 生成权限验证报告

**步骤4：备份原内容**
- 创建当前版本的完整备份
- 记录备份位置和时间戳
- 确保备份数据的可恢复性
- 生成备份确认信息

**步骤5：应用更新内容**
- 将更新内容应用到知识条目或文档
- 处理内容冲突和合并
- 更新相关字段和属性
- 验证更新内容的格式

**步骤6：更新版本信息**
- 生成新的版本号
- 更新版本元数据
- 记录版本变更摘要
- 建立版本关联关系

**步骤7：验证更新一致性**
- 检查更新后的内容完整性
- 验证与其他知识的一致性
- 检查引用关系的有效性
- 生成一致性验证报告

**步骤8：记录变更历史**
- 创建变更记录条目
- 记录详细的变更内容
- 关联变更原因和说明
- 生成完整的变更历史

**步骤9：返回更新状态**
- 返回更新操作的状态
- 提供新版本号信息
- 返回备份位置
- 提供变更历史记录

## 🚀 快速开始

### 基本使用（单条目更新模式）
```
使用 manage_document_version_change 更新年假政策内容
知识ID：knl_001
更新内容：新的年假计算规则
变更原因：根据最新劳动法调整年假政策
```

### 基本使用（文档级变更模式）
```
使用 manage_document_version_change 管理年假政策版本变更
变更文档：年假政策v2.0
前一版本：v1.0
变更描述：更新年假计算规则，增加特殊情况处理
影响评估：影响标签、FAQ、知识点、知识图谱
```

### 支持的变更类型
- **内容更新**: 知识内容的修改和更新
- **结构调整**: 知识结构的重组和调整
- **元数据更新**: 元数据的更新和维护
- **规则变更**: 业务规则和计算方法的变更
- **新增内容**: 新增章节和内容

## 📋 输入规范

### 必需输入（单条目更新模式）
```json
{
  "knowledge_id": "knl_001",
  "updated_content": {
    "title": "员工年假管理规定（2024年修订）",
    "content": "更新后的政策内容..."
  },
  "change_reason": "根据最新劳动法调整年假政策"
}
```

### 必需输入（文档级变更模式）
```json
{
  "changed_document": {
    "document_id": "policy_001",
    "new_version": "v2.0",
    "content": "更新后的文档内容...",
    "change_summary": "更新年假计算规则，增加特殊情况处理"
  },
  "previous_version": {
    "version_id": "v1.0",
    "content": "前一版本内容..."
  },
  "change_description": "详细描述变更内容和原因"
}
```

### 可选输入
```json
{
  "update_mode": "single_entry",
  "impact_assessment": {
    "affected_components": ["tags", "faq", "knowledge_points", "knowledge_graph"],
    "estimated_effort": "4小时"
  },
  "backup_settings": {
    "create_backup": true,
    "backup_location": "/backups"
  }
}
```

## 📤 输出内容

### 标准输出（单条目更新模式）
```json
{
  "update_status": {
    "status": "success",
    "knowledge_id": "knl_001",
    "previous_version": "v1.0",
    "new_version": "v2.0"
  },
  "backup_location": "/backups/knl_001_v1_20240120_103000",
  "change_history": {
    "change_id": "chg_001",
    "changes_made": ["更新年假计算规则", "增加特殊情况处理"]
  }
}
```

### 标准输出（文档级变更模式）
```json
{
  "version_update_status": {
    "status": "success",
    "document_id": "policy_001",
    "new_version": "v2.0",
    "previous_version": "v1.0",
    "update_time": "2024-01-20T10:30:00Z"
  },
  "updated_components": {
    "tags": {
      "status": "updated",
      "changes": ["新增标签：特殊情况处理", "修改标签：计算规则"],
      "processing_time": 15
    },
    "faq": {
      "status": "updated",
      "changes": ["新增FAQ：特殊情况处理", "修改FAQ：计算规则"],
      "processing_time": 25
    },
    "knowledge_points": {
      "status": "updated",
      "changes": ["新增知识点：特殊情况", "修改知识点：计算方法"],
      "processing_time": 20
    },
    "knowledge_graph": {
      "status": "updated",
      "changes": ["更新实体关系", "添加新实体"],
      "processing_time": 30
    }
  },
  "version_relationships": {
    "direct_predecessor": "v1.0",
    "successor_versions": [],
    "related_versions": ["v1.1", "v1.2"],
    "derivation_path": "v1.0 → v1.1 → v1.2 → v2.0"
  },
  "consistency_check": {
    "status": "passed",
    "checks_performed": 12,
    "issues_found": 0,
    "validation_time": 5
  }
}
```

## 📊 质量指标

- **更新成功率**: ≥98%（目标值）
- **版本管理准确率**: 100%（目标值）
- **备份成功率**: 100%（目标值）
- **版本更新成功率**: ≥95%（目标值）
- **组件更新成功率**: ≥98%（目标值）
- **关联关系准确率**: ≥98%（目标值）
- **一致性验证通过率**: ≥95%（目标值）

---

**manage_document_version_change** - 智能版本变更管理，确保知识一致性！ 🔄