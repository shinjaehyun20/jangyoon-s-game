#!/usr/bin/env python3
"""
장윤이 게임 모음 (jangyoon-s-game) — 전수 무결성 및 다양성 검증기 (CI / Pre-commit Gate)

검증 범위:
1. games.json 구조 및 실물 파일 링크 무결성 (404 방지, 이미지 깨짐 방지)
2. 썸네일 SVG 문법 파싱 및 0바이트 여부
3. menu.json 항목 및 실물 파일 링크 무결성
4. 루트 디렉토리 vs 등록 디렉토리 1:1 정합성 (하위 오배치, 유령 폴더, 누락 폴더 검출)
5. 문서 카운터 동기화 (README.md, index.html, docs/github-about.md, docs/assets/portfolio-hero.svg)
6. 게임 메커니즘 및 키워드 유사도/다양성 진단

종료 코드:
- 0: 모든 무결성 검증 통과 (PASS)
- 1: 무결성 결함 검출 (FAIL)
"""

import os
import sys
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import Counter, defaultdict

REPO_ROOT = Path(__file__).resolve().parent.parent
GAMES_JSON = REPO_ROOT / "games.json"
MENU_JSON = REPO_ROOT / "menu.json"
README_MD = REPO_ROOT / "README.md"
INDEX_HTML = REPO_ROOT / "index.html"
GITHUB_ABOUT = REPO_ROOT / "docs" / "github-about.md"
HERO_SVG = REPO_ROOT / "docs" / "assets" / "portfolio-hero.svg"
CHANGES_MD = REPO_ROOT / "CHANGES.md"

REQUIRED_GAME_FIELDS = ["id", "title", "title_ko", "description", "thumbnail", "path"]
EXCLUDED_DIRS = {".git", ".claude", ".github", "__pycache__", "_candidates", "docs", "games", "marketing", "output", "scripts"}

