import shutil
from cyclopts import App

app = App(name="nbcode", help="nbcode: AI Native Code Lab CLI")
# 支持探测的 agent 可执行文件名
supported_agents = [
    "gemini",
    "qwen",
    "codex",
    "codebuddy",
    "kimi",
]

@app.command
def agents():
    """列出当前机器上可识别的 AI agent。"""
    print(f"{'STATUS':<8} {'AGENT':<15} {'PATH'}")
    print("-" * 60)
    
    for binary in supported_agents:
        path = shutil.which(binary)
        status = "✅" if path else "❌"
        display_path = path if path else "-"
        print(f"{status:<7} {binary:<15} {display_path}")

def __main__():
    app()

if __name__ == "__main__":
    __main__()
