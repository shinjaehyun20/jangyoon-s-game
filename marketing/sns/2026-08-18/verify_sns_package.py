#!/usr/bin/env python3
"""Offline verifier for the reusable Jangyoon's Game SNS package.

No platform session, cookie, credential, or remote response is read or written.
It validates only canonical project facts and prepared local promotion assets.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image

PACKAGE = Path(__file__).resolve().parent
PROJECT = PACKAGE.parents[2]
EXPECTED_GAME_COUNT = 228
FORBIDDEN_STALE_COUNT = "171"
REQUIRED_COPY = ("canonical.md", "x.md", "threads.md", "instagram.md")
EXPECTED_ASSETS = {
    "assets/x-card.png": (1600, 900),
    "assets/threads-card.png": (1200, 675),
    "assets/instagram-card.png": (1080, 1350),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> None:
    games = json.loads((PROJECT / "games.json").read_text(encoding="utf-8"))
    if len(games) != EXPECTED_GAME_COUNT:
        fail(f"games.json count={len(games)} expected={EXPECTED_GAME_COUNT}")

    checked_copy: dict[str, str] = {}
    for name in REQUIRED_COPY:
        path = PACKAGE / name
        if not path.is_file():
            fail(f"missing copy: {name}")
        body = path.read_text(encoding="utf-8")
        if str(EXPECTED_GAME_COUNT) not in body:
            fail(f"{name} does not state {EXPECTED_GAME_COUNT}")
        if FORBIDDEN_STALE_COUNT in body:
            fail(f"{name} includes stale count {FORBIDDEN_STALE_COUNT}")
        checked_copy[name] = sha256(path)

    checked_assets: dict[str, dict[str, object]] = {}
    for relative, expected_size in EXPECTED_ASSETS.items():
        path = PACKAGE / relative
        if not path.is_file():
            fail(f"missing asset: {relative}")
        with Image.open(path) as im:
            if im.size != expected_size:
                fail(f"{relative} size={im.size} expected={expected_size}")
        checked_assets[relative] = {"pixels": expected_size, "sha256": sha256(path)}

    status = json.loads((PACKAGE / "platform-status.json").read_text(encoding="utf-8"))
    if status.get("verified_claims", {}).get("game_count") != EXPECTED_GAME_COUNT:
        fail("platform-status verified_claims.game_count is not 226")

    print(json.dumps({
        "verifier": "verify_sns_package.py",
        "result": "PASS",
        "game_count": len(games),
        "copy_sha256": checked_copy,
        "assets": checked_assets,
        "network_or_session_access": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
