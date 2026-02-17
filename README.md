# Bot Project - Stdio Wrapper

本项目旨在将命令行工具（如 `qwen-cli`）封装为现代化的 Web 聊天界面。

## 项目结构
- `bot-py/`: Python 后端 (uv 管理)
- `bot-ts/`: TypeScript/Bun 后端 & 前端 (bun 管理)

## 快速开始
目前项目处于需求讨论和规划阶段。详见 `docs/plans/stdio-wrapper.md`。


## 参考

以[geminicli](https://geminicli.com)为例:
- [context7](https://context7.com/websites/geminicli)
- [deepwiki](https://deepwiki.com/google-gemini/gemini-cli)

## bot-ref

下载同步: git clone依赖的原始项目
预处理：利用 Repomix 等工具将仓库“脱水”，剔除干扰，保留骨架。
符号化：利用 tree-sitter 等工具生成精确的符号表，作为 AI 的导航地图。
动态注入：不追求一次性处理所有代码，而是通过 LLM 编排，根据场景动态加载相关的代码片段。
标准化导航：在库中引入类似 llms.txt 的 AI 友好型说明文件，作为知识库的“高速缓存”。