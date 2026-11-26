"""Hold a Windows byte-range lock for the lifetime of the bot."""
from contextlib import contextmanager
import os
from pathlib import Path

class AlreadyRunning(RuntimeError):
    pass

@contextmanager
def runtime_lock():
    if os.name != "nt":
        yield
        return
    import msvcrt
    folder = Path(os.environ["LOCALAPPDATA"]) / "CodePhrex" / "Phrex"
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / "runtime.lock").open("a+b") as handle:
        handle.seek(0)
        try:
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError as exc:
            raise AlreadyRunning("Runtime lock unavailable") from exc
        try:
            yield
        finally:
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