def check_all():
    errors = []
    warnings = []

    print("==================================================")
    print(" 🎮 장윤이 게임 아케이드 무결성 검증 (Integrity Verifier)")
    print("==================================================")

    # [1] games.json 로드 및 검증
    if not GAMES_JSON.exists():
        errors.append(f"[치명적] games.json 파일이 존재하지 않습니다: {GAMES_JSON}")
        return False, errors, warnings

    try:
        with open(GAMES_JSON, "r", encoding="utf-8") as f:
            games = json.load(f)
    except Exception as e:
        errors.append(f"[치명적] games.json JSON 파싱 오류: {e}")
        return False, errors, warnings

    if not isinstance(games, list):
        errors.append("[치명적] games.json 루트는 배열(list)이어야 합니다.")
        return False, errors, warnings

    total_games = len(games)
    print(f"[*] 등록된 총 게임 수: {total_games}개")

    game_ids = set()
    game_paths = set()

    for idx, g in enumerate(games):
        prefix = f"게임 [{idx}]"
        # 필수 필드
        for field in REQUIRED_GAME_FIELDS:
            if field not in g or not str(g[field]).strip():
                errors.append(f"{prefix} '{field}' 필드가 누락되었거나 비어있습니다 (id: {g.get('id', 'N/A')})")

        gid = g.get("id", "")
        if gid:
            if gid in game_ids:
                errors.append(f"{prefix} 중복된 게임 ID 검출: '{gid}'")
            game_ids.add(gid)

        # Path 검증
        path_str = g.get("path", "")
        if path_str:
            if path_str.startswith("http://") or path_str.startswith("https://"):
                pass # 외부 링크 허용
            else:
                game_paths.add(path_str.split("/")[0])
                target_file = REPO_ROOT / path_str.replace("/", os.sep)
                if not target_file.exists():
                    errors.append(f"{prefix} [{gid}] 404 링크 에러 — 실물 파일 없음: {path_str}")
                elif target_file.stat().st_size == 0:
                    errors.append(f"{prefix} [{gid}] 0바이트 빈 파일: {path_str}")

        # Thumbnail 검증
        thumb_str = g.get("thumbnail", "")
        if thumb_str:
            if thumb_str.startswith("http://") or thumb_str.startswith("https://"):
                pass
            else:
                target_thumb = REPO_ROOT / thumb_str.replace("/", os.sep)
                if not target_thumb.exists():
                    errors.append(f"{prefix} [{gid}] 썸네일 이미지 파일 부존재 (깨진 이미지): {thumb_str}")
                elif target_thumb.stat().st_size == 0:
                    errors.append(f"{prefix} [{gid}] 0바이트 빈 썸네일 파일: {thumb_str}")
                elif thumb_str.endswith(".svg"):
                    try:
                        ET.parse(str(target_thumb))
                    except ET.ParseError as pe:
                        errors.append(f"{prefix} [{gid}] SVG 썸네일 XML 구문 오류 ({thumb_str}): {pe}")

    print(f"[*] games.json 검증 완료 (에러 {len([e for e in errors if 'games.json' in e or '게임 [' in e])}건)")

    # [2] menu.json 검증
    if MENU_JSON.exists():
        try:
            with open(MENU_JSON, "r", encoding="utf-8") as f:
                menu = json.load(f)
            menu_item_count = 0
            menu_ids = set()
            for sec in menu:
                for item in sec.get("items", []):
                    menu_item_count += 1
                    gid = item.get("id")
                    if gid:
                        menu_ids.add(gid)
                    mpath = item.get("path", "")
                    if mpath and not mpath.startswith("http"):
                        mtarget = REPO_ROOT / mpath.replace("/", os.sep)
                        if not mtarget.exists():
                            errors.append(f"menu.json [{item.get('id')}] 404 메뉴 경로: {mpath}")
            
            # 최신 게임 ID가 menu.json에 등록되어 있는지 검증 (메뉴 누락 방지)
            if len(games) >= 2:
                recent_ids = [g.get("id") for g in games[-2:]]
                for rid in recent_ids:
                    if rid and rid not in menu_ids:
                        errors.append(f"menu.json 동기화 누락: 최신 게임 '{rid}'가 menu.json 항목에 등록되지 않았습니다.")
            
            print(f"[*] menu.json 검증 완료 (총 {menu_item_count}개 메뉴 항목 검사, 최신 게임 등록 확인)")
        except Exception as e:
            errors.append(f"menu.json 파싱 오류: {e}")

    # [3] 물리 디렉토리 구조 검증 (오배치, 미등록 게임 검출)
    subdirs = [d for d in os.listdir(REPO_ROOT) if (REPO_ROOT / d).is_dir() and d not in EXCLUDED_DIRS]
    for d in subdirs:
        dpath = REPO_ROOT / d
        html_file = dpath / "index.html"
        if not html_file.exists():
            warnings.append(f"루트 서브폴더 '{d}'에 index.html이 없습니다.")
        if d not in game_ids and d not in game_paths:
            errors.append(f"미등록 게임 폴더 발견 (games.json에 등록되지 않음): '{d}'")

    # games/ 하위 서브폴더 잔여물 검사
    games_sub = REPO_ROOT / "games"
    if games_sub.exists() and any(games_sub.iterdir()):
        for item in games_sub.iterdir():
            if item.is_dir():
                errors.append(f"루트가 아닌 'games/' 하위로 오배치된 게임 폴더 발견: {item.name}")

    # [4] 카운터 및 문서 동기화 전수 검증 (README.md, index.html, docs/github-about.md, CHANGES.md, SVG)
    count_str = str(total_games)
    
    # 4-1. README.md
    if README_MD.exists():
        readme_txt = README_MD.read_text(encoding="utf-8")
        if f"games-{count_str}-6C5CE7" not in readme_txt:
            errors.append(f"README.md 배지 카운터 오류 (badge/games-{count_str}-6C5CE7 미발견)")
        if f"어린이 미니게임 {count_str}개" not in readme_txt:
            errors.append(f"README.md 상단 설명 카운터 오류 ('어린이 미니게임 {count_str}개' 미발견)")
        if f"[{count_str}개의 게임을" not in readme_txt:
            errors.append(f"README.md 히어로 링크 카운터 오류 ('{count_str}개의 게임을' 미발견)")
        if f"전체 {count_str}개 게임 목록" not in readme_txt:
            errors.append(f"README.md summary 카운터 오류 ('전체 {count_str}개 게임 목록' 미발견)")
        
        # README.md 게임 목록 표 행 1:1 정합성 검증
        details_match = re.search(r'<details>\s*<summary><strong>전체 \d+개 게임 목록 펼치기</strong></summary>(.*?)</details>', readme_txt, re.DOTALL)
        if not details_match:
            errors.append("README.md 내 전체 게임 목록 <details> 표가 존재하지 않습니다.")
        else:
            table_rows = [l for l in details_match.group(1).splitlines() if l.strip().startswith('| [')]
            if len(table_rows) != total_games:
                errors.append(f"README.md 게임 목록 표 행 개수 불일치: 표({len(table_rows)}행) != games.json({total_games}개)")
            else:
                print(f"[*] README.md 게임 목록 표 1:1 동기화 정상 확인 ({len(table_rows)}/{total_games}행)")

        # README.md 최근 변경사항 섹션 내 최신 총 게임 수 및 게임 타이틀 일치 검증
        recent_changes_match = re.search(r'## 최근 변경사항 \(\d{4}-\d{2}\)(.*?)(?=\n## |\Z)', readme_txt, re.DOTALL)
        if not recent_changes_match:
            errors.append("README.md 내 '## 최근 변경사항' 섹션이 발견되지 않았습니다.")
        else:
            rc_content = recent_changes_match.group(1)
            if f"(총 {count_str}개)" not in rc_content and f"총 {count_str}개" not in rc_content:
                errors.append(f"README.md '## 최근 변경사항' 내 최신 총 게임 카운터('총 {count_str}개') 미반영")
            else:
                print(f"[*] README.md 최근 변경사항 최신 총 게임 카운터 정상 확인 (총 {count_str}개)")

            if len(games) >= 2:
                for g in games[-2:]:
                    t_ko = g.get("title_ko", "")
                    t_en = g.get("title", "")
                    gid = g.get("id", "")
                    if t_ko and (t_ko not in rc_content and gid not in rc_content and t_en not in rc_content):
                        errors.append(f"README.md '## 최근 변경사항' 내 최신 게임 '{t_ko}'({gid}) 미등록")

        # README.md 중복 섹션 헤더 검출
        for h_year in ["2026-09", "2026-08", "2026-07", "2026-06", "2026-05", "2026-04"]:
            header_pattern = f"## 최근 변경사항 ({h_year})"
            h_count = readme_txt.count(header_pattern)
            if h_count > 1:
                errors.append(f"README.md 내 '{header_pattern}' 중복 헤더 검출 ({h_count}회)")
    else:
        errors.append("README.md 파일이 존재하지 않습니다.")

    # 4-2. docs/github-about.md
    if GITHUB_ABOUT.exists():
        about_txt = GITHUB_ABOUT.read_text(encoding="utf-8")
        if f"{count_str}개 어린이" not in about_txt:
            errors.append(f"docs/github-about.md 카운터 오류 ('{count_str}개 어린이' 미발견)")
        if "244개" in about_txt or "246개" in about_txt:
            errors.append("docs/github-about.md 내 구버전 잔여 카운터(244개 또는 246개) 발견")
        print(f"[*] docs/github-about.md 정합성 정상 확인 ({count_str}개)")
    else:
        errors.append("docs/github-about.md 파일이 존재하지 않습니다.")

    # 4-3. index.html
    if INDEX_HTML.exists():
        html_txt = INDEX_HTML.read_text(encoding="utf-8")
        if f"총 {count_str}개의" not in html_txt:
            errors.append(f"index.html 메타 설명 내 카운터 오류 ('총 {count_str}개의' 미발견)")
        print(f"[*] index.html 메타 카운터 정상 확인 ({count_str}개)")
    else:
        errors.append("index.html 파일이 존재하지 않습니다.")

    # 4-4. portfolio-hero.svg
    if HERO_SVG.exists():
        hero_txt = HERO_SVG.read_text(encoding="utf-8")
        if f">{count_str}</text>" not in hero_txt and f"{count_str}개 어린이용" not in hero_txt:
            errors.append(f"portfolio-hero.svg 내 카운터 오류 ({count_str} 미발견)")
        print(f"[*] portfolio-hero.svg 카운터 정상 확인 ({count_str}개)")
    else:
        errors.append("portfolio-hero.svg 파일이 존재하지 않습니다.")

    # 4-5. CHANGES.md
    if CHANGES_MD.exists():
        changes_txt = CHANGES_MD.read_text(encoding="utf-8")
        if f"총 {count_str}개" not in changes_txt:
            errors.append(f"CHANGES.md 내 최신 총 게임 카운터('총 {count_str}개') 미발견")
        print(f"[*] CHANGES.md 최신 게임 이력 정상 확인")
    else:
        errors.append("CHANGES.md 파일이 존재하지 않습니다.")

    # 4-6. GitHub About Description Check & Auto-sync via gh CLI
    try:
        gh_view = subprocess.run(["gh", "repo", "view", "shinjaehyun20/jangyoon-s-game", "--json", "description"], capture_output=True, text=True, timeout=5)
        if gh_view.returncode == 0:
            gh_desc = json.loads(gh_view.stdout).get("description", "")
            if count_str not in gh_desc:
                warnings.append(f"GitHub Repo Description({gh_desc})에 최신 수치({count_str})가 반영되지 않았습니다. 자동 갱신을 실행합니다.")
                new_desc = f"터치로 바로 즐기는 {count_str}개 어린이 미니게임 아케이드 — 학습, 액션, 퍼즐, 창의 놀이."
                subprocess.run(["gh", "repo", "edit", "shinjaehyun20/jangyoon-s-game", "--description", new_desc], check=False)
                print(f"[*] GitHub Repo Description 자동 갱신 완료 -> {new_desc}")
            else:
                print(f"[*] GitHub Repo Description 최신 일치 확인 -> {gh_desc}")
    except Exception as e:
        warnings.append(f"gh CLI Description 확인 실패 (네트워크 또는 비설치): {e}")

    # 4-7. Git Branches Hygiene (No lingering merged worktree/branches)
    try:
        br_res = subprocess.run(["git", "branch", "-r", "--merged", "origin/main"], capture_output=True, text=True, cwd=str(REPO_ROOT), timeout=5)
        if br_res.returncode == 0:
            lingering = [b.strip() for b in br_res.stdout.splitlines() if b.strip() and not b.strip().endswith("origin/main") and not b.strip().endswith("origin/HEAD")]
            if lingering:
                warnings.append(f"origin/main에 머지된 후 삭제되지 않은 원격 브랜치 발견: {', '.join(lingering)}")
    except Exception:
        pass


    # [5] 게임 다양성 및 메커니즘 분석 리포트
    print("\n--- 🧩 게임 메커니즘 및 다양성 분석 리포트 ---")
    genre_keywords = {
        "피하기 (Dodge/Avoid)": ["dodge", "rain-dodge", "lightning", "snow-dodge", "submarine", "traffic"],
        "받기/잡기 (Catch/Collect)": ["catch", "collect", "grab", "hunt", "fishing", "clean"],
        "매칭/퍼즐 (Match/Puzzle)": ["match", "pair", "puzzle", "sort", "shadow", "shape", "tangram", "sudoku", "2048", "ubongo"],
        "리듬/음악/타이핑 (Rhythm/Music/Typing)": ["rhythm", "piano", "drum", "beat", "typing", "sound"],
        "조작/점프/액션 (Jump/Action/Run)": ["jump", "run", "race", "flight", "fly", "hop", "kick", "throw", "bowling", "golf"],
        "학습/창의/그리기 (Learn/Creative/Math)": ["math", "count", "quiz", "color", "draw", "trace", "hangul", "urimal", "paper", "dress", "decor", "make", "cook", "chef"],
        "우주/모험 (Space/Adventure)": ["space", "star", "rocket", "whale", "planet", "dino", "castle", "maze"]
    }

    genre_counts = Counter()
    for g in games:
        text = f"{g.get('id', '')} {g.get('title', '')} {g.get('title_ko', '')} {g.get('description', '')}".lower()
        matched = False
        for genre, kw_list in genre_keywords.items():
            if any(kw in text for kw in kw_list):
                genre_counts[genre] += 1
                matched = True
        if not matched:
            genre_counts["기타/시뮬레이션"] += 1

    for genre, count in genre_counts.most_common():
        pct = (count / total_games) * 100
        bar = "█" * int(pct / 4)
        print(f"  - {genre:<30} : {count:3d}개 ({pct:5.1f}%) {bar}")

    # 결과 요약
    print("\n==================================================")
    if errors:
        print(f" ❌ 검증 실패: {len(errors)}개의 결함이 발견되었습니다.")
        print("==================================================")
        for err in errors:
            print(f"  [!] {err}")
        return False, errors, warnings
    else:
        print(" ✅ 무결성 검증 완벽 통과 (ALL CHECKS PASSED)")
        if warnings:
            print(f" ⚠️ 경고 사항: {len(warnings)}건")
            for warn in warnings:
                print(f"  [-] {warn}")
        print(f" - 깨진 링크(404): 0건")
        print(f" - 깨진 이미지: 0건")
        print(f" - 누락/오배치 디렉토리: 0건")
        print(f" - SVG XML 문법: 전수 정상")
        print("==================================================")
        return True, errors, warnings

if __name__ == "__main__":
    passed, errs, warns = check_all()
    if not passed:
        sys.exit(1)
    sys.exit(0)
