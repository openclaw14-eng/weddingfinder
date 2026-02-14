# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## Python Standards

- Python 3.10+ preferred (match-case, better typing, | union syntax)
- Type hints everywhere they help
- `pathlib` > `os.path`
- `dataclasses` or `Pydantic` for structured data
- `httpx` or `aiohttp` for HTTP (requests if sync-only)
- `typer` or `argparse` for CLI tools
- Format: `ruff` (replaces black + isort + flake8)
- Lint: `ruff` + `mypy --strict` when it matters
- Project structure: `pyproject.toml` > `setup.py`
- Tests: `pytest`, `pytest-asyncio` for async
- Docs: Google-style docstrings, concise

## Research

- Latest fixes? Check GitHub releases, PEPs, packaging.python.org
- Don't guess — verify with sources
- Stack Overflow is a hint, not an authority

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
