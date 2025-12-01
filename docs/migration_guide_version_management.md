# 版本管理 Skills 迁移指南

## 概述

本指南帮助您从旧的版本管理 Skills (`manage_document_version_change` 和 `maintain_version_relationships`) 迁移到新的统一 Skill (`manage_knowledge_version`)。

**迁移日期**: 2025-12-01  
**弃用期限**: 2026-06-01（6个月后完全移除旧 Skills）  
**影响范围**: 版本管理相关的所有工作流

## 为什么要合并？

### 问题分析

旧的两个 Skills 存在 30-40% 的功能重叠：

1. **版本关系更新** (40% 重叠)
   - 两者都输出版本关系信息
   - 都涉及版本映射和关联

2. **依赖关系验证** (30% 重叠)
   - 都进行依赖关系检查
   - 都验证更新一致性

3. **组件更新协调** (35% 重叠)
   - 都处理多组件版本更新
   - 都需要协调组件间关系

### 合并优势

✅ **消除重复**：整合重叠的 30-40% 功能  
✅ **统一接口**：一个 skill 完成完整的版本管理  
✅ **简化调用**：LLM 只需选择一个 skill  
✅ **降低维护成本**：从 2 个 skills 减少到 1 个  
✅ **提升一致性**：统一的验证和错误处理逻辑

## 快速迁移对照表

| 场景 | 旧方式 | 新方式 |
|------|--------|--------|
| 简单内容更新 | `manage_document_version_change(mode="single_entry")` | `manage_knowledge_version(mode="single_entry")` |
| 复杂文档变更 | `manage_document_version_change(mode="document_level")` + `maintain_version_relationships(...)` | `manage_knowledge_version(mode="document_level")` |
| 纯关系维护 | `maintain_version_relationships(...)` | `manage_knowledge_version(mode="relationship_only")` |

## 详细迁移指南

### 场景1：单条目内容更新

#### 旧方式（manage_document_version_change）

```json
{
  "skill": "manage_document_version_change",
  "mode": "single_entry",
  "knowledge_id": "knl_001",
  "updated_content": {
    "title": "员工年假管理规定（2024年修订）",
    "content": "更新后的政策内容..."
  },
  "change_reason": "根据最新劳动法调整年假政策"
}
```

#### 新方式（manage_knowledge_version）

```json
{
  "skill": "manage_knowledge_version",
  "mode": "single_entry",
  "version_change": {
    "knowledge_id": "knl_001",
    "updated_content": {
      "title": "员工年假管理规定（2024年修订）",
      "content": "更新后的政策内容..."
    },
    "change_reason": "根据最新劳动法调整年假政策"
  }
}
```

**变化说明**：

- 参数结构调整：将更新信息包装在 `version_change` 对象中
- 功能增强：自动创建基本的版本映射关系

---

### 场景2：文档级批量变更

#### 旧方式（需要两步）

**步骤1：更新内容**

```json
{
  "skill": "manage_document_version_change",
  "mode": "document_level",
  "changed_document": {
    "document_id": "policy_001",
    "new_version": "v2.0",
    "content": "更新后的文档内容...",
    "change_summary": "更新年假计算规则"
  },
  "previous_version": {
    "version_id": "v1.0",
    "content": "前一版本内容..."
  }
}
```

