# Skill Factory - 智能Skill生成器

## 📖 概述

`skill_factory` 是一个强大的Skill生成系统，通过结构化的对话流程引导用户定义需求，自动生成符合Claude Agent Skills规范的完整技能包。无论是初学者还是经验丰富的开发者，都能快速创建高质量、标准化的Skill。

## 🚀 快速开始

### 安装和启用

`skill_factory` 是Claude Agent Skill，无需额外安装。确保Skill目录正确放置在：
```
.claude/skills/skill_factory/
```

### 基本使用方法

#### 方式1：明确请求创建Skill
```
请帮我创建一个新的Skill
或者
使用skill_factory创建数据处理Skill
```

#### 方式2：自动识别创建需求
当检测到以下情况时，`skill_factory` 会自动建议创建新Skill：
- 用户重复执行相似复杂操作
- 现有Skill组合无法高效解决问题
- 用户表达"希望自动化"某类任务

## 🎯 核心功能

### 智能需求收集
通过结构化对话收集Skill需求：
1. **基本信息**：Skill名称、功能描述、目标用户
2. **功能细节**：根据Skill类型针对性询问
3. **技术需求**：确认脚本、模板、参考文档需求

### 自动化内容生成
基于收集的需求自动生成：
- ✅ 符合规范的SKILL.md文件
- ✅ 用户友好的README.md说明
- ✅ 高质量的Python脚本
- ✅ 标准化的模板文件
- ✅ 详细的使用示例

### 质量保证体系
三层质量验证：
1. **结构验证**：文件结构和命名规范
2. **内容验证**：逻辑完整性和准确性
3. **功能验证**：脚本可执行性和安全性

## 📁 项目结构

```
.claude/skills/skill_factory/
├── SKILL.md                              # 主技能文件
├── README.md                             # 本使用说明
├── REFERENCE_DEVELOPMENT.md              # 开发规范参考
├── REFERENCE_API_BEST_PRACTICES.md       # API集成指南
├── REFERENCE_TROUBLESHOOTING.md          # 问题排查指南
├── EXAMPLES.md                           # 完整使用示例
├── scripts/                              # Python脚本目录
│   ├── skill_validator.py                # 结构验证脚本
│   ├── template_generator.py             # 模板生成器
│   ├── dependency_checker.py             # 依赖检查器
│   └── structure_builder.py              # 目录构建器
├── templates/                            # 标准模板库
│   ├── data_processor/SKILL.md           # 数据处理模板
│   ├── api_integrator/SKILL.md           # API集成模板
│   ├── document_generator/SKILL.md       # 文档生成模板
│   ├── file_operator/SKILL.md            # 文件操作模板
│   └── content_creator/SKILL.md          # 内容创作模板
├── examples/                             # 示例Skill库
│   ├── excel_data_processor/             # Excel处理示例
│   ├── weather_api_integrator/           # API集成示例
│   └── weekly_report_generator/          # 报告生成示例
└── utils/                                # 工具函数
    ├── __init__.py
    ├── file_helpers.py                   # 文件操作工具
    └── validation_rules.py               # 验证规则库
```

## 🔧 工具脚本使用

### 1. Skill结构验证器
```bash
# 验证Skill结构是否符合规范
python scripts/skill_validator.py path/to/your_skill

# 输出示例：
✅ Skill验证通过！
❌ 发现错误: 缺失SKILL.md文件
```

### 2. 模板生成器
```bash
# 基于需求生成合适的模板
python scripts/template_generator.py

# 根据Skill类型和复杂度自动选择最佳模板
```

### 3. 依赖检查器
```bash
# 检查Python脚本的依赖库可用性
python scripts/dependency_checker.py path/to/your_skill

# 输出示例：
✅ 所有依赖都可用！
❌ 缺失依赖: requests, pandas
```

### 4. 结构构建器
```bash
# 自动创建标准的Skill目录结构
python scripts/structure_builder.py

# 根据模板生成完整的文件结构
```

## 🎪 使用示例

### 创建数据处理Skill
```
用户：请帮我创建一个处理Excel数据的Skill

Skill Factory交互流程：
1. 询问Skill名称和功能描述
2. 确认数据处理的具体需求
3. 选择技术配置选项
4. 自动生成完整的Skill包

生成结果：excel_data_processor Skill包
```

### 创建API集成Skill
```
用户：需要集成天气预报API

Skill Factory交互流程：
1. 确认API端点和认证方式
2. 设置缓存和限流策略
3. 配置错误处理机制
4. 生成专业的API集成Skill

生成结果：weather_api_integrator Skill包
```

## 📚 参考文档

### 开发规范参考 (`REFERENCE_DEVELOPMENT.md`)
- 详细的Skill开发规范
- 文件结构和命名要求
- 代码安全和性能最佳实践
- 测试和质量保证指南

### API集成最佳实践 (`REFERENCE_API_BEST_PRACTICES.md`)
- API客户端架构设计
- 认证和授权实现
- 错误处理和重试机制
- 性能优化和缓存策略

### 问题排查指南 (`REFERENCE_TROUBLESHOOTING.md`)
- 常见问题分类和解决方案
- 调试工具和使用方法
- 紧急处理步骤
- 预防措施和监控策略

## 🔄 高级功能

### 模板库管理
- **标准模板**：5种预设模板类型
- **自定义模板**：支持用户保存个性化模板
- **模板推荐**：基于使用历史智能推荐

### 版本控制
- 记录Skill生成历史
- 支持版本回滚和比较
- 模板版本管理

### 批量生成
- 基于模板批量创建相似Skill
- 配置参数化生成
- 质量批量验证

## 🐛 故障排除

### 常见问题

**Q: Skill创建失败，提示结构验证错误**
A: 使用 `skill_validator.py` 检查具体错误，修复文件结构问题

**Q: 生成的脚本无法执行**
A: 使用 `dependency_checker.py` 检查依赖库，安装缺失的包

**Q: API调用失败**
A: 检查网络连接、认证信息和API端点可用性

**Q: 性能问题，响应缓慢**
A: 参考性能优化指南，实现缓存和限流机制

### 调试工具

#### 详细日志
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### 性能分析
```python
from utils.performance import profile_function

@profile_function
def slow_function():
    # 你的代码
    pass
```

## 🔧 自定义和扩展

### 添加新的模板类型
1. 在 `templates/` 目录下创建新模板
2. 更新 `template_generator.py` 中的模板映射
3. 添加相应的示例和文档

### 扩展工具函数
1. 在 `utils/` 目录下添加新工具
2. 更新 `__init__.py` 导入
3. 编写相应的测试用例

### 自定义验证规则
1. 修改 `utils/validation_rules.py`
2. 更新验证脚本逻辑
3. 测试新的验证规则

## 📞 技术支持

### 获取帮助
如果遇到问题，请：
1. 首先查看相应的参考文档
2. 使用内置的调试工具
3. 检查错误日志和堆栈信息

### 问题上报
当需要外部帮助时，请提供：
- 详细的错误描述
- 重现步骤
- 环境信息
- 已尝试的解决方案

### 贡献指南
欢迎贡献改进：
- 提交问题报告
- 提出功能建议
- 贡献代码改进

## 📄 许可证和版权

本项目遵循开源许可证。具体许可证信息请查看LICENSE文件。

---

**Skill Factory - 让Skill创建变得简单、标准、高效！** 🚀

如有任何问题或建议，请通过适当渠道联系我们。