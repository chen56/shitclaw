# nbcode

## 项目目标
利用现有ai code工具, 实现ai native代码开发闭环流程, 从定义任务>执行>反馈, 循环往复, 任务流转依赖github project或聊天软件完成。

## 规范
- 每次对话都重新加载`AGENTS.md`
- 对话、文档、代码注释都是中文
- git/github 相关操作先阅读 `.agents/github.md`。 
- 遇到不合理的结果，应认真调查是否和猜测相符，再给出合理的解释。
- 每次对话的最后列出当前加载的上下文、skill文件路径