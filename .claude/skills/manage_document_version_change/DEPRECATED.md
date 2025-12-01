# DEPRECATED

此 Skill 已被 `manage_knowledge_version` 替代。

## 迁移说明

**旧 Skill**: `manage_document_version_change`  
**新 Skill**: `manage_knowledge_version`  
**弃用日期**: 2025-12-01  
**移除计划**: 2026-06-01（6个月后）

## 功能映射

### 单条目更新模式

**旧调用方式**:

```json
{
  "skill": "manage_document_version_change",
  "mode": "single_entry",
  "knowledge_id": "knl_001",
  "updated_content": {...},
  "change_reason": "..."
}
```

**新调用方式**:

```json
{
  "skill": "manage_knowledge_version",
  "mode": "single_entry",
  "version_change": {
    "knowledge_id": "knl_001",
    "updated_content": {...},
    "change_reason": "..."
  }
}
```

### 文档级变更模式

**旧调用方式**:

```json
{
  "skill": "manage_document_version_change",
  "mode": "document_level",
  "changed_document": {...},
  "previous_version": {...}
}
```

**新调用方式**:

```json
{
  "skill": "manage_knowledge_version",
  "mode": "document_level",
  "version_change": {...},
  "relationship_maintenance": {...}
}
```

## 优势

新的 `manage_knowledge_version` 提供：

- ✅ 统一的版本管理接口
- ✅ 自动的关系维护（无需单独调用 `maintain_version_relationships`）
- ✅ 更完整的验证机制
- ✅ 更清晰的工作模式划分

## 详细文档

查看完整的迁移指南和使用文档：

- [manage_knowledge_version SKILL.md](../../.claude/skills/manage_knowledge_version/SKILL.md)
- [迁移指南](../../docs/migration_guide_version_management.md)

## 支持

如有问题，请参考：

- 新 Skill 文档
- 实施计划：`implementation_plan.md`
- 或联系知识库管理团队
