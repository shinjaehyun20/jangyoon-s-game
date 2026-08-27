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
CHANGES_MD = os.path.join(GAME_ROOT, "CHANGES.md")

NEW_GAMES = [
    {
        "id": "neon-circuit-connect",
        "title": "Neon Circuit Connect",
        "title_ko": "⚡ 네온 회로 연결사",
        "description": "타일을 회전시켜 발전소에서 아기 로봇까지 네온 전선을 연결하고 번쩍이는 에너지를 충전하세요!",
        "thumbnail": "neon-circuit-connect/thumb.svg",
        "path": "neon-circuit-connect/index.html"
    },
    {
        "id": "jungle-vine-swinger",
        "title": "Jungle Vine Swinger",
        "title_ko": "🐒 정글 덩굴 스윙 타잔",
        "description": "화면을 터치해 덩굴을 잡고 반동을 실어 날아가며 정글의 바나나와 별을 모으는 스윙 액션 놀이!",
        "thumbnail": "jungle-vine-swinger/thumb.svg",
        "path": "jungle-vine-swinger/index.html"
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
                "label": g["title_ko"],
                "path": g["path"]
            })
            
    if not to_add:
        print("All games already exist in menu.json.")
        return
        
    kids_cat["items"] = to_add + kids_cat["items"]
    with open(MENU_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Added {len(to_add)} games to menu.json kids category items.")

def update_changes_md():
    if not os.path.exists(CHANGES_MD):
        return
    txt = Path(CHANGES_MD).read_text(encoding="utf-8")
    if "## 2026-08-27" in txt:
        print("CHANGES.md already contains 2026-08-27.")
        return
        
    entry = """## 2026-08-27 (일일 게임 제작, nyx)

- 게임 2종 추가: `neon-circuit-connect`(⚡ 네온 회로 연결사), `jungle-vine-swinger`(🐒 정글 덩굴 스윙 타잔).
- `neon-circuit-connect` — 3x3/4x4 그리드 상의 회로 타일을 탭하여 90도씩 회전시켜 ⚡발전소에서 🤖아기 로봇까지 네온 전선을 연결하는 직관적이고 시각적으로 화려한 전기 연결 퍼즐 놀이. BFS 실시간 경로 탐색, 네온 펄스 및 스파크 파티클 효과, 성공 시 스테이지 클리어 및 보너스 시간 지급.
- `jungle-vine-swinger` — 진자 운동으로 흔들리는 덩굴을 타고 화면을 탭하여 시원하게 공중으로 날아가며 🍌바나나와 ⭐별을 모으고 다음 덩굴을 잡는 타이밍 기반 정글 스윙 액션 놀이. 부드러운 60fps 캔버스 물리, 트램펄린 나뭇잎 안전 낙하 방지, 콤보 스윙 시스템 탑재.
- 두 게임 모두 단일 HTML, 외부 CDN 의존성 0건, 100dvh/overflow 보호, Pointer Events, 시작·종료 오버레이, 홈 링크, localStorage 최고기록(`neon_circuit_connect_best`, `jungle_vine_swinger_best`), SVG 썸네일 포함.
- `games.json` 230→232, 고유 ID 232(중복 0건), `menu.json` kids 카테고리 최상단에 신규 2건 배치. README 뱃지·상단문구·게임 표·최근변경 섹션과 docs/assets/portfolio-hero.svg, docs/github-about.md, index.html의 하드코딩 게임 카운트를 실측 232로 동기화.

"""
    new_txt = entry + txt
    Path(CHANGES_MD).write_text(new_txt, encoding="utf-8")
    print("Updated CHANGES.md with 2026-08-27 entry.")

def update_readme(new_count):
    if not os.path.exists(README_MD):
        return
    txt = Path(README_MD).read_text(encoding="utf-8")
    count_str = str(new_count)
    
    # 1. Counters
    txt = re.sub(r'어린이 미니게임 \d+개', f'어린이 미니게임 {count_str}개', txt)
    txt = re.sub(r'badge/games-\d+-6C5CE7', f'badge/games-{count_str}-6C5CE7', txt)
    txt = re.sub(r'\[!\[\d+개의 게임을', f'[![{count_str}개의 게임을', txt)
    txt = re.sub(r'전체 \d+개 게임 목록', f'전체 {count_str}개 게임 목록', txt)
    txt = re.sub(r'games\.json 실측 \d+개', f'games.json 실측 {count_str}개', txt)
    
    # 2. Table rows
    table_header = "| 게임 | 설명 | 카테고리 |\n|---|---|---|\n"
    new_rows = "| [⚡ 네온 회로 연결사 (neon-circuit-connect)](./neon-circuit-connect) | 타일을 회전시켜 발전소에서 아기 로봇까지 네온 전선을 연결하고 번쩍이는 에너지를 충전하세요! | 어린이/퍼즐·인지 |\n| [🐒 정글 덩굴 스윙 타잔 (jungle-vine-swinger)](./jungle-vine-swinger) | 화면을 터치해 덩굴을 잡고 반동을 실어 날아가며 정글의 바나나와 별을 모으는 스윙 액션 놀이! | 어린이/액션·물리 |\n"
    
    if "neon-circuit-connect" not in txt and table_header in txt:
        txt = txt.replace(table_header, table_header + new_rows)
        print("Added new game rows to README.md table.")
        
    # 3. Recent Changes Section
    recent_header = "## 최근 변경사항 (2026-08)\n"
    recent_entry = """- **⚡ 네온 회로 연결사 · 🐒 정글 덩굴 스윙 타잔 추가 (2026-08-27)** — 터치 회전으로 ⚡발전소에서 🤖로봇까지 전선을 잇는 네온 회로 퍼즐과 진자 물리 반동으로 시원하게 날아가는 정글 스윙 액션 미니게임 2종 추가 (총 232개). 단일 HTML, 외부 CDN 의존성 없음, 100dvh/overflow 보호, Pointer Events 통합 조작.

"""
    if "2026-08-27" not in txt and recent_header in txt:
        txt = txt.replace(recent_header, recent_header + "\n" + recent_entry, 1)
        print("Added 2026-08-27 entry to README.md recent changes.")
        
    Path(README_MD).write_text(txt, encoding="utf-8")
    print(f"Updated README.md to count {count_str}.")

def update_other_docs(new_count):
    count_str = str(new_count)
    
    # 1. docs/assets/portfolio-hero.svg
    if os.path.exists(HERO_SVG):
        svg = Path(HERO_SVG).read_text(encoding="utf-8")
        svg = re.sub(r'\d+개 어린이용', f'{count_str}개 어린이용', svg)
        svg = re.sub(r'시작하는 \d+개의', f'시작하는 {count_str}개의', svg)
        svg = re.sub(r'>\d+</text>', f'>{count_str}</text>', svg)
        Path(HERO_SVG).write_text(svg, encoding="utf-8")
        print(f"Updated docs/assets/portfolio-hero.svg to count {new_count}.")

    # 2. docs/github-about.md
    if os.path.exists(GITHUB_ABOUT):
        about = Path(GITHUB_ABOUT).read_text(encoding="utf-8")
        about = re.sub(r'즐기는 \d+개 어린이', f'즐기는 {count_str}개 어린이', about)
        Path(GITHUB_ABOUT).write_text(about, encoding="utf-8")
        print(f"Updated docs/github-about.md to count {new_count}.")

    # 3. index.html (GitHub Pages Root)
    if os.path.exists(INDEX_HTML):
        html = Path(INDEX_HTML).read_text(encoding="utf-8")
        html = re.sub(r'content="장윤이를 위한 게임 모음[^"]*"', f'content="장윤이를 위한 게임 모음 - 총 {count_str}개의 타이핑, 퍼즐, 액션 게임을 한 곳에서"', html)
        Path(INDEX_HTML).write_text(html, encoding="utf-8")
        print(f"Updated index.html to count {new_count}.")

    # 4. GitHub Repo About description via gh CLI
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
    update_changes_md()
    update_readme(count)
    update_other_docs(count)
    print("\n--- All metadata and documentation updated successfully ---")
