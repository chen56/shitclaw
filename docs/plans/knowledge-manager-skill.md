# AI 知识库管理系统 (Knowledge Manager) 设计方案

## 1. 目标
解决 AI 在编码过程中因“预训练知识过时”或“幻觉”导致的问题。通过建立一个可管理的、版本化的本地知识依赖库，为 Agent 提供确定性的参考依据。

## 2. 核心组件

### 2.1 依赖描述文件 (`.bot/ref.lock.json`)
作为项目的“知识 Source of Truth”，记录所有外部知识源的确定性版本。
```json
{
  "refs": [
    {
      "id": "acp-spec",
      "name": "agent-client-protocol",
      "url": "https://github.com/agentclientprotocol/agent-client-protocol.git",
      "version": "main",
      "commit": "optional-last-synced-commit-hash",
      "path": ".bot/cache/ref/github.com/agentclientprotocol/agent-client-protocol",
      "auto_index": true
    }
  ]
}
```

### 2.2 同步工具 (`bot sync`)
实现类似 `uv sync` 的逻辑：
1. 读取 `ref.lock.json`。
2. 检查本地缓存目录。
3. 执行 `git clone --depth 1` 或 `git pull`。
4. 如果是 `main` 分支且有更新，触发重新索引。

### 2.3 分层索引机制 (`Layered Indexing`)
对仓库内容进行渐进式摘要，存放在 `.bot/index/`：

- **Layer 1 (Global Overview)**: 项目定位、核心概念、顶层目录结构。
- **Layer 2 (Feature/Module Maps)**: 关键 API 定义、协议方法列表、核心模型结构（如 `PromptRequest`）。
- **Layer 2 (Examples & Patterns)**: 典型用法示例、最佳实践代码片段。
- **Layer 3 (source)**: 原始仓库引用。


## 3. 工作流集成

### 3.1 预处理阶段 (Knowledge Lookup)
在执行任何重大开发任务（如实现 ACP 后端）之前，Agent 必须执行：
1. **识别需求**: 需要哪些协议或库的知识？
2. **检索索引**: 查看 `.bot/index/` 是否有相关记录。
3. **精准阅读**: 根据 Layer 2 索引定位到具体的 `src/*.rs` 或 `docs/*.md` 进行深度解析。

### 3.2 冲突处理
如果 Agent 预训练知识与本地 Ref 库冲突，**以本地 Ref 库为准**。

## 4. 实施计划 (Skill: `ref-manager`)

### 第一阶段：自动化同步
开发 `ref_sync` 工具，支持从 GitHub 拉取并验证版本。

### 第二阶段：结构化扫描
开发扫描器，利用大模型的能力对下载的仓库进行“初次阅读”，生成 L1 和 L2 级别的 Markdown 索引。

### 第三阶段：动态上下文注入
在 Agent 的思考链路中增加一个“知识检索步”，强制其在回答前“看一眼文档”。
