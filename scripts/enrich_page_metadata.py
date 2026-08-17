#!/usr/bin/env python3
"""Add idempotent, catalog-sourced SEO/AEO metadata to local game pages."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = "<!-- jangyoon-s-game catalog metadata -->"


def metadata(game: dict[str, str]) -> str:
    title = game["title_ko"].strip() or game["title"].strip()
    description = game["description"].strip()
    full_description = f"{title} — {description} 장윤이 게임 놀이터의 어린이 미니게임입니다."
    return "\n".join(
        [
            MARKER,
            f'<meta name="description" content="{html.escape(full_description, quote=True)}">',
            f'<meta property="og:title" content="{html.escape(title, quote=True)} | 장윤이 게임 놀이터">',
            f'<meta property="og:description" content="{html.escape(full_description, quote=True)}">',
        ]
    )


def main() -> int:
    games = json.loads((ROOT / "games.json").read_text(encoding="utf-8"))
    updated = 0
    skipped = 0
    for game in games:
        path = str(game["path"])
        if path.startswith(("http://", "https://")):
            skipped += 1
            continue
        page = ROOT / path
        text = page.read_text(encoding="utf-8")
        if MARKER in text:
            skipped += 1
            continue
        if not re.search(r"</head\s*>", text, flags=re.IGNORECASE):
            raise ValueError(f"missing </head>: {page.relative_to(ROOT)}")
        text = re.sub(r"</head\s*>", metadata(game) + "\n</head>", text, count=1, flags=re.IGNORECASE)
        page.write_text(text, encoding="utf-8")
        updated += 1
    print(json.dumps({"updated": updated, "skipped": skipped, "catalog_games": len(games)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
