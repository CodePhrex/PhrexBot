"""Explicitly invoked local launcher; does not register startup tasks."""
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def load_config(path, inherited):
    env = dict(inherited)
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        match = re.fullmatch(r"([A-Z_][A-Z0-9_]*)=(.*)", line)
        if match:
            env[match[1]] = match[2].strip()
    return env

def main():
    if os.name != "nt":
        return 2
    folder = Path(os.environ["LOCALAPPDATA"]) / "CodePhrex" / "Phrex" / "logs"
    folder.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("phrex.runtime")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(folder / "runtime.log", maxBytes=1048576, backupCount=3, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    try:
        python = ROOT / ".venv" / "Scripts" / "python.exe"
        if not python.is_file() or not (ROOT / "bot.py").is_file():
            raise FileNotFoundError()
        env = load_config(ROOT / ".env", os.environ)
        logger.info("Runtime launch requested")
        result = subprocess.run([str(python), "-u", str(ROOT / "bot.py")], cwd=ROOT, env=env, check=False)
        logger.info("Runtime exited with code %d", result.returncode)
        return result.returncode
    except Exception as exc:
        logger.error("Runtime launch failed: %s", type(exc).__name__)
        return 1
    finally:
        logger.removeHandler(handler)
        handler.close()

if __name__ == "__main__":
    sys.exit(main())
