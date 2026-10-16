"""Regression coverage for registration omissions hidden by array ordering."""
import copy
import json
import unittest
from pathlib import Path

from verify_integrity import menu_consistency_errors, recent_games, live_metadata_errors

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
        menu[0]["items"][0]["path"] = self.games[-1]["path"]
        self.assertTrue(any("경로 불일치" in e for e in menu_consistency_errors(self.games, menu)))

    def test_newest_games_do_not_depend_on_array_order(self):
        expected = {"compass-treasure-safari", "star-magnet-lab"}
        fixture = [g for g in self.games if g["id"] in expected]
        fixture.append({"id": "older-tail", "created": "2026-01-01"})
        self.assertEqual(expected, {g["id"] for g in recent_games(fixture)})
        self.assertEqual(expected, {g["id"] for g in recent_games(list(reversed(fixture)))})

    def test_live_metadata_cannot_pass_on_count_and_old_tail_alone(self):
        live = copy.deepcopy(self.games)
        live[0]["description"] = "COMPASS TREASURE SAFARI"
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


if __name__ == "__main__":
    unittest.main()