**步骤2：维护关系**

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
  "component_dependencies": {
    "knl_001": ["tags_001", "faq_001"]
  }
}
```

#### 新方式（一步完成）

```json
{
  "skill": "manage_knowledge_version",
  "mode": "document_level",
  "version_change": {
    "knowledge_id": "knl_001",
    "updated_content": {
      "title": "员工年假管理规定（2024年修订）",
      "content": "更新后的文档内容..."
    },
    "change_reason": "根据最新劳动法调整年假政策",
    "change_summary": "更新年假计算规则，增加特殊情况处理"
  },
  "relationship_maintenance": {
    "version_changes": [
      {
        "component_type": "knowledge_entry",
        "old_version_id": "knl_001_v1",
        "new_version_id": "knl_001_v2",
        "change_type": "content_update"
      },
      {
        "component_type": "tags",
        "old_version_id": "tags_001_v1",
        "new_version_id": "tags_001_v2",
        "change_type": "structural_update"
      }
    ],
    "component_dependencies": {
      "knl_001": ["tags_001", "faq_001", "knowledge_points_001"],
      "tags_001": ["knowledge_graph_001"]
    }
  }
}
```

**变化说明**：

- **一步完成**：无需分两次调用，内容变更和关系维护自动整合
- **统一验证**：自动执行内容一致性、关系完整性和依赖正确性验证
- **完整输出**：返回版本变更状态、版本映射、溯源路径和依赖关系图

---

### 场景3：纯关系维护

#### 旧方式（maintain_version_relationships）

```json
{
  "skill": "maintain_version_relationships",
  "version_changes": [
    {
      "component_type": "knowledge_entry",
      "old_version_id": "knl_001_v1",
      "new_version_id": "knl_001_v2",
      "change_type": "content_update"
    }
  ],
  "component_dependencies": {
    "knl_001": ["tags_001", "faq_001"]
  },
  "traceability_requirements": {
    "maintain_full_history": true,
    "enable_rollback": true
  }
}
```

#### 新方式（manage_knowledge_version）

```json
{
  "skill": "manage_knowledge_version",
  "mode": "relationship_only",
  "relationship_maintenance": {
    "version_changes": [
      {
        "component_type": "knowledge_entry",
        "old_version_id": "knl_001_v1",
        "new_version_id": "knl_001_v2",
        "change_type": "content_update"
      }
    ],
    "component_dependencies": {
      "knl_001": ["tags_001", "faq_001"]
    }
  },
  "options": {
    "maintain_full_history": true,
    "enable_rollback": true
  }
}
```

**变化说明**：

- 新增 `mode="relationship_only"` 模式
- 跳过内容更新阶段，专注于关系维护
- 配置选项移至 `options` 对象

---

## 输出格式变化

### 旧输出（分散在两个 Skills）

**manage_document_version_change 输出**：

```json
{
  "update_status": {...},
  "backup_location": "...",
  "change_history": {...},
  "version_relationships": {...}  // 部分版本关系信息
}
```

**maintain_version_relationships 输出**：

```json
{
  "version_mappings": [...],
  "traceability_paths": [...],
  "dependency_graph": {...},
  "maintenance_status": {...}
}
```

### 新输出（统一格式）

```json
{
  "version_update": {
    "status": "success",
    "knowledge_id": "knl_001",
    "previous_version": "v1.0",
    "new_version": "v2.0",
    "backup_location": "/backups/knl_001_v1_20240120"
  },
  "version_mappings": [...],
  "traceability_paths": [...],
  "dependency_graph": {...},
  "validation_results": {
    "content_consistency": {...},
    "relationship_integrity": {...},
    "dependency_correctness": {...}
  },
  "processing_stats": {...}
}
```

**优势**：

- 所有信息集中在一个响应中
- 新增统一的验证结果
- 新增处理统计信息

---

## 工作模式选择指南

### mode="single_entry" - 单条目更新模式

**适用场景**：

- 快速修改单个知识条目的内容
- 简单的元数据更新
- 不涉及复杂的组件依赖

**特点**：

- 快速高效（平均 2-3 秒）
- 自动创建备份
- 建立基本版本映射
- 适合日常维护

**示例**：

```
更新年假政策中的某个条款
修改FAQ的答案内容
更正知识点的描述
```

---

### mode="document_level" - 文档级变更模式

**适用场景**：

- 文档级别的重大更新
- 涉及多个关联组件（tags、FAQ、knowledge_points、knowledge_graph）
- 需要完整的版本溯源和依赖分析

**特点**：

- 完整的版本管理（平均 60-120 秒）
- 自动协调多组件更新
- 完整的依赖分析和关系维护
- 构建版本溯源路径

**示例**：

```
发布新版本的政策文档
重大业务规则变更
知识库结构性调整
```

---

### mode="relationship_only" - 关系维护模式

**适用场景**：

- 批量修复版本映射关系
- 优化依赖关系图
- 不涉及内容更新的关系维护

**特点**：

- 专注关系维护（平均 2-5 秒）
- 跳过内容更新阶段
- 适合批量关系修复
- 性能优化场景

**示例**：

```
修复历史版本映射错误
重建依赖关系图
批量更新溯源路径
```

---

## 迁移检查清单

### 代码迁移

- [ ] 识别所有使用 `manage_document_version_change` 的地方
- [ ] 识别所有使用 `maintain_version_relationships` 的地方
- [ ] 更新 Skill 调用为 `manage_knowledge_version`
- [ ] 调整输入参数结构（添加 `mode` 和 `version_change`/`relationship_maintenance`）
- [ ] 更新输出处理逻辑（适配新的统一输出格式）

### 测试验证

- [ ] 测试单条目更新场景
- [ ] 测试文档级变更场景
- [ ] 测试纯关系维护场景
- [ ] 验证版本映射正确性
- [ ] 验证溯源路径完整性
- [ ] 验证依赖关系准确性

### 文档更新

- [ ] 更新工作流文档
- [ ] 更新 API 文档
- [ ] 更新用户手册
- [ ] 通知相关团队成员

---

## 常见问题 (FAQ)

### Q1: 旧 Skills 何时会被完全移除？

**A**: 旧 Skills 将保留 6 个月（至 2026-06-01），期间标记为 `DEPRECATED`。建议在 2026年3月前完成迁移。

### Q2: 迁移后性能会有影响吗？

**A**: 不会。新 Skill 在单条目更新模式下性能相当，在文档级变更模式下由于整合了两个步骤，反而提升了整体效率。

### Q3: 如果我只需要内容更新，不需要关系维护怎么办？

**A**: 使用 `mode="single_entry"`，系统会自动创建基本的版本映射，但不会执行深度的依赖分析和关系维护。

### Q4: 新 Skill 是否向后兼容？

**A**: 输入参数结构有调整，不完全向后兼容。但我们提供了 6 个月的过渡期和详细的迁移指南。

### Q5: 遇到迁移问题怎么办？

**A**:

1. 查看本迁移指南
2. 查看新 Skill 的 [SKILL.md](../.claude/skills/manage_knowledge_version/SKILL.md)
3. 查看实施计划文档
4. 联系知识库管理团队

---

## 技术支持

### 文档资源

- [manage_knowledge_version SKILL.md](../.claude/skills/manage_knowledge_version/SKILL.md) - 完整的 Skill 文档
- [implementation_plan.md](implementation_plan.md) - 详细的实施计划
- [README.md](../README.md) - 系统概览

### 联系方式

如有问题或需要帮助，请：

1. 查阅上述文档资源
2. 提交 Issue 到项目仓库
3. 联系知识库管理团队

---

## 迁移时间表

| 时间节点 | 里程碑 | 说明 |
|---------|--------|------|
| 2025-12-01 | 新 Skill 发布 | `manage_knowledge_version` 正式可用 |
| 2025-12-01 | 旧 Skills 标记为弃用 | 添加 DEPRECATED 标记 |
| 2026-03-01 | 建议迁移完成日期 | 给予 3 个月迁移时间 |
| 2026-06-01 | 旧 Skills 完全移除 | 不再支持旧 Skills |

---

**祝迁移顺利！** 🚀

如有任何问题，请随时查阅文档或联系支持团队。
