import sys

class LogType:
    INFO = "info"
    ERROR = "error"
    SUCCESS = "success"
    WARNING = "warning"
    INDICATION = "indication"

colors = {
    LogType.INFO: "\033[94m",
    LogType.ERROR: "\033[91m",
    LogType.SUCCESS: "\033[92m",
    LogType.WARNING: "\033[93m",
    LogType.INDICATION: "\033[90m",
    
    "end": "\033[0m"
}


def logger(msg, type = LogType.INFO):
    if type == LogType.INDICATION:
        print(f"{colors[type]}{msg}{colors['end']}")
    else:
        print(f"{colors[type]}[{type.upper()}] {msg}{colors['end']}")

class ProgressBar:
    def __init__(self, max: int, width: int = 50):
        self.max = max
        self.width = width
        self.progress = 0
        self.display()

    def display(self):
        progress = int(self.progress * self.width / self.max)
        print(f"{colors[LogType.INDICATION]}\r[{'=' * progress}{' ' * (self.width - progress)}] {self.progress}/{self.max}{colors['end']}", end="")
        sys.stdout.flush()

    def update(self, progress: int):
        self.progress = progress
        self.display()
    
    def next(self):
        self.update(self.progress + 1)
    
    def finish(self):
        print()
        sys.stdout.flush()