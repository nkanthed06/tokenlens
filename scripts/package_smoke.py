"""Build and verify TokenLens in a clean virtual environment."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], *, cwd: Path | None = None) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="tokenlens-smoke-") as directory:
        workspace = Path(directory)
        source = workspace / "source"
        shutil.copytree(
            ROOT,
            source,
            ignore=shutil.ignore_patterns(
                ".git",
                ".venv",
                "__pycache__",
                "build",
                "dist",
                "*.egg-info",
            ),
        )
        distributions = workspace / "dist"
        run(
            [
                sys.executable,
                "-m",
                "build",
                "--wheel",
                "--outdir",
                str(distributions),
                str(source),
            ]
        )
        wheel = next(distributions.glob("tokenlens-*.whl"))

        environment = workspace / "venv"
        venv.create(environment, with_pip=True)
        binaries = environment / ("Scripts" if os.name == "nt" else "bin")
        run([str(binaries / "python"), "-m", "pip", "install", "--no-deps", str(wheel)])
        run(
            [
                str(binaries / "python"),
                "-c",
                "from tokenlens import __version__; print(__version__)",
            ]
        )
        run([str(binaries / "tokenlens"), "--help"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
