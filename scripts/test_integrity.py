"""Regression coverage for registration omissions hidden by array ordering."""
import copy
import json
import unittest
import tempfile
import shutil
from unittest.mock import patch
import sync_metadata
from pathlib import Path

from verify_integrity import menu_consistency_errors, recent_games, live_metadata_errors, catalog_content_errors

ROOT = Path(__file__).resolve().parent.parent


class RegistrationTests(unittest.TestCase):
    def setUp(self):
        self.games = json.loads((ROOT / "games.json").read_text(encoding="utf-8"))
        self.menu = json.loads((ROOT / "menu.json").read_text(encoding="utf-8"))

    def test_entire_catalog_has_unique_consistent_menu_entries(self):
        self.assertEqual([], menu_consistency_errors(self.games, self.menu))

    def test_missing_front_middle_or_last_entry_is_detected(self):
        for game in (self.games[0], self.games[len(self.games) // 2], self.games[-1]):
            menu = copy.deepcopy(self.menu)
            for section in menu:
                section["items"] = [i for i in section["items"] if i["id"] != game["id"]]
            self.assertTrue(any(game["id"] in e for e in menu_consistency_errors(self.games, menu)))

    def test_duplicate_and_wrong_existing_path_are_detected(self):
        menu = copy.deepcopy(self.menu)
        menu[0]["items"].append(copy.deepcopy(menu[0]["items"][0]))
        self.assertTrue(any("중복" in e for e in menu_consistency_errors(self.games, menu)))
        menu = copy.deepcopy(self.menu)
        menu[0]["items"][0]["path"] = "invalid_wrong_dir/index.html"
        self.assertTrue(any("경로 불일치" in e for e in menu_consistency_errors(self.games, menu)))

    def test_newest_games_do_not_depend_on_array_order(self):
        expected = {"compass-treasure-safari", "star-magnet-lab"}
        fixture = [g for g in self.games if g["id"] in expected]
        fixture.append({"id": "older-tail", "created": "2026-01-01"})
        self.assertEqual(expected, {g["id"] for g in recent_games(fixture)})
        self.assertEqual(expected, {g["id"] for g in recent_games(list(reversed(fixture)))})

    def test_live_metadata_cannot_pass_on_count_and_old_tail_alone(self):
        live = copy.deepcopy(self.games)
        target = recent_games(self.games)[0]
        for g in live:
            if g["id"] == target["id"]:
                g["description"] += " [stale deployment fixture]"
                break
        self.assertTrue(any("description" in e for e in live_metadata_errors(self.games, live)))
        self.assertEqual([], live_metadata_errors(self.games, list(reversed(self.games))))

    def test_two_game_korean_content_readme_and_home_links(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for game in self.games:
            if game["id"] not in {"compass-treasure-safari", "star-magnet-lab"}:
                continue
            self.assertRegex(game["description"], r"[가-힣]")
            self.assertEqual(game["description"], game["subtitle"])
            self.assertEqual(game["thumb"], game["thumbnail"])
            self.assertIn(game["title_ko"], readme)
            self.assertIn(game["description"], readme)
            html = (ROOT / game["path"]).read_text(encoding="utf-8")
            self.assertIn('href="../index.html" id="homeBtn"', html)
            self.assertEqual(3, html.count('href="../index.html"'))
            self.assertNotIn('maximum-scale=1', html)
            self.assertIn('overflow-y: auto', html)
            self.assertIn('@media (max-width: 420px)', html)
            self.assertIn('@media (max-height: 640px)', html)

    def test_replayed_placeholder_and_duplicate_catalog_are_rejected(self):
        games = copy.deepcopy(self.games)
        target = recent_games(self.games)[0]
        for g in games:
            if g["id"] == target["id"]:
                g["description"] = "COMPASS TREASURE SAFARI"
                break
        self.assertTrue(any("description" in e for e in catalog_content_errors(games)))
        games = copy.deepcopy(self.games)
        games.append(copy.deepcopy(games[0]))
        self.assertTrue(any("duplicate" in e for e in catalog_content_errors(games)))

    def test_sync_preserves_existing_games_and_is_idempotent(self):
        names = ("GAMES_JSON", "MENU_JSON", "README_MD", "INDEX_HTML", "GITHUB_ABOUT", "HERO_SVG", "CHANGES_MD")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in names:
                source = getattr(sync_metadata, name)
                target = root / source.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
            for game in self.games[:2]:
                target = root / game["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / game["path"], target)
            from contextlib import ExitStack
            with ExitStack() as stack:
                for name in names:
                    stack.enter_context(patch.object(sync_metadata, name, root / getattr(sync_metadata, name).relative_to(ROOT)))
                stack.enter_context(patch.object(sync_metadata, "REPO_ROOT", root))
                runner = stack.enter_context(patch.object(sync_metadata.subprocess, "run"))
                runner.return_value.returncode = 0
                before = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
                self.assertTrue(sync_metadata.sync_all())
                first = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
                for path in [Path("games.json"), Path("menu.json")] + [Path(g["path"]) for g in self.games[:2]]:
                    self.assertEqual(before[path], first[path])
                self.assertTrue(sync_metadata.sync_all())
                self.assertEqual(first, {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()})
                games = json.loads((root / "games.json").read_text(encoding="utf-8"))
                target_id = recent_games(games)[0]["id"]
                for g in games:
                    if g["id"] == target_id:
                        g["description"] = "COMPASS TREASURE SAFARI"
                        break
                (root / "games.json").write_text(json.dumps(games), encoding="utf-8")
                before_rejected = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
                self.assertFalse(sync_metadata.sync_all())
                self.assertEqual(before_rejected, {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()})


if __name__ == "__main__":
    unittest.main()
