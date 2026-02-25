# Stdio 封装项目：从 CLI 到 Web UI (并行实验)

## 项目目标
开发一个 Web 工具，将 `qwen` (Qwen Code) 封装为现代化的聊天界面。本项目将分别使用 **Python** 和 **TypeScript/Bun** 实现两套完全相同功能的后端，用于对比评估。

## 调研结论 (qwen 核心参数)
- **命令**: `qwen`
- **交互模式**: 
    - `-i, --prompt-interactive`: 执行初始 prompt 并保持交互模式（适合长对话）。
    - `query`: 直接传 query 进入默认模式。
- **输入输出格式**:
    - `--input-format [text|stream-json]`: 默认为 text。
    - `-o, --output-format [text|json|stream-json]`: 极大利好流式解析。
    - `--include-partial-messages`: 在使用 `stream-json` 时包含部分消息，适合极致流式体验。

## 并行方案对比设计

### 方案 A: bot-py (Python)
- **核心技术**: Python 3.12+, `uv`, `FastAPI`, `asyncio.subprocess`。
- **实验重点**: 使用 Python 的异步流处理 `stream-json` 输出并实时转发。

### 方案 B: bot-ts (TypeScript/Bun)
- **核心技术**: `Bun`, `Elysia`, `Bun.spawn`。
- **实验重点**: 利用 Bun 极简的 `ReadableStream` 适配和 WebSocket 处理。

## 核心任务清单 (TODO)

### 1. 技术预研
- [ ] **手动验证**：运行 `qwen -o stream-json "hello"` 观察其 JSON 流的结构。
- [ ] **交互验证**：测试在非 TTY 环境下持续写入 stdin 是否能被 `qwen` 正常处理。

### 2. bot-py 实现路径
- [ ] 初始化 FastAPI 项目。
- [ ] 封装 `asyncio.create_subprocess_exec`。
- [ ] 实现 SSE 接口转发 `stream-json` 数据。

### 3. bot-ts 实现路径
- [ ] 初始化 Bun 项目。
- [ ] 使用 `Bun.spawn` 的 `stdout` 直接对接 Web Response。
- [ ] 实现 WebSocket 版本的实时交互。

### 4. 前端开发 (共用)
- [ ] 编写 React 聊天 UI。
- [ ] 增加 "后端切换" 功能，方便在页面上直接对比 Python/TS 的响应速度。

### 5. 对比总结
- [ ] 记录开发过程中的坑（如 JSON 流的断句、缓冲区刷新）。
- [ ] 对比两者的延迟、内存占用。

## 技术要点备忘
- `qwen` 可能包含复杂的 ANSI 转义字符，若使用 `text` 格式需过滤，推荐优先使用 `stream-json`。
- 需处理子进程的自动重启和超时。
