# ACP 协议技术规范 (基于 2024-11-05 版本)

本规范详细描述了客户端（Web UI 后端）与 ACP 代理（如 `qwen --acp`）交互时所需的 JSON-RPC 消息结构。

## 1. 基础消息外壳
所有消息必须遵循 JSON-RPC 2.0 规范。

### 请求 (Request)
```json
{
  "jsonrpc": "2.0",
  "id": "unique-id",
  "method": "method-name",
  "params": { ... }
}
```

### 响应 (Response)
```json
{
  "jsonrpc": "2.0",
  "id": "unique-id",
  "result": { ... }
}
```

### 通知 (Notification)
```json
{
  "jsonrpc": "2.0",
  "method": "method-name",
  "params": { ... }
}
```

---

## 2. 核心方法定义

### 2.1 `initialize` (Request)
建立连接后的第一条消息。
- **Params**:
  - `protocolVersion`: `1` (数字)
  - `clientCapabilities`: 必须包含 `fs`。
  - `clientInfo`: `{ "name": "...", "version": "..." }`

### 2.2 `session/new` (Request)
创建一个新的会话。
- **Params**: `{}`
- **Result**: `{ "sessionId": "string" }`

### 2.3 `session/prompt` (Request)
发送用户输入。
- **Params**:
  - `sessionId`: `string`
  - `prompt`: `ContentBlock[]`
- **Result**: `PromptResponse`
  - `stopReason`: `end_turn | max_tokens | max_turn_requests | refusal | cancelled`

### 2.4 `session/update` (Notification)
由代理发送，用于流式返回 AI 的回复。
- **Params**:
  - `sessionId`: `string`
  - `update`: `SessionUpdate`
    - `sessionUpdate`: `"agent_message_chunk" | "agent_thought_chunk" | "tool_call" | ...`
    - `content`: `ContentBlock` (当类型为 chunk 时)

---

## 3. 内容块 (ContentBlock) 结构
在 `prompt` 和 `update` 中通用。

### 文本块 (Text)
```json
{
  "type": "text",
  "text": "内容字符串"
}
```

### 资源链接 (ResourceLink)
```json
{
  "type": "resource_link",
  "uri": "file:///path/to/file"
}
```

---

## 4. 典型交互时序图

1.  **Client** -> `initialize` (Request)
2.  **Agent** -> `initialize` (Response)
3.  **Client** -> `initialized` (Notification)
4.  **Client** -> `session/new` (Request)
5.  **Agent** -> `session/new` (Response: `sessionId: "s1"`)
6.  **Client** -> `session/prompt` (Request: `sessionId: "s1"`, `prompt: "Hello"`)
7.  **Agent** -> `session/update` (Notification: `chunk: "H"`)
8.  **Agent** -> `session/update` (Notification: `chunk: "i"`)
9.  **Agent** -> `session/prompt` (Response: `stopReason: "end_turn"`)
