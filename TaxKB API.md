# TaxKB REST API v3.0 完整文档

**版本**: 3.0.0
**最后更新**: 2025-11-24
**适用场景**: 传统业务系统集成（HR系统、财务系统、OA系统等）

---

## 目录

- [1. 概述](#1-概述)
- [2. v3.0核心设计理念](#2-v30核心设计理念)
- [3. 基础信息](#3-基础信息)
- [4. 核心资源API](#4-核心资源api)
  - [4.1 文档资源（Documents）](#41-文档资源documents)
  - [4.2 标签资源（Tags）](#42-标签资源tags)
  - [4.3 任务资源（Processings & Jobs）](#43-任务资源processings--jobs)
  - [4.4 关系资源（Relations）](#44-关系资源relations)
- [5. 搜索功能](#5-搜索功能)
  - [5.1 文档检索（Document Search）](#51-文档检索document-search)
  - [5.2 语义搜索（Semantic Search）](#52-语义搜索semantic-search)
- [6. 统计分析](#6-统计分析)
- [7. 完整使用示例](#7-完整使用示例)
- [8. 错误处理](#8-错误处理)
- [9. 从v2.1迁移指南](#9-从v21迁移指南)
- [10. 附录](#10-附录)

---

## 1. 概述

### 1.1 什么是TaxKB REST API v3.0

TaxKB REST API v3.0 是围绕**四大核心要素**设计的知识库管理接口：

```
┌─────────────────────────────────────────┐
│       TaxKB 四大核心要素                 │
├─────────────────────────────────────────┤
│  1️⃣ 文档（Document）                    │
│     系统的核心对象，承载知识内容         │
│                                         │
│  2️⃣ 标签（Tag）                         │
│     对文档内容的结构化抽象               │
│                                         │
│  3️⃣ 任务（Processing & Job）            │
│     将文档转化为知识的处理流程           │
│                                         │
│  4️⃣ 关系（Relation）                    │
│     连接各种实体，形成知识网络           │
└─────────────────────────────────────────┘
```

**v3.0核心特性**：
- ✅ **资源化设计**：文档、标签、关系是一等资源，Job是任务处理的一等公民
- ✅ **职责分离**：上传存储、任务调度、关系管理各司其职
- ✅ **灵活可组合**：支持任意任务组合和关系构建
- ✅ **完整的搜索能力**：文档检索 + 语义搜索
- ✅ **统计分析**：独立的stats端点提供多维度统计

### 1.2 架构定位

```
┌─────────────────────────────────────────┐
│      应用层（业务系统）                  │
│   HR系统、财务系统、OA系统等             │
└─────────────────────────────────────────┘
                    │
                    │ HTTP/REST
                    ▼
┌─────────────────────────────────────────┐
│         TaxKB REST API v3.0             │
│                                         │
│  📄 Documents  📑 Tags                   │
│  ⚙️  Processings  🔗 Relations(计划中)   │
│  🔍 Search     📊 Stats                  │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│      DuckDB + LanceDB + SQLite          │
└─────────────────────────────────────────┘
```

---

## 2. v3.0核心设计理念

### 2.1 围绕四大核心要素组织API

```
/api/v3/
│
├── documents/      # 文档资源（核心要素1）
├── tags/           # 标签资源（核心要素2）
├── processings/    # 任务资源（核心要素3）
├── jobs/           # Job资源（细粒度任务）
├── relations/      # 关系资源（核心要素4 - 计划中）⏳
│
├── search/         # 搜索功能（跨资源）
└── stats/          # 统计分析（跨资源）
```

### 2.2 接口职责分离

```
上传文档（存储） ≠ 处理文档（调度）
查询文档（元数据） ≠ 搜索内容（语义）
管理关系（关系） ≠ 文档属性（元数据）
```

**设计原则**：
- 每个资源有清晰的CRUD操作
- 每个端点只做一件事
- 用户可以自由组合原子操作

### 2.3 与v2.1的核心变更

| 特性 | v2.1 | v3.0 |
|------|------|------|
| **关系管理** | 散落在各处，没有统一抽象 | 独立的Relations资源 ⏳ (计划中) |
| **搜索功能** | 语义搜索 + 模糊的文档查询 | 明确分离：检索 vs 语义 ✅ |
| **统计分析** | 无 | 独立的Stats端点 ✅ |
| **任务管理** | Processing | Job（一等公民）+ Processing（分组标识）✅ |

---

## 3. 基础信息

### 3.1 基础URL

**本地开发**: `http://localhost:8000/api/v3`
**测试环境**: `http://localhost:9601/api/v3`
**生产环境**: `http://<your-domain>/api/v3`

### 3.2 认证方式

**API Key认证**（Header）:
```http
X-API-Key: sk-taxkb-admin-prod-VldMpvuKDD0QbZ4bu8HOTA
```

**测试环境API Key**:
```
sk-taxkb-admin-test-TESTADMIN123456789ABC
```

### 3.3 请求格式

**Content-Type**:
- 上传文档: `multipart/form-data`
- 其他端点: `application/json`

### 3.4 响应格式

**成功响应** (HTTP 200/201):
```json
{
  "doc_id": "doc_abc123",
  "status": "uploaded"
}
```

**错误响应** (HTTP 4xx/5xx):
```json
{
  "detail": "错误描述信息"
}
```

### 3.5 HTTP状态码

| 状态码 | 说明 | 示例 |
|-------|------|------|
| 200 | 成功 | 查询成功 |
| 201 | 创建成功 | 文档上传成功 |
| 400 | 请求错误 | 参数格式错误 |
| 401 | 未授权 | API Key无效 |
| 404 | 资源不存在 | doc_id不存在 |
| 422 | 验证错误 | 标签约束违反 |
| 500 | 服务器错误 | 内部处理失败 |

---

## 4. 核心资源API

### 4.1 文档资源（Documents）

文档是知识库的核心对象，承载原始知识内容。

#### 完整端点列表

```
POST   /api/v3/documents              # 上传文档
GET    /api/v3/documents/{doc_id}     # 查询文档详情
PATCH  /api/v3/documents/{doc_id}     # 更新文档元数据
DELETE /api/v3/documents/{doc_id}     # 删除文档
PATCH  /api/v3/documents/{doc_id}/tags    # 修改文档标签
GET    /api/v3/documents/{doc_id}/content # 获取L1全文内容
```

---

#### 4.1.1 POST /api/v3/documents - 上传文档

**描述**: 上传单个文档到知识库，**只负责存储，不自动触发处理**。

**请求格式**: `multipart/form-data`

**参数**:

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| file | File | ✅ 是 | 文档文件（PDF/DOCX/XLSX/TXT） |
| metadata | JSON字符串 | ❌ 否 | 文档元数据 |

**metadata格式**:
```json
{
  "title": "北京总部产假管理规定（2025年修订版）",
  "description": "详细说明产假天数、申请流程等",
  "tags": {
    "主体": ["北京总部"],
    "业务领域": ["假期管理/生育假期"],
    "时间维度": ["2025年", "Q4"]
  }
}
```

**响应**:
```json
{
  "doc_id": "doc_abc123",
  "status": "uploaded",
  "message": "文档上传成功",
  "document": {
    "title": "北京总部产假管理规定（2025年修订版）",
    "file_hash": "a1b2c3d4e5f6...",
    "file_size": 245678,
    "file_path": "/data/files/2025/11/产假政策.pdf",
    "file_extension": "pdf",
    "created_at": "2025-11-24T10:00:00Z"
  },
  "tags": {
    "主体": [
      {"tag_id": "tag_001", "name": "北京总部", "verified": true}
    ],
    "业务领域": [
      {"tag_id": "tag_102", "name": "假期管理/生育假期", "verified": true}
    ]
  }
}
```

**curl示例**:
```bash
curl -X POST http://localhost:9601/api/v3/documents \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC" \
  -F "file=@产假政策.pdf" \
  -F 'metadata={"title":"产假政策2025","tags":{"主体":["北京总部"]}}'
```

**注意事项**:
- ✅ 只负责存储，不自动创建Processing
- ✅ 如需处理，需单独调用 `POST /api/v3/processings`
- ✅ 重复文件（相同hash）会返回已存在记录
- ✅ 最大文件大小: 50MB

---

#### 4.1.2 GET /api/v3/documents/{doc_id} - 查询文档详情

**描述**: 查询文档的完整信息，包括元数据、标签、处理结果。

**路径参数**:
- `doc_id`: 文档ID

**查询参数**:

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| include | string | ❌ 否 | 包含的字段，逗号分隔。可选值: tags, l1, l2, l3, relations |

**响应**:
```json
{
  "doc_id": "doc_abc123",
  "title": "北京总部产假管理规定（2025年修订版）",
  "file_hash": "a1b2c3d4e5f6...",
  "file_size": 245678,
  "file_extension": "pdf",
  "processing_status": "completed",
  "quality_score": 0.92,
  "created_at": "2025-11-24T10:00:00Z",
  "updated_at": "2025-11-24T10:01:30Z",

  "tags": {
    "主体": [
      {"tag_id": "tag_001", "name": "北京总部", "verified": true}
    ],
    "业务领域": [
      {"tag_id": "tag_102", "name": "假期管理/生育假期", "verified": true}
    ]
  },

  "l1_summary": {
    "page_count": 5,
    "extraction_model": "pymupdf",
    "extracted_at": "2025-11-24T10:00:15Z",
    "has_tables": true,
    "has_images": false
  },

  "l2_summary": {
    "strategy": "full_document",
    "chunk_count": 1,
    "embedding_model": "text-embedding-v4",
    "vectorized_at": "2025-11-24T10:00:35Z"
  },

  "l3_summary": {
    "one_sentence": "北京总部员工产假为128天，包括国家规定98天及北京市延长30天。",
    "summary": "本政策详细规定了北京总部员工的产假管理办法...",
    "llm_model": "claude-3-5-haiku-20241022",
    "processed_at": "2025-11-24T10:01:00Z"
  },

  "relations": {
    "version": [
      {"relation_id": "rel_001", "target_doc_id": "doc_xyz", "similarity": 0.95}
    ],
    "similar": [
      {"relation_id": "rel_002", "target_doc_id": "doc_def", "similarity": 0.82}
    ]
  }
}
```

**curl示例**:
```bash
# 基本信息
curl "http://localhost:9601/api/v3/documents/doc_abc123" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC"

# 包含所有信息
curl "http://localhost:9601/api/v3/documents/doc_abc123?include=tags,l1,l2,l3,relations" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC"
```

---

#### 4.1.3 PATCH /api/v3/documents/{doc_id} - 更新文档元数据

**描述**: 更新文档的元数据（标题、描述等），不包括标签（标签有专用端点）。

**路径参数**:
- `doc_id`: 文档ID

**请求体**:
```json
{
  "title": "北京总部产假管理规定（2025年修订版-最终版）",
  "description": "更新了第三章内容"
}
```

**响应**:
```json
{
  "doc_id": "doc_abc123",
  "message": "文档元数据已更新",
  "updated_fields": ["title", "description"],
  "updated_at": "2025-11-24T15:30:00Z"
}
```

---

#### 4.1.4 DELETE /api/v3/documents/{doc_id} - 删除文档

**描述**: 删除文档及其所有关联数据（标签、关系、向量等）。

**路径参数**:
- `doc_id`: 文档ID

**响应**:
```json
{
  "doc_id": "doc_abc123",
  "message": "文档已删除",
  "deleted_at": "2025-11-24T15:30:00Z"
}
```

**注意事项**:
- ⚠️ 删除操作不可逆
- ⚠️ 会同时删除L1/L2/L3数据、标签关联、关系记录

---

#### 4.1.5 PATCH /api/v3/documents/{doc_id}/tags - 修改文档标签

**描述**: 修改文档的标签，支持添加、移除、替换、确认操作。

**路径参数**:
- `doc_id`: 文档ID

**请求体**:
```json
{
  "action": "add",  // add | remove | replace | verify
  "tags": {
    "内容标签": ["育儿假", "家庭照护假"]
  }
}
```

**操作类型**:

| 操作 | 说明 |
|-----|------|
| `add` | 添加新标签 |
| `remove` | 移除标签 |
| `replace` | 替换维度的所有标签 |
| `verify` | 确认自动提取的标签 |

**响应**:
```json
{
  "doc_id": "doc_abc123",
  "action": "add",
  "message": "成功添加2个标签",
  "updated_tags": {
    "added": [
      {"tag_id": "tag_302", "name": "育儿假"},
      {"tag_id": "tag_303", "name": "家庭照护假"}
    ]
  },
  "current_tags": {
    "内容标签": [
      {"tag_id": "tag_301", "name": "产假"},
      {"tag_id": "tag_302", "name": "育儿假"},
      {"tag_id": "tag_303", "name": "家庭照护假"}
    ]
  }
}
```

**curl示例**:
```bash
# 添加标签
curl -X PATCH "http://localhost:9601/api/v3/documents/doc_abc123/tags" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC" \
  -H "Content-Type: application/json" \
  -d '{"action": "add", "tags": {"内容标签": ["育儿假"]}}'

# 移除标签
curl -X PATCH "http://localhost:9601/api/v3/documents/doc_abc123/tags" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC" \
  -H "Content-Type: application/json" \
  -d '{"action": "remove", "tags": {"内容标签": ["育儿假"]}}'
```

---

#### 4.1.6 GET /api/v3/documents/{doc_id}/content - 获取L1全文内容

**描述**: 获取文档的L1提取全文内容（可能很大，单独端点）。

**路径参数**:
- `doc_id`: 文档ID

**响应**:
```json
{
  "doc_id": "doc_abc123",
  "l1_full_text": "根据国家和北京市相关政策，北京总部员工产假天数规定如下...",
  "page_count": 5,
  "extraction_model": "pymupdf",
  "extracted_at": "2025-11-24T10:00:15Z",
  "tables": [
    {
      "table_id": "table_001",
      "page": 2,
      "caption": "产假天数明细表"
    }
  ],
  "images": []
}
```

---

### 4.2 标签资源（Tags）

标签是对文档内容的结构化抽象，用于多维度分类和过滤。

#### 完整端点列表

```
GET    /api/v3/tags                   # 查询标签列表
POST   /api/v3/tags                   # 创建标签
GET    /api/v3/tags/{tag_id}          # 查询标签详情
PATCH  /api/v3/tags/{tag_id}          # 修改标签
DELETE /api/v3/tags/{tag_id}          # 删除标签
GET    /api/v3/tags/{tag_id}/documents    # 查询标签下的文档
```

---

#### 4.2.1 GET /api/v3/tags - 查询标签列表

**描述**: 查询标签体系，支持扁平列表或树状结构。

**查询参数**:

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| dimension | string | ❌ 否 | 标签维度 |
| tree | boolean | ❌ 否 | 是否返回树状结构（默认false） |
| include_counts | boolean | ❌ 否 | 是否包含文档数量（默认false） |

**响应（扁平列表）**:
```json
{
  "dimension": "内容标签",
  "total_tags": 50,
  "tags": [
    {
      "tag_id": "tag_301",
      "name": "产假",
      "dimension": "内容标签",
      "full_path": "产假",
      "description": "产假相关内容",
      "document_count": 5
    }
  ]
}
```

**响应（树状结构）**:
```json
{
  "dimension": "业务领域",
  "total_tags": 13,
  "tree": [
    {
      "tag_id": "tag_100",
      "name": "假期管理",
      "level": 1,
      "document_count": 12,
      "children": [
        {"tag_id": "tag_101", "name": "年假", "level": 2, "document_count": 3},
        {"tag_id": "tag_102", "name": "生育假期", "level": 2, "document_count": 8}
      ]
    }
  ]
}
```

**curl示例**:
```bash
# 查询所有标签（扁平）
curl "http://localhost:9601/api/v3/tags" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC"

# 查询树状结构（含文档数）
curl "http://localhost:9601/api/v3/tags?dimension=业务领域&tree=true&include_counts=true" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC"
```

---

#### 4.2.2 POST /api/v3/tags - 创建标签

**描述**: 创建新标签，支持单个标签或层级标签（自动创建中间节点）。

**请求体（单个标签）**:
```json
{
  "name": "育儿假",
  "dimension": "内容标签",
  "description": "育儿假相关内容"
}
```

**请求体（层级标签）**:
```json
{
  "dimension": "业务领域",
  "full_path": "薪酬福利/工资薪酬",
  "description": "工资薪酬管理"
}
```

**响应**:
```json
{
  "target_tag": {
    "tag_id": "tag_302",
    "name": "育儿假",
    "dimension": "内容标签",
    "full_path": "育儿假",
    "created_at": "2025-11-24T15:00:00Z"
  }
}
```

---

#### 4.2.3 GET /api/v3/tags/{tag_id} - 查询标签详情

**描述**: 查询标签的详细信息，包括关联的文档数量、父子关系等。

**路径参数**:
- `tag_id`: 标签ID

**响应**:
```json
{
  "tag_id": "tag_102",
  "name": "生育假期",
  "dimension": "业务领域",
  "parent_tag_id": "tag_100",
  "full_path": "假期管理/生育假期",
  "level": 2,
  "description": "生育相关假期政策",
  "document_count": 8,
  "children": [],
  "created_at": "2025-01-01T00:00:00Z"
}
```

---

#### 4.2.4 GET /api/v3/tags/{tag_id}/documents - 查询标签下的文档

**描述**: 查询使用了该标签的所有文档。

**路径参数**:
- `tag_id`: 标签ID

**查询参数**:

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| include_children | boolean | ❌ 否 | 是否包含子标签的文档（默认false） |
| limit | integer | ❌ 否 | 返回数量（默认50） |
| offset | integer | ❌ 否 | 偏移量（默认0） |

**响应**:
```json
{
  "tag_id": "tag_102",
  "tag_name": "生育假期",
  "full_path": "假期管理/生育假期",
  "include_children": false,
  "total": 8,
  "documents": [
    {
      "doc_id": "doc_abc123",
      "title": "产假政策",
      "created_at": "2025-11-24T10:00:00Z",
      "quality_score": 0.92
    }
  ]
}
```

**curl示例**:
```bash
# 查询标签下的文档
curl "http://localhost:9601/api/v3/tags/tag_102/documents" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC"

# 包含子标签的文档
curl "http://localhost:9601/api/v3/tags/tag_100/documents?include_children=true" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC"
```

---

### 4.3 任务资源（Jobs & Processings）

**Job是任务系统的一等公民**，代表单个具体的处理任务（如L1提取、L2向量化），具有完整的生命周期（pending → processing → done/failed）。

**Processing是一组相关Jobs的分组标识符**，用于追踪一次用户操作产生的所有任务，其状态从Jobs聚合计算得出。Processing不存储状态，只作为查询和追踪的锚点。

#### 完整端点列表

```
# Processing资源（粗粒度）
POST   /api/v3/processings                    # 创建Processing
GET    /api/v3/processings                    # 查询Processing列表
GET    /api/v3/processings/{processing_id}    # 查询Processing详情
POST   /api/v3/processings/{processing_id}/retry     # 重试失败任务
POST   /api/v3/processings/{processing_id}/cancel    # 取消Processing
GET    /api/v3/processings/{processing_id}/jobs      # 查询Processing的所有Job

# Job资源（细粒度）
GET    /api/v3/jobs                           # 查询Job列表
GET    /api/v3/jobs/{job_id}                  # 查询Job详情
POST   /api/v3/jobs/{job_id}/retry            # 重试单个Job
```

---

#### 4.3.1 POST /api/v3/processings - 创建Processing

**描述**: 创建Processing分组，批量创建文档处理任务。自动生成processing_id用于追踪。

**请求体**:
```json
{
  "doc_ids": ["doc_001", "doc_002"],
  "tasks": ["l1_extract", "l2_vectorize", "l3_knowledge_extract"],
  "metadata": {
    "description": "年度政策文档处理",
    "created_by": "user_123"
  }
}
```

**参数说明**:

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| doc_ids | array | ✅ 是 | 文档ID列表 |
| tasks | array | ✅ 是 | 任务类型列表 |
| metadata | object | ❌ 否 | 可选元数据（创建者、描述等） |

**支持的任务类型**:
- `l1_extract`: L1文档提取
- `l2_vectorize`: L2向量化
- `l3_knowledge_extract`: L3知识提取
- 其他已注册的任务类型

**响应**:
```json
{
  "processing_id": "proc_abc123",
  "job_count": 6,
  "doc_count": 2,
  "created_at": "2025-11-24T10:00:00Z",
  "message": "已创建6个任务（2个文档 × 3个任务类型）"
}
```

**curl示例**:
```bash
# 单文档完整处理
curl -X POST "http://localhost:9601/api/v3/processings" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC" \
  -H "Content-Type: application/json" \
  -d '{
    "doc_ids": ["doc_001"],
    "tasks": ["l1_extract", "l2_vectorize", "l3_knowledge_extract"]
  }'

# 批量处理多个文档
curl -X POST "http://localhost:9601/api/v3/processings" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC" \
  -H "Content-Type: application/json" \
  -d '{
    "doc_ids": ["doc_001", "doc_002", "doc_003"],
    "tasks": ["l1_extract", "l2_vectorize", "l3_knowledge_extract"],
    "metadata": {"description": "批量处理年度政策文档"}
  }'
```

---

#### 4.3.2 GET /api/v3/processings/{processing_id} - 查询Processing状态

**描述**: 查询Processing的详细状态和进度。状态从关联的Jobs聚合计算得出。

**路径参数**:
- `processing_id`: Processing ID

**响应**:
```json
{
  "processing_id": "proc_abc123",
  "status": "running",
  "progress": {
    "total_jobs": 9,
    "completed_jobs": 6,
    "failed_jobs": 1,
    "pending_jobs": 0,
    "processing_jobs": 2,
    "completion_rate": 0.67
  },
  "doc_ids": ["doc_001", "doc_002", "doc_003"],
  "created_at": "2025-11-24T10:00:00Z",
  "metadata": {
    "description": "年度政策文档处理"
  }
}
```

**状态说明**（从Jobs聚合计算）:
- `pending`: 所有Job都是pending
- `running`: 至少有一个Job在processing
- `completed`: 所有Job都是done
- `failed`: 有Job失败且没有正在运行的Job
- `partial`: 部分成功部分失败

---

#### 4.3.3 GET /api/v3/processings - 查询Processing列表

**描述**: 查询Processing列表，支持多种过滤条件。

**查询参数**:

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| status | string | ❌ 否 | 状态 |
| created_by | string | ❌ 否 | 创建者 |
| created_after | string | ❌ 否 | 创建时间（ISO 8601） |
| limit | integer | ❌ 否 | 返回数量（默认100） |
| offset | integer | ❌ 否 | 偏移量（默认0） |

**响应**:
```json
{
  "total": 50,
  "limit": 20,
  "offset": 0,
  "processings": [
    {
      "processing_id": "proc_abc123",
      "status": "completed",
      "progress": {
        "total_jobs": 9,
        "completed_jobs": 9,
        "completion_rate": 1.0
      },
      "doc_ids": ["doc_001", "doc_002", "doc_003"],
      "created_at": "2025-11-24T10:00:00Z"
    }
  ]
}
```

---

#### 4.3.4 GET /api/v3/jobs - 查询Job列表

**描述**: 查询Job列表，支持按文档、任务类型、状态过滤。

**查询参数**:

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| processing_id | string | ❌ 否 | Processing ID |
| doc_id | string | ❌ 否 | 文档ID |
| job_type | string | ❌ 否 | 任务类型 |
| status | string | ❌ 否 | 状态 |
| limit | integer | ❌ 否 | 返回数量（默认100） |
| offset | integer | ❌ 否 | 偏移量（默认0） |

**响应**:
```json
{
  "total": 150,
  "jobs": [
    {
      "job_id": "job_001",
      "job_type": "l1_extract",
      "processing_id": "proc_abc123",
      "target_type": "document",
      "target_ids": ["doc_001"],
      "status": "done",
      "progress": 100,
      "created_at": "2025-11-24T10:00:00Z",
      "completed_at": "2025-11-24T10:00:15Z"
    }
  ]
}
```

**curl示例**:
```bash
# 查询所有失败的Job
curl "http://localhost:9601/api/v3/jobs?status=failed" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC"

# 查询特定文档的所有Job
curl "http://localhost:9601/api/v3/jobs?doc_id=doc_001" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC"
```

---

#### 4.3.5 GET /api/v3/jobs/{job_id} - 查询Job详情

**描述**: 查询单个Job的详细信息。

**路径参数**:
- `job_id`: Job ID

**响应**:
```json
{
  "job_id": "job_001",
  "job_type": "l1_extract",
  "processing_id": "proc_abc123",
  "target_type": "document",
  "target_ids": ["doc_001"],
  "status": "done",
  "progress": 100,
  "priority": 5,
  "current_retry": 0,
  "max_retries": 3,
  "created_at": "2025-11-24T10:00:00Z",
  "started_at": "2025-11-24T10:00:05Z",
  "completed_at": "2025-11-24T10:00:15Z",
  "result": {
    "l1_page_count": 5,
    "l1_extraction_model": "pymupdf"
  }
}
```

---

#### 4.3.6 POST /api/v3/jobs/{job_id}/retry - 重试单个Job

**描述**: 重试失败的Job。

**路径参数**:
- `job_id`: Job ID

**响应**:
```json
{
  "new_job_id": "job_002",
  "original_job_id": "job_001",
  "status": "pending",
  "created_at": "2025-11-24T15:00:00Z"
}
```

---

### 4.4 关系资源（Relations）

> ⚠️ **计划中功能** | **Planned Feature**
>
> 本节描述的Relations API端点和功能目前**尚未实现**，属于v3.0的规划功能。
>
> 预计在后续版本中实现。当前系统使用 `GET /api/v3/documents/{doc_id}/similar` 端点提供基础的文档相似度查询功能。

关系是连接各种实体的纽带，形成知识网络。这是v3.0的**核心规划功能**。

#### 完整端点列表（计划中）

```
GET    /api/v3/relations                  # 查询关系列表
POST   /api/v3/relations                  # 创建关系
GET    /api/v3/relations/{relation_id}    # 查询关系详情
DELETE /api/v3/relations/{relation_id}    # 删除关系
GET    /api/v3/relations/nodes/{node_id}  # 查询节点的所有关系
POST   /api/v3/relations/graph/traverse   # 图遍历
```

---

#### 4.4.1 GET /api/v3/relations - 查询关系列表

**描述**: 查询关系列表，支持按类型、节点过滤。

**查询参数**:

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| relation_type | string | ❌ 否 | 关系类型 |
| source_id | string | ❌ 否 | 源节点ID |
| target_id | string | ❌ 否 | 目标节点ID |
| limit | integer | ❌ 否 | 返回数量（默认100） |
| offset | integer | ❌ 否 | 偏移量（默认0） |

**响应**:
```json
{
  "total": 320,
  "relations": [
    {
      "relation_id": "rel_001",
      "relation_type": "version",
      "source_id": "doc_001",
      "target_id": "doc_002",
      "metadata": {
        "similarity_score": 0.95,
        "changes": "更新了第3章内容"
      },
      "created_at": "2025-11-24T10:00:00Z"
    }
  ]
}
```

**支持的关系类型**:

| 类型 | 说明 | 场景 |
|------|------|------|
| `version` | 版本关系 | doc_v1 → doc_v2 |
| `similar` | 相似关系 | doc_a ↔ doc_b |
| `reference` | 引用关系 | doc_a → doc_b |
| `variant` | 变体关系 | 北京版 ↔ 上海版 |
| `parent_child` | 父子关系 | 总政策 → 细则 |

---

#### 4.4.2 POST /api/v3/relations - 创建关系

**描述**: 创建两个节点之间的关系。

**请求体**:
```json
{
  "relation_type": "version",
  "source_id": "doc_001",
  "target_id": "doc_002",
  "metadata": {
    "similarity_score": 0.95,
    "changes": "更新了第3章内容",
    "impact_level": "high"
  }
}
```

**响应**:
```json
{
  "relation_id": "rel_001",
  "relation_type": "version",
  "source_id": "doc_001",
  "target_id": "doc_002",
  "created_at": "2025-11-24T10:00:00Z"
}
```

**curl示例**:
```bash
curl -X POST "http://localhost:9601/api/v3/relations" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC" \
  -H "Content-Type: application/json" \
  -d '{
    "relation_type": "version",
    "source_id": "doc_001",
    "target_id": "doc_002",
    "metadata": {
      "similarity_score": 0.95
    }
  }'
```

---

#### 4.4.3 GET /api/v3/relations/{relation_id} - 查询关系详情

**描述**: 查询关系的详细信息。

**路径参数**:
- `relation_id`: 关系ID

**响应**:
```json
{
  "relation_id": "rel_001",
  "relation_type": "version",
  "source_id": "doc_001",
  "source_title": "产假政策（2024版）",
  "target_id": "doc_002",
  "target_title": "产假政策（2025版）",
  "metadata": {
    "similarity_score": 0.95,
    "changes": "更新了第3章内容"
  },
  "created_at": "2025-11-24T10:00:00Z"
}
```

---

#### 4.4.4 GET /api/v3/relations/nodes/{node_id} - 查询节点的所有关系

**描述**: 查询节点（文档、标签等）的所有关系。

**路径参数**:
- `node_id`: 节点ID（如doc_001）

**查询参数**:

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| relation_type | string | ❌ 否 | 关系类型 |
| direction | string | ❌ 否 | 方向：in/out/both（默认both） |

**响应**:
```json
{
  "node_id": "doc_001",
  "node_type": "document",
  "node_title": "产假政策（2024版）",
  "total_relations": 5,
  "relations": {
    "out": [
      {
        "relation_id": "rel_001",
        "relation_type": "version",
        "target_id": "doc_002",
        "target_title": "产假政策（2025版）",
        "metadata": {"similarity_score": 0.95}
      }
    ],
    "in": [
      {
        "relation_id": "rel_002",
        "relation_type": "reference",
        "source_id": "doc_003",
        "source_title": "员工手册",
        "metadata": {"section": "第5章"}
      }
    ]
  }
}
```

**curl示例**:
```bash
# 查询所有关系
curl "http://localhost:9601/api/v3/relations/nodes/doc_001" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC"

# 只查询版本关系
curl "http://localhost:9601/api/v3/relations/nodes/doc_001?relation_type=version" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC"

# 只查询出边
curl "http://localhost:9601/api/v3/relations/nodes/doc_001?direction=out" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC"
```

---

#### 4.4.5 POST /api/v3/relations/graph/traverse - 图遍历

**描述**: 从起始节点开始，遍历关系图，返回关系子图。

**请求体**:
```json
{
  "start_node": "doc_001",
  "relation_types": ["version", "similar"],
  "max_depth": 3,
  "direction": "both"
}
```

**响应**:
```json
{
  "start_node": "doc_001",
  "max_depth": 3,
  "nodes": [
    {
      "node_id": "doc_001",
      "node_type": "document",
      "title": "产假政策（2024版）",
      "depth": 0
    },
    {
      "node_id": "doc_002",
      "node_type": "document",
      "title": "产假政策（2025版）",
      "depth": 1
    }
  ],
  "edges": [
    {
      "relation_id": "rel_001",
      "relation_type": "version",
      "source_id": "doc_001",
      "target_id": "doc_002"
    }
  ]
}
```

**使用场景**:
- 查找文档的所有版本历史
- 查找文档的间接相关文档
- 构建知识图谱可视化

**curl示例**:
```bash
curl -X POST "http://localhost:9601/api/v3/relations/graph/traverse" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC" \
  -H "Content-Type: application/json" \
  -d '{
    "start_node": "doc_001",
    "relation_types": ["version", "similar"],
    "max_depth": 3
  }'
```

---

## 5. 搜索功能

搜索功能明确区分两种搜索方式：**文档检索**（基于元数据）和**语义搜索**（基于内容）。

### 5.1 文档检索（Document Search）

#### POST /api/v3/search/documents - 文档检索

**描述**: 基于元数据、标签、属性的结构化查询，精确高效。

**请求体**:
```json
{
  "filters": {
    "tags": {
      "主体": ["北京总部"],
      "业务领域": ["假期管理"],
      "时间维度": ["2025年"]
    },
    "tags_logic": "AND",
    "processing_status": "completed",
    "created_after": "2025-01-01",
    "created_before": "2025-12-31",
    "file_extension": "pdf",
    "file_size_min": 1024,
    "file_size_max": 10485760,
    "quality_score_min": 0.8,
    "keyword": "产假"
  },
  "sort_by": "created_at",
  "order": "desc",
  "limit": 50,
  "offset": 0
}
```

**支持的过滤条件**:

| 过滤条件 | 类型 | 说明 |
|---------|------|------|
| `tags` | object | 标签过滤（多维度） |
| `tags_logic` | string | 标签逻辑：AND/OR |
| `processing_status` | string | 处理状态 |
| `created_after` | string | 创建时间（开始） |
| `created_before` | string | 创建时间（结束） |
| `file_extension` | string | 文件类型 |
| `file_size_min` | integer | 文件大小（最小，字节） |
| `file_size_max` | integer | 文件大小（最大，字节） |
| `quality_score_min` | float | 质量分数（最小） |
| `keyword` | string | 关键词（基于L1全文） |

**响应**:
```json
{
  "total": 12,
  "limit": 50,
  "offset": 0,
  "filters_applied": {
    "tags": {
      "主体": ["北京总部"],
      "业务领域": ["假期管理"],
      "时间维度": ["2025年"]
    },
    "tags_logic": "AND"
  },
  "documents": [
    {
      "doc_id": "doc_abc123",
      "title": "产假政策",
      "file_size": 245678,
      "file_extension": "pdf",
      "processing_status": "completed",
      "quality_score": 0.92,
      "created_at": "2025-11-24T10:00:00Z",
      "tags": {
        "主体": [{"tag_id": "tag_001", "name": "北京总部"}],
        "业务领域": [{"tag_id": "tag_102", "name": "假期管理/生育假期"}]
      },
      "l3_one_sentence": "北京总部员工产假为128天。"
    }
  ],
  "search_time_ms": 45
}
```

**curl示例**:
```bash
# 基础检索
curl -X POST "http://localhost:9601/api/v3/search/documents" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "tags": {
        "主体": ["北京总部"],
        "业务领域": ["假期管理"]
      },
      "tags_logic": "AND",
      "processing_status": "completed"
    },
    "limit": 20
  }'

# 复杂过滤
curl -X POST "http://localhost:9601/api/v3/search/documents" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "tags": {
        "业务领域": ["假期管理", "薪酬福利"]
      },
      "tags_logic": "OR",
      "created_after": "2025-01-01",
      "quality_score_min": 0.8,
      "file_extension": "pdf"
    },
    "sort_by": "quality_score",
    "order": "desc"
  }'
```

**使用场景**:
- ✅ 按标签浏览文档（如：查看所有"北京总部"+"假期管理"的文档）
- ✅ 按时间范围查询（如：查看2025年新增的文档）
- ✅ 按质量筛选（如：只看高质量文档）
- ✅ 按文件属性过滤（如：只看PDF文件，大小<10MB）

---

### 5.2 语义搜索（Semantic Search）

#### POST /api/v3/search/semantic - 语义搜索

**描述**: 基于向量相似度的语义搜索，支持自然语言查询。

**请求体**:
```json
{
  "query": "产假期间社保怎么办？",
  "top_k": 5,
  "strategy": "auto",
  "filters": {
    "tags": {
      "业务领域": ["假期管理", "薪酬福利"]
    },
    "tags_logic": "OR"
  },
  "include_content": false
}
```

**参数说明**:

| 参数 | 类型 | 必需 | 说明 |
|-----|------|------|------|
| query | string | ✅ 是 | 查询文本 |
| top_k | integer | ❌ 否 | 返回数量（默认5，最大50） |
| strategy | string | ❌ 否 | 检索策略：auto/full_document/chunk_retrieval |
| filters | object | ❌ 否 | 过滤条件（支持标签过滤） |
| include_content | boolean | ❌ 否 | 是否包含内容（默认false） |

**响应**:
```json
{
  "query": "产假期间社保怎么办？",
  "total": 3,
  "top_k": 5,
  "results": [
    {
      "doc_id": "doc_abc123",
      "title": "产假期间社保缴纳规定",
      "score": 0.93,
      "strategy": "full_document",
      "content": "产假期间社保由单位正常缴纳，个人部分由单位代缴后从生育津贴中扣除。",
      "tags": {
        "业务领域": [{"tag_id": "tag_102", "name": "假期管理/生育假期"}]
      },
      "l3_one_sentence": "产假期间社保由单位正常缴纳，个人部分由单位代缴后从生育津贴中扣除。"
    },
    {
      "doc_id": "doc_def456",
      "title": "生育保险报销指南",
      "score": 0.88,
      "strategy": "chunk_retrieval",
      "chunks": [
        {
          "chunk_id": "chunk_001",
          "content": "生育保险待遇包括生育医疗费用和生育津贴...",
          "score": 0.90
        }
      ]
    }
  ],
  "search_time_ms": 125
}
```

**curl示例**:
```bash
# 基础语义搜索
curl -X POST "http://localhost:9601/api/v3/search/semantic" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "产假期间社保怎么办？",
    "top_k": 5
  }'

# 带标签过滤的语义搜索
curl -X POST "http://localhost:9601/api/v3/search/semantic" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "产假政策",
    "top_k": 5,
    "filters": {
      "tags": {
        "主体": ["北京总部"],
        "时间维度": ["2025年"]
      },
      "tags_logic": "AND"
    }
  }'
```

**使用场景**:
- ✅ 自然语言问答（如：用户问"产假期间社保怎么办？"）
- ✅ 相似内容推荐（如：找到与当前文档相似的其他文档）
- ✅ 模糊查询（如：用户不知道准确的关键词）

---

### 5.3 文档检索 vs 语义搜索对比

| 维度 | 文档检索 | 语义搜索 |
|------|---------|---------|
| **查询方式** | 结构化过滤（标签、属性） | 自然语言查询 |
| **匹配方式** | 精确匹配 | 语义相似度 |
| **性能** | 快（毫秒级） | 较慢（百毫秒级） |
| **适用场景** | 浏览、筛选、统计 | 问答、推荐、发现 |
| **返回结果** | 符合条件的文档列表 | 相似度排序的文档 |

**组合使用**:
```bash
# 先用文档检索缩小范围（快速）
POST /api/v3/search/documents
{
  "filters": {
    "tags": {"主体": ["北京总部"]},
    "processing_status": "completed"
  }
}
→ 得到100个文档

# 再用语义搜索精准匹配（智能）
POST /api/v3/search/semantic
{
  "query": "产假期间社保",
  "filters": {
    "tags": {"主体": ["北京总部"]}
  }
}
→ 得到最相关的5个文档
```

---

## 6. 统计分析

统计分析提供多维度的数据统计，帮助了解知识库的整体状况。

### 完整端点列表

```
GET /api/v3/stats/overview      # 总览统计
GET /api/v3/stats/documents     # 文档统计
GET /api/v3/stats/tags          # 标签统计
GET /api/v3/stats/processings   # 任务统计
GET /api/v3/stats/quality       # 质量统计
```

---

### 6.1 GET /api/v3/stats/overview - 总览统计

**描述**: 知识库总览统计。

**响应**:
```json
{
  "total_documents": 1250,
  "total_tags": 121,
  "total_processings": 1500,
  "total_relations": 3200,
  "storage_size_gb": 12.5,
  "avg_quality_score": 0.85,
  "last_updated": "2025-11-24T15:00:00Z"
}
```

**curl示例**:
```bash
curl "http://localhost:9601/api/v3/stats/overview" \
  -H "X-API-Key: sk-taxkb-admin-test-TESTADMIN123456789ABC"
```

---

### 6.2 GET /api/v3/stats/documents - 文档统计

**描述**: 文档的多维度统计。

**响应**:
```json
{
  "total": 1250,
  "by_status": {
    "completed": 1150,
    "processing": 50,
    "failed": 50
  },
  "by_file_type": {
    "pdf": 800,
    "docx": 350,
    "xlsx": 100
  },
  "by_tag": {
    "主体": {
      "北京总部": 600,
      "上海分公司": 400,
      "深圳分公司": 250
    },
    "业务领域": {
      "假期管理": 200,
      "薪酬福利": 300,
      "入转调离": 150
    }
  },
  "storage_size_gb": 12.5,
  "avg_file_size_mb": 0.98
}
```

---

### 6.3 GET /api/v3/stats/tags - 标签统计

**描述**: 标签使用情况统计。

**响应**:
```json
{
  "by_dimension": {
    "主体": {
      "total_tags": 15,
      "used_tags": 12,
      "usage_rate": 0.8
    },
    "业务领域": {
      "total_tags": 45,
      "used_tags": 38,
      "usage_rate": 0.84
    }
  },
  "top_tags": [
    {
      "tag_id": "tag_001",
      "name": "北京总部",
      "dimension": "主体",
      "doc_count": 600
    },
    {
      "tag_id": "tag_102",
      "name": "假期管理/生育假期",
      "dimension": "业务领域",
      "doc_count": 200
    }
  ],
  "unused_tags": [
    {
      "tag_id": "tag_999",
      "name": "未使用标签",
      "dimension": "内容标签"
    }
  ]
}
```

---

### 6.4 GET /api/v3/stats/processings - 任务统计

**描述**: 任务执行情况统计。

**响应**:
```json
{
  "total_processings": 1500,
  "by_status": {
    "completed": 1400,
    "failed": 50,
    "running": 30,
    "pending": 20
  },
  "total_jobs": 4500,
  "by_job_type": {
    "l1_extract": 1500,
    "l2_vectorize": 1500,
    "l3_knowledge_extract": 1500
  },
  "by_job_status": {
    "done": 4350,
    "failed": 150
  },
  "success_rate": 0.97,
  "avg_processing_duration_seconds": 45
}
```

---

### 6.5 GET /api/v3/stats/quality - 质量统计

**描述**: 文档质量统计。

**响应**:
```json
{
  "avg_score": 0.85,
  "distribution": {
    "0.9-1.0": 450,
    "0.8-0.9": 500,
    "0.7-0.8": 200,
    "0.0-0.7": 100
  },
  "issues": {
    "missing_required_tags": 50,
    "low_confidence_tags": 100,
    "incomplete_l3": 30
  },
  "top_quality_documents": [
    {
      "doc_id": "doc_abc123",
      "title": "产假政策",
      "quality_score": 0.98
    }
  ],
  "low_quality_documents": [
    {
      "doc_id": "doc_xyz789",
      "title": "某文档",
      "quality_score": 0.45,
      "issues": ["missing_required_tags", "low_confidence_tags"]
    }
  ]
}
```

---

## 7. 完整使用示例

### 7.1 示例1：单文档上传并处理

```bash
#!/bin/bash

API_KEY="sk-taxkb-admin-test-TESTADMIN123456789ABC"
BASE_URL="http://localhost:9601/api/v3"

# 1. 上传文档
echo "1. 上传文档..."
DOC_RESPONSE=$(curl -s -X POST "$BASE_URL/documents" \
  -H "X-API-Key: $API_KEY" \
  -F "file=@产假政策.pdf" \
  -F 'metadata={"title":"产假政策2025","tags":{"主体":["北京总部"]}}')

DOC_ID=$(echo $DOC_RESPONSE | jq -r '.doc_id')
echo "文档已上传: $DOC_ID"

# 2. 创建Processing
echo "2. 创建Processing..."
PROC_RESPONSE=$(curl -s -X POST "$BASE_URL/processings" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"doc_ids\": [\"$DOC_ID\"],
    \"tasks\": [\"l1_extract\", \"l2_vectorize\", \"l3_knowledge_extract\"]
  }")

PROC_ID=$(echo $PROC_RESPONSE | jq -r '.processing_id')
echo "Processing已创建: $PROC_ID"

# 3. 轮询Processing状态
echo "3. 等待处理完成..."
while true; do
  STATUS_RESPONSE=$(curl -s "$BASE_URL/processings/$PROC_ID" \
    -H "X-API-Key: $API_KEY")

  STATUS=$(echo $STATUS_RESPONSE | jq -r '.status')
  PROGRESS=$(echo $STATUS_RESPONSE | jq -r '.progress.completion_rate')

  echo "状态: $STATUS, 进度: $(echo "$PROGRESS * 100" | bc)%"

  if [ "$STATUS" = "completed" ]; then
    echo "处理完成！"
    break
  elif [ "$STATUS" = "failed" ]; then
    echo "处理失败！"
    exit 1
  fi

  sleep 5
done

# 4. 查询文档详情
echo "4. 查询文档详情..."
FINAL_RESULT=$(curl -s "$BASE_URL/documents/$DOC_ID?include=tags,l3" \
  -H "X-API-Key: $API_KEY")

echo "最终结果:"
echo $FINAL_RESULT | jq '{doc_id, title, quality_score, l3_summary}'
```

---

### 7.2 示例2：文档检索 + 语义搜索

```bash
#!/bin/bash

API_KEY="sk-taxkb-admin-test-TESTADMIN123456789ABC"
BASE_URL="http://localhost:9601/api/v3"

# 1. 先用文档检索缩小范围
echo "1. 文档检索（缩小范围）..."
SEARCH_RESPONSE=$(curl -s -X POST "$BASE_URL/search/documents" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "tags": {
        "主体": ["北京总部"],
        "业务领域": ["假期管理"]
      },
      "tags_logic": "AND",
      "processing_status": "completed"
    },
    "limit": 100
  }')

TOTAL=$(echo $SEARCH_RESPONSE | jq '.total')
echo "找到 $TOTAL 个文档"

# 2. 再用语义搜索精准匹配
echo "2. 语义搜索（精准匹配）..."
SEMANTIC_RESPONSE=$(curl -s -X POST "$BASE_URL/search/semantic" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "产假期间社保怎么办？",
    "top_k": 5,
    "filters": {
      "tags": {
        "主体": ["北京总部"],
        "业务领域": ["假期管理"]
      }
    }
  }')

echo "语义搜索结果:"
echo $SEMANTIC_RESPONSE | jq '.results[] | {title, score, l3_one_sentence}'
```

---

### 7.3 示例3：关系管理和图遍历

```bash
#!/bin/bash

API_KEY="sk-taxkb-admin-test-TESTADMIN123456789ABC"
BASE_URL="http://localhost:9601/api/v3"

# 1. 创建版本关系
echo "1. 创建版本关系..."
RELATION_RESPONSE=$(curl -s -X POST "$BASE_URL/relations" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "relation_type": "version",
    "source_id": "doc_001",
    "target_id": "doc_002",
    "metadata": {
      "similarity_score": 0.95,
      "changes": "更新了第3章内容"
    }
  }')

RELATION_ID=$(echo $RELATION_RESPONSE | jq -r '.relation_id')
echo "关系已创建: $RELATION_ID"

# 2. 查询节点的所有关系
echo "2. 查询文档的所有关系..."
NODE_RELATIONS=$(curl -s "$BASE_URL/relations/nodes/doc_001" \
  -H "X-API-Key: $API_KEY")

echo "文档关系:"
echo $NODE_RELATIONS | jq '.relations'

# 3. 图遍历（查找所有版本历史）
echo "3. 图遍历（版本历史）..."
GRAPH_RESPONSE=$(curl -s -X POST "$BASE_URL/relations/graph/traverse" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "start_node": "doc_001",
    "relation_types": ["version"],
    "max_depth": 5
  }')

echo "版本历史图:"
echo $GRAPH_RESPONSE | jq '{nodes: .nodes | length, edges: .edges | length}'
```

---

## 8. 错误处理

### 8.1 错误响应格式

```json
{
  "detail": "错误描述信息"
}
```

或（详细错误）:
```json
{
  "detail": {
    "error": "错误类型",
    "message": "错误描述",
    "field": "出错字段"
  }
}
```

### 8.2 常见错误

#### 1. API Key缺失（401）

```json
{
  "detail": "Missing API Key. Please provide 'X-API-Key' header."
}
```

**解决**: 添加 `X-API-Key` header。

---

#### 2. 资源不存在（404）

```json
{
  "detail": "文档不存在: doc_xyz"
}
```

**解决**: 检查资源ID是否正确。

---

#### 3. 标签约束违反（422）

```json
{
  "detail": "维度'主体'只能选择一个标签，当前选择了2个"
}
```

**解决**: 检查标签体系的基数约束。

---

## 9. 从v2.1迁移指南

### 9.1 核心变更对照

| v2.1 | v3.0 | 变更说明 |
|------|------|---------|
| `POST /documents` | `POST /documents` + `POST /processings` | 职责分离 |
| `POST /documents/search` | `POST /search/documents` | 端点重组 |
| `POST /search/semantic` | `POST /search/semantic` | 保持不变 |
| 无 | `GET /relations/...` | 新增关系管理 |
| 无 | `GET /stats/...` | 新增统计分析 |

### 9.2 迁移步骤

#### 步骤1：更新上传逻辑

```python
# v2.1（旧代码）
response = requests.post(
    "http://localhost:9601/api/v2/documents",
    headers={"X-API-Key": api_key},
    files={"file": open("test.pdf", "rb")}
)
# 自动创建processing

# v3.0（新代码）
# 1. 上传
doc_response = requests.post(
    "http://localhost:9601/api/v3/documents",
    headers={"X-API-Key": api_key},
    files={"file": open("test.pdf", "rb")}
)
doc_id = doc_response.json()["doc_id"]

# 2. 创建Processing
proc_response = requests.post(
    "http://localhost:9601/api/v3/processings",
    headers={"X-API-Key": api_key},
    json={
        "doc_ids": [doc_id],
        "tasks": ["l1_extract", "l2_vectorize", "l3_knowledge_extract"]
    }
)
```

#### 步骤2：更新搜索逻辑

```python
# v2.1（模糊）
response = requests.post(
    "http://localhost:9601/api/v2/documents/search",
    ...
)

# v3.0（明确区分）
# 文档检索
doc_search = requests.post(
    "http://localhost:9601/api/v3/search/documents",
    json={"filters": {...}}
)

# 语义搜索
semantic_search = requests.post(
    "http://localhost:9601/api/v3/search/semantic",
    json={"query": "产假政策"}
)
```

#### 步骤3：利用新功能

```python
# 关系管理
relations = requests.get(
    f"http://localhost:9601/api/v3/relations/nodes/{doc_id}",
    headers={"X-API-Key": api_key}
)

# 统计分析
stats = requests.get(
    "http://localhost:9601/api/v3/stats/overview",
    headers={"X-API-Key": api_key}
)
```

---

## 10. 附录

### 10.1 API端点完整列表

#### 文档资源（Documents）
```
POST   /api/v3/documents
GET    /api/v3/documents/{doc_id}
PATCH  /api/v3/documents/{doc_id}
DELETE /api/v3/documents/{doc_id}
PATCH  /api/v3/documents/{doc_id}/tags
GET    /api/v3/documents/{doc_id}/content
```

#### 标签资源（Tags）
```
GET    /api/v3/tags
POST   /api/v3/tags
GET    /api/v3/tags/{tag_id}
PATCH  /api/v3/tags/{tag_id}
DELETE /api/v3/tags/{tag_id}
GET    /api/v3/tags/{tag_id}/documents
```

#### 任务资源（Processings & Jobs）
```
POST   /api/v3/processings
GET    /api/v3/processings
GET    /api/v3/processings/{processing_id}
POST   /api/v3/processings/{processing_id}/retry
POST   /api/v3/processings/{processing_id}/cancel
GET    /api/v3/processings/{processing_id}/jobs

GET    /api/v3/jobs
GET    /api/v3/jobs/{job_id}
POST   /api/v3/jobs/{job_id}/retry
```

#### 关系资源（Relations）
```
GET    /api/v3/relations
POST   /api/v3/relations
GET    /api/v3/relations/{relation_id}
DELETE /api/v3/relations/{relation_id}
GET    /api/v3/relations/nodes/{node_id}
POST   /api/v3/relations/graph/traverse
```

#### 搜索功能（Search）
```
POST   /api/v3/search/documents
POST   /api/v3/search/semantic
```

#### 统计分析（Stats）
```
GET    /api/v3/stats/overview
GET    /api/v3/stats/documents
GET    /api/v3/stats/tags
GET    /api/v3/stats/processings
GET    /api/v3/stats/quality
```

### 10.2 四大核心要素总结

| 核心要素 | 端点前缀 | 主要操作 |
|---------|---------|---------|
| **文档** | `/documents` | CRUD、标签管理、内容查询 |
| **标签** | `/tags` | CRUD、文档关联查询 |
| **任务** | `/jobs`（核心）, `/processings`（分组） | Job创建/查询/重试，Processing追踪进度 |
| **关系** | `/relations` | CRUD、节点查询、图遍历 |

### 10.3 配额和限制

| 项目 | 限制 |
|-----|------|
| 单文件大小 | 50MB |
| 单次Processing最大targets | 1000个 |
| 单次Processing最大tasks | 10个 |
| 文档检索最大limit | 100 |
| 语义搜索最大top_k | 50 |
| 图遍历最大深度 | 10 |
| API调用速率 | 60次/分钟 |

---

## 联系方式

**技术支持**: taxkb-support@example.com
**GitHub**: https://github.com/your-org/taxkb
**文档反馈**: 请提交Issue到GitHub仓库

---

**最后更新**: 2025-11-24
**维护者**: TaxKB Team
