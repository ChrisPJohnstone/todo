from atexit import register
from pathlib import Path
from signal import SIGTERM
from sys import exit, stderr, stdin, stdout
from time import sleep
from typing import Final
from logging import DEBUG, log
import os

from .notification import NotificationService


class DaemonService:
    DEFAULT_PIDFILE: Final[Path] = Path("/tmp/todo/todo.pid")

    def __init__(self, pidfile: Path = DEFAULT_PIDFILE) -> None:
        self.pidfile = pidfile

    @property
    def pidfile(self) -> Path:
        """Path to the pidfile."""
        return self._pidfile

    @pidfile.setter
    def pidfile(self, value: Path) -> None:
        value.parent.mkdir(parents=True, exist_ok=True)
        self._pidfile: Path = value

    @property
    def pidfile_exists(self) -> bool:
        """Boolean indicating if the pidfile exists."""
        return self.pidfile.exists()

    @property
    def notifier(self) -> NotificationService:
        return self._notifier

    @notifier.setter
    def notifier(self, value: NotificationService) -> None:
        self._notifier: NotificationService = value

    def delete_pidfile(self) -> None:
        """Deleted pidfile"""
        self.pidfile.unlink()

    def pid_from_pidfile(self) -> int:
        """Return the pid from pidfile."""
        if not self.pidfile_exists:
            raise FileNotFoundError(f"pidfile {self.pidfile} does not exist.")
        pid: str | None = self.pidfile.read_text().strip()
        if not pid:
            raise ValueError(f"pidfile {self.pidfile} is empty.")
        return int(pid)

    def kill_pid(self, pid: int | None = None) -> None:
        _pid: int = pid if isinstance(pid, int) else self.pid_from_pidfile()
        try:
            while 1:
                os.kill(_pid, SIGTERM)
                sleep(0.1)
        except OSError as error:
            error_str: str = str(error.args)
            if error_str.find("No such process") > 0:
                if self.pidfile_exists:
                    self.delete_pidfile()
            else:
                print(error_str)
                exit(1)

    def _start_fork(self) -> int:
        pid: int = os.fork()
        if pid > 0:
            exit(0)
        return pid

    def daemonize(self) -> None:
        """Deamonize class. UNIX double fork mechanism."""
        # First Fork
        pid: int = self._start_fork()

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # Second Fork
        pid: int = self._start_fork()

        # redirect standard file descriptors
        stdout.flush()
        stderr.flush()
        si = open(os.devnull, "r")
        so = open(os.devnull, "a+")
        se = open(os.devnull, "a+")

        os.dup2(si.fileno(), stdin.fileno())
        os.dup2(so.fileno(), stdout.fileno())
        os.dup2(se.fileno(), stderr.fileno())

        # write pidfile
        register(self.delete_pidfile)
        self.pidfile.write_text(f"{os.getpid()}\n")

    def start(self) -> None:
        """Start the daemon."""
        try:
            self.kill_pid(self.pid_from_pidfile())
        except (FileNotFoundError, ValueError):
            pass
        self.daemonize()
        self.run()

    def stop(self) -> None:
        """Stop the daemon."""
        try:
            pid: int = self.pid_from_pidfile()
        except (FileNotFoundError, ValueError):
            message: str = "pidfile does not exist. Daemon not running?\n"
            self._log(DEBUG, message)
            return
        self.kill_pid(pid)

    def restart(self) -> None:
        """Restart the daemon."""
        self.stop()
        self.start()

    def run(self) -> None:
        """Daemon main loop."""
        self.notifier = NotificationService()
        while True:
            sleep(1)
            self.notifier.send_notification("test")

    def _message(self, message: str) -> str:
        return f"Daemon: {message}"

    def _log(self, level: int, message: str) -> None:
        log(level, self._message(message))
