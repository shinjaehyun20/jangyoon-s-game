import os
import json
import re
from pathlib import Path

GAME_ROOT = r"D:\workspace\projects\active\jangyoon-s-game"
GAMES_JSON = os.path.join(GAME_ROOT, "games.json")
MENU_JSON = os.path.join(GAME_ROOT, "menu.json")
HERO_SVG = os.path.join(GAME_ROOT, "docs", "assets", "portfolio-hero.svg")
GITHUB_ABOUT = os.path.join(GAME_ROOT, "docs", "github-about.md")
README_MD = os.path.join(GAME_ROOT, "README.md")

NEW_GAMES = [
    {
        "id": "turtle-bubble-rescue",
        "title": "Turtle Bubble Rescue",
        "title_ko": "🐢 바다거북 비눗방울 구출",
        "description": "비눗방울에 갇힌 아기 바다거북과 물고기 친구들을 톡톡 터치해 안전한 산호초 둥지로 구출해주세요!",
        "thumbnail": "turtle-bubble-rescue/thumb.svg",
        "path": "turtle-bubble-rescue/index.html"
    },
    {
        "id": "cosmic-star-baker",
        "title": "Cosmic Star Baker",
        "title_ko": "🥐 우주 별빛 베이커리",
        "description": "외계인 손님들의 주문 순서에 맞춰 별빛 반죽, 행성 시럽, 별가루 토핑을 올려 맛있는 우주 디저트를 구워내세요!",
        "thumbnail": "cosmic-star-baker/thumb.svg",
        "path": "cosmic-star-baker/index.html"
    }
]

def update_games_json():
    with open(GAMES_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
        
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

if __name__ == "__main__":
    count = update_games_json()
    update_menu_json()
    update_counters(count)
