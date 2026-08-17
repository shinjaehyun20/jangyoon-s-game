import os
import sys
import json
import re
import subprocess
from pathlib import Path

GAME_ROOT = r"D:\workspace\projects\active\jangyoon-s-game"
GAMES_JSON = os.path.join(GAME_ROOT, "games.json")
MENU_JSON = os.path.join(GAME_ROOT, "menu.json")
INDEX_HTML = os.path.join(GAME_ROOT, "index.html")
HERO_SVG = os.path.join(GAME_ROOT, "docs", "assets", "portfolio-hero.svg")
GITHUB_ABOUT = os.path.join(GAME_ROOT, "docs", "github-about.md")
README_MD = os.path.join(GAME_ROOT, "README.md")

NEW_GAMES = [
    {
        "id": "star-whale-voyage",
        "title": "Star Whale Voyage",
        "title_ko": "🐳 아기별고래 우주 유영",
        "description": "은하수 바다를 헤엄치는 아기별고래를 부드럽게 유영시켜 반짝이는 별가루를 모으고 우주 오로라를 펼치세요!",
        "thumbnail": "star-whale-voyage/thumb.svg",
        "path": "star-whale-voyage/index.html"
    },
    {
        "id": "potion-magic-shop",
        "title": "Potion Magic Shop",
        "title_ko": "🧪 숲속 마법 물약방",
        "description": "숲속 요정 손님들의 주문 순서에 맞춰 이슬, 풀잎, 별가루, 꽃잎을 플라스크에 넣어 신비한 마법 물약을 조제하세요!",
        "thumbnail": "potion-magic-shop/thumb.svg",
        "path": "potion-magic-shop/index.html"
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
    count_str = str(new_count)
    
    # 1. Update docs/assets/portfolio-hero.svg
    if os.path.exists(HERO_SVG):
        svg = Path(HERO_SVG).read_text(encoding="utf-8")
        svg = re.sub(r'\d+개 어린이용', f'{count_str}개 어린이용', svg)
        svg = re.sub(r'시작하는 \d+개의', f'시작하는 {count_str}개의', svg)
        svg = re.sub(r'>\d+</text>', f'>{count_str}</text>', svg)
        Path(HERO_SVG).write_text(svg, encoding="utf-8")
        print(f"Updated docs/assets/portfolio-hero.svg to count {new_count}.")

    # 2. Update docs/github-about.md
    if os.path.exists(GITHUB_ABOUT):
        about = Path(GITHUB_ABOUT).read_text(encoding="utf-8")
        about = re.sub(r'즐기는 \d+개 어린이', f'즐기는 {count_str}개 어린이', about)
        Path(GITHUB_ABOUT).write_text(about, encoding="utf-8")
        print(f"Updated docs/github-about.md to count {new_count}.")

    # 3. Update README.md
    if os.path.exists(README_MD):
        readme = Path(README_MD).read_text(encoding="utf-8")
        readme = re.sub(r'어린이 미니게임 \d+개', f'어린이 미니게임 {count_str}개', readme)
        readme = re.sub(r'badge/games-\d+-6C5CE7', f'badge/games-{count_str}-6C5CE7', readme)
        readme = re.sub(r'\[!\[\d+개의 게임을', f'[![{count_str}개의 게임을', readme)
        readme = re.sub(r'전체 \d+개 게임 목록', f'전체 {count_str}개 게임 목록', readme)
        readme = re.sub(r'games\.json 실측 \d+개', f'games.json 실측 {count_str}개', readme)
        Path(README_MD).write_text(readme, encoding="utf-8")
        print(f"Updated README.md to count {new_count}.")

    # 4. Update index.html (GitHub Pages Root)
    if os.path.exists(INDEX_HTML):
        html = Path(INDEX_HTML).read_text(encoding="utf-8")
        html = re.sub(r'content="장윤이를 위한 게임 모음[^"]*"', f'content="장윤이를 위한 게임 모음 - 총 {count_str}개의 타이핑, 퍼즐, 액션 게임을 한 곳에서"', html)
        Path(INDEX_HTML).write_text(html, encoding="utf-8")
        print(f"Updated index.html to count {new_count}.")

    # 5. Update GitHub Repo About description via gh CLI
    try:
        desc = f"터치로 바로 즐기는 {count_str}개 어린이 미니게임 아케이드 — 학습, 액션, 퍼즐, 창의 놀이."
        res = subprocess.run(
            ["gh", "repo", "edit", "shinjaehyun20/jangyoon-s-game", "--description", desc],
            capture_output=True, text=True, check=False
        )
        if res.returncode == 0:
            print(f"Updated GitHub repository About description to: {desc}")
        else:
            print(f"gh repo edit notice: {res.stderr.strip() or res.stdout.strip()}")
    except Exception as e:
        print(f"gh repo edit error: {e}")

if __name__ == "__main__":
    count = update_games_json()
    update_menu_json()
    update_counters(count)
    
    # 6. Run automated integrity check
    print("\n--- Running automated integrity check ---")
    verify_script = os.path.join(os.path.dirname(__file__), "verify_integrity.py")
    res = subprocess.run([sys.executable, verify_script], check=False)
    if res.returncode != 0:
        print("[!] Integrity check failed! Please fix errors above.")
        sys.exit(1)

