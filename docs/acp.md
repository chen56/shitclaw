# Agent Client Protocol (ACP) 调查报告

## 1. 协议概述
Agent Client Protocol (ACP) 是一种基于 **JSON-RPC 2.0** 的通信协议，旨在标准化客户端（如 IDE、Web UI）与 AI 代理（Agent）之间的交互。

- **传输层**: 通常通过标准输入/输出 (stdio) 或 WebSocket 进行。
- **消息格式**: 严格遵循 JSON-RPC 2.0 规范。

## 2. Qwen CLI (qwen) 的 ACP 实现
`qwen` 原生支持 ACP 模式，可通过 `--acp` 参数启动。

## 3. 运行模式与交互机制
启动后，`qwen` 作为一个长驻进程，通过标准 IO 进行双工通信。后端需维护该子进程的生命周期。

## 4. 实战演示：手工交互流程记录

### 第一步：握手 (Initialize)
**命令：**
```bash
printf '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": 1, "clientCapabilities": {"fs": {"readTextFile": true, "writeTextFile": true}}, "clientInfo": {"name": "test", "version": "1.0"}}}\n{"jsonrpc": "2.0", "method": "initialized", "params": {}}\n' | qwen --acp
```

### 第二步：创建会话 (session/new)
**发送：**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "session/new",
  "params": {
    "cwd": "/absolute/path/to/project",
    "mcpServers": []
  }
}
```

**真实响应示例 (Result):**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "sessionId": "094557ea-5c1e-48ba-bc72-d17e8fe8ab91",
    "models": {
      "currentModelId": "coder-model(qwen-oauth)",
      "availableModels": [...]
    }
  }
}
```

**伴随通知 (Notification):**
代理会立即推送可用命令（`available_commands_update`）。

### 第三步：对话交互 (session/prompt)
**发送：**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "session/prompt",
  "params": {
    "sessionId": "094557ea-5c1e-48ba-bc72-d17e8fe8ab91",
    "prompt": [
      { "type": "text", "text": "Hi" }
    ]
  }
}
```

**预期流式通知：**
会连续收到多次 `agent_message_chunk` 类型的 `session/update` 通知，最后收到 `stopReason: "end_turn"` 的 Response。

## 5. 核心消息参考表
详见：[ACP 协议技术规范](./acp-protocol-spec.md)
