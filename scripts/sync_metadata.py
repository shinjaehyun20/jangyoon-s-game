#!/usr/bin/env python3
"""
장윤이 게임 아케이드 (jangyoon-s-game) — 7대 메타데이터 원자적 자동 동기화기 (sync_metadata.py)

역할:
1. games.json을 단일 진실 공급원(SSOT)으로 삼아 전체 게임 목록 및 개수 파악
2. 7대 필수 문서/에셋을 원자적으로 자동 갱신:
   - menu.json (최신 게임 메뉴 카테고리 누락 방지 자동 추가)
   - README.md (배지, 상단 설명, 히어로 링크, 서머리 카운터, 전체 게임 목록 표, 최근 변경사항 헤더/카운터)
   - docs/github-about.md (카운터 동기화)
   - index.html (메타 설명 카운터 동기화)
   - docs/assets/portfolio-hero.svg (SVG 텍스트 카운터 동기화)
   - CHANGES.md (최신 총 게임 카운터 동기화)
3. 갱신 후 verify_integrity.py를 자동 실행하여 무결성 100% PASS 검증
"""

import os
import sys
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GAMES_JSON = REPO_ROOT / "games.json"
MENU_JSON = REPO_ROOT / "menu.json"
README_MD = REPO_ROOT / "README.md"
INDEX_HTML = REPO_ROOT / "index.html"
GITHUB_ABOUT = REPO_ROOT / "docs" / "github-about.md"
HERO_SVG = REPO_ROOT / "docs" / "assets" / "portfolio-hero.svg"
CHANGES_MD = REPO_ROOT / "CHANGES.md"
VERIFY_SCRIPT = REPO_ROOT / "scripts" / "verify_integrity.py"

