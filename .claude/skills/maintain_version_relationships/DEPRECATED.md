# DEPRECATED

此 Skill 已被 `manage_knowledge_version` 替代。

## 迁移说明

**旧 Skill**: `maintain_version_relationships`  
**新 Skill**: `manage_knowledge_version`  
**弃用日期**: 2025-12-01  
**移除计划**: 2026-06-01（6个月后）

## 功能映射

### 版本关系维护

**旧调用方式**:

```json
{
  "skill": "maintain_version_relationships",
  "version_changes": [
    {
      "component_type": "knowledge_entry",
      "old_version_id": "knl_001_v1",
      "new_version_id": "knl_001_v2"
    }
  ],
  "component_dependencies": {...}
}
```

**新调用方式**:

```json
{
  "skill": "manage_knowledge_version",
  "mode": "relationship_only",
  "relationship_maintenance": {
    "version_changes": [
      {
        "component_type": "knowledge_entry",
        "old_version_id": "knl_001_v1",
        "new_version_id": "knl_001_v2"
      }
    ],
    "component_dependencies": {...}
  }
}
```

### 与内容更新结合

**旧调用方式**（需要两步）:

```
步骤1: manage_document_version_change(...)
步骤2: maintain_version_relationships(...)
```

**新调用方式**（一步完成）:

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

- ✅ 自动整合内容更新和关系维护
- ✅ 无需手动协调两个 Skills
- ✅ 统一的验证和错误处理
- ✅ 更高的处理效率

## 详细文档

查看完整的迁移指南和使用文档：

- [manage_knowledge_version SKILL.md](../../.claude/skills/manage_knowledge_version/SKILL.md)
- [迁移指南](../../docs/migration_guide_version_management.md)

## 支持

如有问题，请参考：

- 新 Skill 文档
- 实施计划：`implementation_plan.md`
- 或联系知识库管理团队
