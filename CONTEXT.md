# 项目：Stdio Wrapper Bot (ACP 集成)

## 概述
本项目正在为 `qwen`/`geminicli`等编码代理开发一个现代化的 Web UI，具有并行的 Python 和 TypeScript 后端以进行性能评估。我们目前正在集成 **Agent Client Protocol (ACP)** 以标准化所有通信。


- **范围**: 实验性原型，单用户，无账号与持久化。
- **参照物**: [JetBrains IDEs acp implements](https://blog.jetbrains.com/ai/2025/12/bring-your-own-ai-agent-to-jetbrains-ides/  )
- **技术选型**: 前端单页；后端将提供两套等价实现：Python 与 TypeScript/Bun；两者遵循相同协议与接口；前端与后端通过 WebSocket 进行通信以支持流式更新。

## 核心技术
- **Python 后端 (`bot-py`)**: FastAPI, `asyncio.subprocess`, `uv`。
- **TypeScript 后端 (`bot-ts`)**: Bun, `Elysia`, `Bun.spawn`。
- **前端**: React (后端共享)。
- **协议**: Agent Client Protocol (ACP) - JSON-RPC 2.0。

## Qwen CLI 参考 (qwen)
- **交互式**: `-i, --prompt-interactive`
- **格式**: `--input-format [text|stream-json]`, `-o, --output-format [text|json|stream-json]`
- **流式**: `--include-partial-messages` (对实时 UI 至关重要)。

## ACP 参考
- **本地源码**: [agent-client-protocol](.bot/cache/ref/github.com/agentclientprotocol/agent-client-protocol )
- **目标**: 在两个后端中实现 ACP 代理。

## 开发任务与状态
1. **研究**:
   - [x] 分析 ACP 协议。
   - [x] 验证 `qwen --acp` 初始化与输出结构。
     - 协议版本: 1 (JSON-RPC 2.0)
     - 必需能力: `clientCapabilities.fs` 需包含 `readTextFile`, `writeTextFile` 等。
     - 支持模式: `plan`, `default`, `auto-edit`, `yolo`。
2. **后端**:
   - [ ] `bot-py`: FastAPI + SSE + ACP 实现。
   - [ ] `bot-ts`: Bun + WebSocket + ACP 实现。
3. **前端**:
   - [ ] 具有后端切换功能的 React UI，以便进行比较。

## 指南
- 严格遵守 ACP 标准。
- 保持 Python 和 TypeScript 之间的功能对等。
- 优先使用 `stream-json` 而不是原始文本，以避免 ANSI 转义字符问题。
