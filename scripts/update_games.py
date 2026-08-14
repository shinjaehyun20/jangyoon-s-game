import os
import json
import re

GAME_ROOT = r"D:\workspace\projects\active\jangyoon-s-game"
GAMES_JSON = os.path.join(GAME_ROOT, "games.json")
MENU_JSON = os.path.join(GAME_ROOT, "menu.json")
HERO_SVG = os.path.join(GAME_ROOT, "docs", "assets", "portfolio-hero.svg")
GITHUB_ABOUT = os.path.join(GAME_ROOT, "docs", "github-about.md")
README_MD = os.path.join(GAME_ROOT, "README.md")

NEW_GAMES = [
    {
        "id": "lumi-dew-garden",
        "title": "Lumi Dew Garden",
        "title_ko": "🌱 루미 이슬정원",
        "description": "이슬을 굴려 정원의 꽃과 풀을 싹틔우세요! 꽃잎과 잎새를 조화롭게 피워내는 힐링 물리 퍼즐.",
        "thumbnail": "lumi-dew-garden/thumb.svg",
        "path": "lumi-dew-garden/index.html"
    },
    {
        "id": "woodland-marble-slide",
        "title": "Woodland Marble Slide",
        "title_ko": "🪵 숲속 구슬길",
        "description": "나무 블록과 숲속 길을 이리저리 슬라이드해 구슬이 🏁 결승점까지 굴러가도록 경로를 완성하세요!",
        "thumbnail": "woodland-marble-slide/thumb.svg",
        "path": "woodland-marble-slide/index.html"
    }
]

def update_games_json():
    with open(GAMES_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Check if already present to prevent duplicates
    existing_ids = {g["id"] for g in data}
    to_add = [g for g in NEW_GAMES if g["id"] not in existing_ids]
    
    if not to_add:
        print("All games already exist in games.json.")
        return len(data)
        
    # Insert at top
    new_data = to_add + data
    with open(GAMES_JSON, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
        
    print(f"Added {len(to_add)} games to games.json. Total count: {len(new_data)}")
    return len(new_data)

def update_menu_json():
    with open(MENU_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Find kids category
    kids_cat = None
    for cat in data:
        if cat.get("id") == "kids":
            kids_cat = cat
            break
            
    if not kids_cat:
        print("Kids category not found in menu.json.")
        return
        
    existing_ids = {item["id"] for item in kids_cat["items"]}
    to_add = []
    for g in NEW_GAMES:
        if g["id"] not in existing_ids:
            to_add.append({
                "id": g["id"],
                "label": f"{g['title_ko'].split()[0]} {g['title_ko'].split(None, 1)[1]}" if ' ' in g['title_ko'] else g['title_ko'],
                "path": g["path"]
            })
            
    if not to_add:
        print("All games already exist in menu.json.")
        return
        
    kids_cat["items"] = to_add + kids_cat["items"]
    with open(MENU_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Added {len(to_add)} games to menu.json kids category items.")

def update_counters(new_count):
    old_count = new_count - 2
    old_str = str(old_count)
    new_str = str(new_count)
    
    # 1. Update docs/assets/portfolio-hero.svg
    if os.path.exists(HERO_SVG):
        svg_content = Path(HERO_SVG).read_text(encoding="utf-8")
        updated_svg = svg_content.replace(f"{old_str}개", f"{new_str}개")
        updated_svg = updated_svg.replace(f"하는 {old_str}개의", f"하는 {new_str}개의")
        updated_svg = updated_svg.replace(f">{old_str}</text>", f">{new_str}</text>")
        Path(HERO_SVG).write_text(updated_svg, encoding="utf-8")
        print(f"Updated docs/assets/portfolio-hero.svg to count {new_count}.")

    # 2. Update docs/github-about.md
    if os.path.exists(GITHUB_ABOUT):
        about_content = Path(GITHUB_ABOUT).read_text(encoding="utf-8")
        updated_about = about_content.replace(f"{old_str}개", f"{new_str}개")
        Path(GITHUB_ABOUT).write_text(updated_about, encoding="utf-8")
        print(f"Updated docs/github-about.md to count {new_count}.")

    # 3. Update README.md
    if os.path.exists(README_MD):
        readme_content = Path(README_MD).read_text(encoding="utf-8")
        updated_readme = readme_content.replace(f"미니게임 {old_str}개", f"미니게임 {new_str}개")
        updated_readme = updated_readme.replace(f"games-{old_str}-6C5CE7", f"games-{new_str}-6C5CE7")
        updated_readme = updated_readme.replace(f"전체 {old_str}개", f"전체 {new_str}개")
        updated_readme = updated_readme.replace(f"{old_str}개의 게임을", f"{new_str}개의 게임을")
        Path(README_MD).write_text(updated_readme, encoding="utf-8")
        print(f"Updated README.md to count {new_count}.")

from pathlib import Path
if __name__ == "__main__":
    count = update_games_json()
    update_menu_json()
    update_counters(count)