def sync_all():
    print("=" * 60)
    print(" 🔄 장윤이 게임 아케이드 7대 메타데이터 원자적 자동 동기화")
    print("=" * 60)

    if not GAMES_JSON.exists():
        print(f"[ERROR] games.json이 존재하지 않습니다: {GAMES_JSON}")
        return False

    with open(GAMES_JSON, "r", encoding="utf-8") as f:
        games = json.load(f)

    total_games = len(games)
    count_str = str(total_games)
    print(f"[*] 총 등록 게임 수: {total_games}개")

    latest_games = games[-2:] if len(games) >= 2 else games
    today_str = datetime.now().strftime("%Y-%m-%d")
    year_month = datetime.now().strftime("%Y-%m")

    # 1. menu.json 동기화
    if MENU_JSON.exists():
        try:
            with open(MENU_JSON, "r", encoding="utf-8") as f:
                menu = json.load(f)
            
            existing_menu_ids = set()
            kids_cat = None
            if isinstance(menu, list):
                for cat in menu:
                    if isinstance(cat, dict):
                        if cat.get("id") == "kids":
                            kids_cat = cat
                        for item in cat.get("items", []):
                            if isinstance(item, dict) and "id" in item:
                                existing_menu_ids.add(item["id"])

            added = False
            if kids_cat is not None and "items" in kids_cat:
                for g in latest_games:
                    gid = g.get("id")
                    if gid and gid not in existing_menu_ids:
                        kids_cat["items"].insert(0, {
                            "id": gid,
                            "title": g.get("title_ko", g.get("title", gid)),
                            "path": f"{gid}/index.html"
                        })
                        print(f"[*] menu.json 'kids'에 신규 게임 추가: {gid}")
                        added = True
            
            if added:
                with open(MENU_JSON, "w", encoding="utf-8") as f:
                    json.dump(menu, f, ensure_ascii=False, indent=2)
                print("[OK] menu.json 동기화 완료")
            else:
                print("[*] menu.json 최신 게임 이미 반영됨")
        except Exception as e:
            print(f"[WARN] menu.json 동기화 중 예외: {e}")

    # 2. README.md 동기화
    if README_MD.exists():
        readme = README_MD.read_text(encoding="utf-8")
        
        # 배지 카운터
        readme = re.sub(r'badge/games-\d+-6C5CE7', f'badge/games-{count_str}-6C5CE7', readme)
        # 상단 설명
        readme = re.sub(r'어린이 미니게임 \d+개', f'어린이 미니게임 {count_str}개', readme)
        # 히어로 링크
        readme = re.sub(r'\[\d+개의 게임을', f'[{count_str}개의 게임을', readme)
        # 서머리 카운터
        readme = re.sub(r'전체 \d+개 게임 목록', f'전체 {count_str}개 게임 목록', readme)

        # 최근 변경사항 섹션 처리
        rc_header = f"## 최근 변경사항 ({year_month})"
        if rc_header not in readme:
            # 첫 번째 '## 최근 변경사항' 앞에 삽입
            readme = re.sub(r'(## 최근 변경사항 \(\d{4}-\d{2}\))', f'{rc_header}\n\n\\1', readme, count=1)
        
        # 첫 번째 변경사항 블록 내 최신 게임 등록 여부 확인
        rc_match = re.search(r'## 최근 변경사항 \(\d{4}-\d{2}\)(.*?)(?=\n## |\Z)', readme, re.DOTALL)
        if rc_match:
            rc_content = rc_match.group(1)
            # 최신 게임이 라인에 없으면 첫 줄에 추가
            missing_in_rc = False
            for g in latest_games:
                gid = g.get("id", "")
                t_ko = g.get("title_ko", "")
                if gid not in rc_content and t_ko not in rc_content:
                    missing_in_rc = True
                    break
            
            if missing_in_rc:
                game_links = ", ".join(f"[{g.get('title_ko', g.get('title'))}]({g.get('id')}/index.html)" for g in latest_games)
                new_line = f"\n- {today_str}: {game_links} (총 {count_str}개)\n"
                readme = readme[:rc_match.start(1)] + new_line + readme[rc_match.start(1):]
            else:
                # 총 N개 카운터만 최신화
                def replace_count(m):
                    block = m.group(0)
                    return re.sub(r'\(총 \d+개\)', f'(총 {count_str}개)', block)
                readme = re.sub(r'## 최근 변경사항 \(\d{4}-\d{2}\).*?(?=\n## |\Z)', replace_count, readme, count=1, flags=re.DOTALL)

        # 전체 게임 목록 표 (<details>) 1:1 동기화
        table_rows = []
        table_rows.append(f"<details>\n<summary><strong>전체 {count_str}개 게임 목록 펼치기</strong></summary>\n\n")
        table_rows.append("| 게임 | 설명 | 카테고리 |\n|---|---|---|\n")
        
        # games.json 역순 정렬
        for g in reversed(games):
            t_ko = g.get("title_ko", g.get("title", ""))
            gid = g.get("id", "")
            path = g.get("path", "")
            desc = g.get("description", "")
            cat = "어린이/아케이드"
            table_rows.append(f"| [{t_ko} ({gid})](./{path}) | {desc} | {cat} |\n")
        
        table_rows.append("\n</details>")
        new_table_block = "".join(table_rows)

        readme = re.sub(r'<details>\s*<summary><strong>전체 \d+개 게임 목록 펼치기</strong></summary>.*?</details>', new_table_block, readme, flags=re.DOTALL)

        README_MD.write_text(readme, encoding="utf-8")
        print("[OK] README.md 7개 요소 전수 동기화 완료")

    # 3. docs/github-about.md
    if GITHUB_ABOUT.exists():
        about = GITHUB_ABOUT.read_text(encoding="utf-8")
        about = re.sub(r'\d+개 어린이', f'{count_str}개 어린이', about)
        about = re.sub(r'244개|246개', f'{count_str}개', about)
        GITHUB_ABOUT.write_text(about, encoding="utf-8")
        print(f"[OK] docs/github-about.md 카운터 동기화 완료 ({count_str}개)")

    # 4. index.html
    if INDEX_HTML.exists():
        html = INDEX_HTML.read_text(encoding="utf-8")
        html = re.sub(r'총 \d+개의', f'총 {count_str}개의', html)
        INDEX_HTML.write_text(html, encoding="utf-8")
        print(f"[OK] index.html 메타 카운터 동기화 완료 ({count_str}개)")

    # 5. docs/assets/portfolio-hero.svg
    if HERO_SVG.exists():
        hero = HERO_SVG.read_text(encoding="utf-8")
        hero = re.sub(r'>\d+</text>', f'>{count_str}</text>', hero)
        hero = re.sub(r'\d+개 어린이용', f'{count_str}개 어린이용', hero)
        HERO_SVG.write_text(hero, encoding="utf-8")
        print(f"[OK] docs/assets/portfolio-hero.svg 카운터 동기화 완료 ({count_str}개)")

    # 6. CHANGES.md
    if CHANGES_MD.exists():
        changes = CHANGES_MD.read_text(encoding="utf-8")
        if f"(총 {count_str}개)" not in changes and f"총 {count_str}개" not in changes:
            changes = re.sub(r'\(총 \d+개\)', f'(총 {count_str}개)', changes, count=1)
            CHANGES_MD.write_text(changes, encoding="utf-8")
            print(f"[OK] CHANGES.md 카운터 동기화 완료 ({count_str}개)")
        else:
            print("[*] CHANGES.md 이미 최신 카운터 반영됨")

    print("\n" + "=" * 60)
    print(" 🧪 무결성 검증기(verify_integrity.py) 자동 실행")
    print("=" * 60)
    res = subprocess.run([sys.executable, str(VERIFY_SCRIPT)], cwd=REPO_ROOT)
    if res.returncode == 0:
        print("\n🎉 [SUCCESS] 7대 메타데이터 동기화 및 무결성 검증 100% 통과 (PASS)!")
        return True
    else:
        print("\n❌ [FAIL] 무결성 검증 실패. 에러 로그를 확인하세요.")
        return False

if __name__ == "__main__":
    success = sync_all()
    sys.exit(0 if success else 1)
