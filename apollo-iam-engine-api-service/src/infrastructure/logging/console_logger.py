from rich.console import Console
from rich.theme import Theme
from datetime import datetime

_theme = Theme({
    "info":    "bold cyan",
    "success": "bold green",
    "warning": "bold yellow",
    "error":   "bold red",
    "debug":   "dim white",
})

console = Console(theme=_theme)


def log(level: str, message: str, emoji: str = "📋"):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    style = level.lower()
    console.print(f"[{style}]{emoji} [{ts}] [{level.upper()}] {message}[/{style}]")


def info(msg: str):    log("info",    msg, "ℹ️ ")
def success(msg: str): log("success", msg, "✅")
def warning(msg: str): log("warning", msg, "⚠️ ")
def error(msg: str):   log("error",   msg, "❌")
def debug(msg: str):   log("debug",   msg, "🔍")
