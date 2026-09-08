#!/usr/bin/env python3
"""
GitHub Polish & Synchronization Script for jangyoon-s-game (248 Games SSOT)
"""
import os
import re
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GAMES_JSON = REPO_ROOT / "games.json"
MENU_JSON = REPO_ROOT / "menu.json"
README_MD = REPO_ROOT / "README.md"
INDEX_HTML = REPO_ROOT / "index.html"
GITHUB_ABOUT = REPO_ROOT / "docs" / "github-about.md"
HERO_SVG = REPO_ROOT / "docs" / "assets" / "portfolio-hero.svg"
CHANGES_MD = REPO_ROOT / "CHANGES.md"

# Categorization mapping for missing games
MISSING_ROWS = [
    ("| [🚀 250호 기념 우주 별자리 레인저 (space-constellation-ranger)](./space-constellation-ranger) | 반짝이는 은하계 밤하늘을 우주선으로 비행하며 250개의 별빛 크리스탈을 모으고 신비로운 12별자리를 완성하는 250회 기념 스페이스 어드벤처 놀이 | 어린이/탐험·우주 |", "space-constellation-ranger"),
    ("| [🧋 버블티 펄 퐁퐁 (bubble-tea-pop)](./bubble-tea-pop) | 화면 아래에서 퐁퐁 떠오르는 달콤한 타피오카 펄과 과일 젤리를 쏙 터치해 컵에 담아 맛있는 무지개 버블티를 완성하는 힐링 터치 놀이 | 어린이/반응·터치 |", "bubble-tea-pop"),
    ("| [🫧 반짝반짝 심해 잠수함 탐험 (twinkle-deepsea-submarine)](./twinkle-deepsea-submarine) | 신비로운 심해 바닷속을 노란 잠수함으로 유영하며 해파리와 산호초를 피해 진주조개와 황금 보물상자를 모으는 힐링 수중 탐험 놀이 | 어린이/탐험·수중 |", "twinkle-deepsea-submarine"),
    ("| [🍮 말랑말랑 젤리 트램펄린 (sweet-jelly-trampoline)](./sweet-jelly-trampoline) | 말랑말랑 통통 튀는 무지개 푸딩 젤리 트램펄린을 좌우로 움직여 아기 곰 인형과 별사탕을 높이높이 튕겨 올리는 경쾌한 터치 바운스 놀이 | 어린이/액션·바운스 |", "sweet-jelly-trampoline"),
    ("| [✨ 우주 별자리 잇기 탐험 (cosmic-star-weaver)](./cosmic-star-weaver) | 반짝이는 우주 공간에서 별들을 선으로 이어 신비로운 별자리를 완성하는 공간 지각 놀이 | 어린이/공간·별자리 |", "cosmic-star-weaver"),
    ("| [🐧 오로라 펭귄의 눈썰매 슬라이드 (aurora-penguin-slide)](./aurora-penguin-slide) | 오로라 밤하늘 아래 빙판길을 미끄러지며 물고기를 모으고 얼음 바위를 피하는 스피드 슬라이드 놀이 | 어린이/액션·슬라이드 |", "aurora-penguin-slide"),
    ("| [🔮 반짝반짝 마법 수정 동굴 탐험 (magic-crystal-cave)](./magic-crystal-cave) | 신비로운 보석 동굴에서 쏟아지는 크리스탈을 마법 카트로 받아내고 무지개 프리즘 파워를 발동하는 힐링 아케이드 놀이 | 어린이/액션·캐치 |", "magic-crystal-cave"),
    ("| [🌈 알록달록 무지개 비눗방울 팡팡 (rainbow-bubble-popper)](./rainbow-bubble-popper) | 화면 가득 떠오르는 영롱한 무지개 비눗방울과 보석·과일을 퐁퐁 터뜨려 신나는 콤보와 점수를 모으는 힐링 터치 놀이 | 어린이/반응·터치 |", "rainbow-bubble-popper"),
    ("| [🔔 멜로디 크리스탈 차임 (melody-crystal-chime)](./melody-crystal-chime) | 5가지 영롱한 펜타토닉 크리스탈 차임벨을 터치해 맑은 멜로디를 연주하는 리듬 액션 놀이 | 어린이/음악·리듬 |", "melody-crystal-chime"),
    ("| [🚀 우주 운석 대시 (cosmic-meteor-dash)](./cosmic-meteor-dash) | 쏟아지는 불타는 운석을 피하며 별 보석과 보호막을 수집하는 스릴 만점 우주선 비행 회피 놀이 | 어린이/액션·회피 |", "cosmic-meteor-dash"),
    ("| [⚡ 꼬마 로봇 건전지 충전 (circuit-robot-battery)](./circuit-robot-battery) | 번개와 건전지 패턴을 탭하여 아기 로봇의 에너지를 충전하는 인지 퍼즐 놀이 | 어린이/퍼즐·인지 |", "circuit-robot-battery"),
    ("| [🎈 무지개 풍선 팡팡 (balloon-rainbow-pop)](./balloon-rainbow-pop) | 하늘로 떠오르는 무지개 풍선을 터치하고 별 풍선 연쇄 폭발을 일으키는 터치 액션 놀이 | 어린이/반응·터치 |", "balloon-rainbow-pop"),
    ("| [🥐 우주 별빛 베이커리 (cosmic-star-baker)](./cosmic-star-baker) | 우주 성운 반죽과 별빛 토핑으로 외계인 손님들이 주문한 신비한 빵을 굽는 베이킹 놀이 | 어린이/창의·요리 |", "cosmic-star-baker"),
    ("| [🐢 바다거북 비눗방울 구출 (turtle-bubble-rescue)](./turtle-bubble-rescue) | 그물에 갇힌 바다거북과 해양 생물들을 거품 방울로 터치해 구출해 주는 바다 환경 구조 놀이 | 어린이/액션·구출 |", "turtle-bubble-rescue"),
    ("| [🚁 사이버 드론 택배 비행사 (cyber-drone-delivery)](./cyber-drone-delivery) | 메가시티의 강풍과 회전 레이저를 뚫고 드론의 양쪽 로터와 부스터를 제어해 지정된 헬리패드에 안전하게 화물을 배송하는 조종 놀이 | 어린이/조종·물리 |", "cyber-drone-delivery"),
    ("| [⛏️ 픽셀 던전 광산 탐험가 (pixel-dungeon-miner)](./pixel-dungeon-miner) | 미지의 지하 동굴을 파고 내려가 진귀한 광석을 채굴하고 산소를 관리하며 장비를 업그레이드하는 탐험 놀이 | 어린이/탐험·채굴 |", "pixel-dungeon-miner"),
    ("| [🧲 중력 구슬 건축가 (gravity-ball-architect)](./gravity-ball-architect) | 중력과 반동 발판을 배치하여 굴러가는 쇠구슬을 목표 지점까지 안내하는 물리 퍼즐 놀이 | 어린이/물리·퍼즐 |", "gravity-ball-architect"),
    ("| [🥁 쿵치딱 리듬 버블 밴드 (beat-bubble-drummer)](./beat-bubble-drummer) | 리듬에 맞춰 떨어지는 음표 버블을 타이밍 맞추어 두드려 연주하는 경쾌한 드럼 놀이 | 어린이/음악·리듬 |", "beat-bubble-drummer"),
    ("| [🐳 아기별고래 우주 유영 (star-whale-voyage)](./star-whale-voyage) | 우주 바다를 헤엄치며 성운과 별가루를 먹고 몸집을 키워나가는 평화로운 비행 힐링 놀이 | 어린이/액션·비행 |", "star-whale-voyage"),
    ("| [🧪 숲속 마법 물약방 (potion-magic-shop)](./potion-magic-shop) | 신비로운 약초와 반짝이는 가루를 조합해 동물 친구들의 고민을 해결하는 마법 제작 놀이 | 어린이/학습·제작 |", "potion-magic-shop"),
    ("| [🌱 루미 이슬정원 (lumi-dew-garden)](./lumi-dew-garden) | 이슬 요정 루미와 함께 새싹에 영롱한 이슬방울을 맺어 예쁜 꽃을 피우는 자연 힐링 놀이 | 어린이/생활·힐링 |", "lumi-dew-garden"),
    ("| [🪵 숲속 구슬길 (woodland-marble-slide)](./woodland-marble-slide) | 나무 레일과 물레방아를 조립해 숲속 다람쥐들에게 도토리 구슬을 배달하는 물리 퍼즐 놀이 | 어린이/물리·퍼즐 |", "woodland-marble-slide"),
]

def polish_github_about(total_games):
    count_str = str(total_games)
    content = f"""# GitHub About

- **Description:** 터치로 바로 즐기는 {count_str}개 어린이 미니게임 아케이드 — 학습, 액션, 퍼즐, 창의 놀이.
- **Homepage:** https://shinjaehyun20.github.io/jangyoon-s-game/
- **Topics:** `kids-games`, `educational-games`, `html5-games`, `javascript`, `game-library`, `mobile-first`, `github-pages`, `korean`
"""
    GITHUB_ABOUT.write_text(content, encoding="utf-8")
    print(f"[*] docs/github-about.md 동기화 완료 ({count_str}개)")

def polish_changes_md(total_games):
    txt = CHANGES_MD.read_text(encoding="utf-8")
    new_entries = f"""## 2026-09-09 — bubble-tea-pop, space-constellation-ranger (총 250개)
- **[🧋 버블티 펄 퐁퐁 (bubble-tea-pop)]** — 화면 아래에서 떠오르는 달콤한 타피오카 펄과 과일 젤리를 쏙 터치해 컵에 담아 맛있는 버블티를 완성하는 힐링 터치 놀이 (외부 의존성 0).
- **[🚀 250호 기념 우주 별자리 레인저 (space-constellation-ranger)]** — 우주선으로 밤하늘을 비행하며 250개 별빛 크리스탈을 모으고 12별자리를 완성하는 250회 기념 스페이스 어드벤처 놀이 (외부 의존성 0).

## 2026-09-08 — sweet-jelly-trampoline, twinkle-deepsea-submarine (총 248개)
- **[🍮 말랑말랑 젤리 트램펄린 (sweet-jelly-trampoline)]** — 푸딩 젤리 트램펄린으로 아기 곰 인형과 별사탕을 튕겨 올리는 경쾌한 터치 바운스 놀이 (외부 의존성 0).
- **[🫧 반짝반짝 심해 잠수함 탐험 (twinkle-deepsea-submarine)]** — 노란 잠수함으로 심해를 유영하며 진주조개와 보물상자를 모으는 힐링 수중 탐험 놀이 (외부 의존성 0).

## 2026-09-06 — aurora-penguin-slide, cosmic-star-weaver (총 246개)
- **[🐧 오로라 펭귄의 눈썰매 슬라이드 (aurora-penguin-slide)]** — 오로라 밤하늘 빙판길을 미끄러지며 물고기를 모으고 얼음 바위를 피하는 스피드 슬라이드 놀이 (외부 의존성 0).
- **[✨ 우주 별자리 잇기 탐험 (cosmic-star-weaver)]** — 우주 공간에서 별들을 선으로 이어 신비로운 별자리를 완성하는 공간 지각 놀이 (외부 의존성 0).

## 2026-09-05 — rainbow-bubble-popper, magic-crystal-cave (총 244개)
- **[🌈 알록달록 무지개 비눗방울 팡팡 (rainbow-bubble-popper)]** — 떠오르는 무지개 비눗방울과 보석·과일을 터뜨려 콤보와 점수를 모으는 힐링 터치 놀이 (외부 의존성 0).
- **[🔮 반짝반짝 마법 수정 동굴 탐험 (magic-crystal-cave)]** — 보석 동굴에서 쏟아지는 크리스탈을 마법 카트로 받아내고 프리즘 파워를 발동하는 아케이드 놀이 (외부 의존성 0).

## 2026-09-03 — starlight-whale-flight, forest-acorn-catapult (총 242개)
- **[🐳 별빛 고래의 하늘 비행 (starlight-whale-flight)]** — 은하수 밤하늘을 헤엄치며 반짝이는 별빛을 모으는 비행 놀이 (외부 의존성 0).
- **[🐿️ 도토리 퐁퐁 발사기 (forest-acorn-catapult)]** — 다람쥐 도토리를 당겨서 나뭇잎 바구니에 골인시키는 물리 조준 놀이 (외부 의존성 0).

## 2026-09-02 — sparkle-firefly-lamp, rainbow-gem-minecart (총 240개)
- **[✨ 반짝반짝 반딧불이 호롱불 (sparkle-firefly-lamp)]** — 밤하늘 반딧불이를 터치해 호롱불을 밝히는 힐링 터치 놀이 (외부 의존성 0).
- **[💎 무지개 보석 광산 열차 (rainbow-gem-minecart)]** — 쏟아지는 오색 보석을 광차로 쏙쏙 담는 레일 액션 게임 (외부 의존성 0).

"""
    if "bubble-tea-pop" not in txt:
        txt = new_entries + txt
        print("[*] CHANGES.md 2026-09-09 신규 게임 이력 추가 완료")

    # 2026-08-28 추가 누락 보완
    aug28_entry = """## 2026-08-28 — turtle-bubble-rescue, cosmic-star-baker (총 232개)
- **[🐢 바다거북 비눗방울 구출 (turtle-bubble-rescue)]** — 그물에 갇힌 바다거북과 해양 생물들을 비눗방울로 구출하는 바다 환경 구조 놀이 (외부 의존성 0).
- **[🥐 우주 별빛 베이커리 (cosmic-star-baker)]** — 성운 반죽과 별빛 토핑으로 외계인 손님들의 주문 빵을 굽는 우주 베이킹 놀이 (외부 의존성 0).

"""
    if "turtle-bubble-rescue" not in txt and "## 2026-08-27" in txt:
        txt = txt.replace("## 2026-08-27", aug28_entry + "## 2026-08-27", 1)
        print("[*] CHANGES.md 2026-08-28 이력 보완 완료")

    CHANGES_MD.write_text(txt, encoding="utf-8")

def polish_readme(total_games):
    count_str = str(total_games)
    txt = README_MD.read_text(encoding="utf-8")

    # 1. 상단 배지 및 헤더 카운터 동기화
    txt = re.sub(r'badge/games-\d+-6C5CE7', f'badge/games-{count_str}-6C5CE7', txt)
    txt = re.sub(r'어린이 미니게임 \d+개', f'어린이 미니게임 {count_str}개', txt)
    txt = re.sub(r'\[!\[\d+개의 게임을', f'[![{count_str}개의 게임을', txt)
    txt = re.sub(r'전체 \d+개 게임 목록', f'전체 {count_str}개 게임 목록', txt)
    txt = re.sub(r'games\.json 실측 \d+개', f'games.json 실측 {count_str}개', txt)

    # 2. 게임 표 전체 248개 동기화
    table_match = re.search(r'(<details>\s*<summary><strong>전체 \d+개 게임 목록 펼치기</strong></summary>\s*\| 게임 \| 설명 \| 카테고리 \|\s*\|---\|---\|---\|\s*)(.*?)(</details>)', txt, re.DOTALL)
    if not table_match:
        raise ValueError("README.md 내 게임 목록 details 표를 찾을 수 없습니다.")

    header_part = f"<details>\n<summary><strong>전체 {count_str}개 게임 목록 펼치기</strong></summary>\n\n\n| 게임 | 설명 | 카테고리 |\n|---|---|---|\n"
    current_body = table_match.group(2).strip()
    footer_part = "\n</details>"

    existing_rows = [l.strip() for l in current_body.splitlines() if l.strip().startswith('| [')]
    
    rows_to_prepend = []
    for row_str, gid in MISSING_ROWS:
        if not any(f"({gid})" in r or f"./{gid}" in r for r in existing_rows):
            rows_to_prepend.append(row_str)

    all_rows = rows_to_prepend + existing_rows
    print(f"[*] 게임 목록 표 재구성: {len(all_rows)}개 행 (누락 추가: {len(rows_to_prepend)}개)")

    new_table_block = header_part + "\n".join(all_rows) + footer_part
    txt = txt[:table_match.start()] + new_table_block + txt[table_match.end():]

    # 3. 최근 변경사항 중복 및 오염 제거 / 재정렬
    tech_split = re.split(r'## 최근 변경사항 \(\d+-\d+\)', txt)
    if len(tech_split) > 1:
        base_pre = tech_split[0]
        clean_changes = f"""## 최근 변경사항 (2026-09)

- **🧋 버블티 펄 퐁퐁 · 🚀 250호 기념 우주 별자리 레인저 추가 (2026-09-09)** — 타피오카 펄 버블티 제조 힐링 터치 놀이와 250회 기념 우주 별자리 완성 스페이스 어드벤처 미니게임 2종 추가 (총 250개 대기록 달성). 단일 HTML, 외부 CDN 의존성 없음, Web Audio 효과음, Pointer Events 최적화.
- **🍮 말랑말랑 젤리 트램펄린 · 🫧 반짝반짝 심해 잠수함 탐험 추가 (2026-09-08)** — 푸딩 젤리 트램펄린 바운스 놀이와 심해 잠수함 유영 탐험 미니게임 2종 추가 (총 248개). 단일 HTML, 외부 CDN 의존성 없음, Web Audio 효과음, 터치 반응형 최적화.
- **🐧 오로라 펭귄의 눈썰매 슬라이드 · ✨ 우주 별자리 잇기 탐험 추가 (2026-09-06)** — 오로라 빙판길을 미끄러지는 스피드 슬라이드와 우주 별들을 선으로 잇는 별자리 지각 미니게임 2종 추가 (총 246개). 단일 HTML, 외부 의존성 없음, Pointer Events 통합 조작.
- **🌈 알록달록 무지개 비눗방울 팡팡 · 🔮 반짝반짝 마법 수정 동굴 탐험 추가 (2026-09-05)** — 화면 가득 떠오르는 비눗방울 터치 놀이와 보석 카트 수집 아케이드 미니게임 2종 추가 (총 244개). 단일 HTML, 외부 의존성 없음.
- **🐳 별빛 고래의 하늘 비행 · 🐿️ 도토리 퐁퐁 발사기 추가 (2026-09-03)** — 은하수 밤하늘을 헤엄치는 비행 놀이와 다람쥐 도토리 물리 조준 골인 미니게임 2종 추가 (총 242개). 단일 HTML, 외부 의존성 없음.
- **✨ 반짝반짝 반딧불이 호롱불 · 💎 무지개 보석 광산 열차 추가 (2026-09-02)** — 밤하늘 반딧불이 힐링 터치 놀이와 쏟아지는 오색 보석 광차 레일 액션 미니게임 2종 추가 (총 240개). 단일 HTML, 외부 의존성 없음.
- **🌊 해저 진주 조개 찾기 · 🍪 아기 몬스터 쿠키 먹이기 추가 (2026-09-02)** — 조개 터치 진주 수집 액션과 쿠키 맞춤 드래그 수집 미니게임 2종 추가 (총 238개). 단일 HTML, 외부 의존성 없음.

## 최근 변경사항 (2026-08)

- **🚀 우주 운석 대시 · 🔔 멜로디 크리스탈 차임 추가 (2026-08-31)** — 불타는 운석을 피하는 우주선 비행 회피 놀이와 5가지 영롱한 크리스탈 차임벨 리듬 액션 미니게임 2종 추가 (총 236개). 단일 HTML, 외부 의존성 없음.
- **🎈 무지개 풍선 팡팡 · ⚡ 꼬마 로봇 건전지 충전 추가 (2026-08-30)** — 무지개 풍선 연쇄 폭발 터치 놀이와 번개/건전지 패턴 매칭 인지 퍼즐 미니게임 2종 추가 (총 234개). 단일 HTML, 외부 의존성 없음.
- **🐢 바다거북 비눗방울 구출 · 🥐 우주 별빛 베이커리 추가 (2026-08-28)** — 해양 생물 비눗방울 구출 놀이와 성운 반죽/별빛 토핑 우주 베이킹 미니게임 2종 추가 (총 232개). 단일 HTML, 외부 의존성 없음.
- **⚡ 네온 회로 연결사 · 🐒 정글 덩굴 스윙 타잔 추가 (2026-08-27)** — 터치 회전으로 ⚡발전소에서 🤖로봇까지 전선을 잇는 네온 회로 퍼즐과 진자 물리 반동으로 시원하게 날아가는 정글 스윙 액션 미니게임 2종 추가. 단일 HTML, 외부 CDN 의존성 없음, 100dvh/overflow 보호, Pointer Events 통합 조작.
- **소방차 불 끄기 · 공룡 뼈 발굴 추가 (2026-08-11)** — 7살 장윤이가 직관적으로 즐길 수 있는 불 끄기 터치 반응 게임과 공룡 뼈 발굴 탐험 게임 추가. 단일 HTML, 외부 의존성 없음, Pointer Events 통합 조작.
- **🥁 동물 밴드 연주 · 🍂 계절 옷장 분류 추가 (2026-08-09)** — 동물 밴드 연주는 4가지 악기(북·트라이앵글·실로폰·탬버린)가 켜지는 순서를 기억하고 똑같이 눌러 라운드를 이어가는 순서 기억 게임으로, 라운드마다 순서가 하나씩 늘어납니다. 계절 옷장 분류는 옷과 물건을 봄·여름·가을·겨울 4칸 중 알맞은 계절 칸으로 드래그해 40초 동안 최대한 많이 분류하는 인지 게임입니다. 두 게임 모두 단일 HTML, Pointer Events, 100dvh/overflow 보호, 시작·종료 오버레이, 홈 링크, localStorage 최고기록, SVG 썸네일, 외부 의존성 0건을 포함합니다. 부수 발견: `hidden-object-hunt`·`rhythm-touch-beat`(2026-08-07 배포)가 README 최근 변경사항 및 CHANGES.md에 미반영 상태였습니다 — `KNOWN_ISSUES.md` 참조.
- **🚲 자전거 균형 타기 · 🧊 냉장고 정리하기 추가 (2026-08-04)** — 자전거 균형 타기는 화면 드래그로 균형 마커를 초록 구역에 맞추고 페달 버튼을 연타해 앞으로 나아가는 실시간 균형 유지 게임으로, 기존 balance-tower(정적 블록 쌓기)·stone-balance-walk(교차 버튼 균형)와 달리 지속적으로 표류하는 균형점을 계속 재조정해야 하는 실시간 밸런스가 핵심입니다. 냉장고 정리하기는 음식 아이템을 냉장·냉동·실온 3칸에 드래그로 분류하는 생활 인지 게임으로, 기존 recycle-rescue(재질 분류)·laundry-sort(색깔 분류)와 달리 "보관 온도" 판단 기준과 아무 칸에나 치우면 되는 상한 음식 등장이 차별점입니다. 두 게임 모두 단일 HTML, Pointer Events, 100dvh/overflow 보호, 시작·종료 오버레이, 홈 링크, localStorage 최고기록, SVG 썸네일, 외부 의존성 0건을 포함합니다. 부수 발견: README "최근 변경사항 (2026-08)" 섹션에 2026-08-03 rocket-sequence-launch·shadow-trail-match 추가 항목이 누락돼 있어 함께 보완했습니다.
- **🚀 로켓 순서 발사 · 🐾 그림자 발자국 탐정 추가 (2026-08-03)** — 로켓 순서 발사는 관제사가 보여주는 그림 명령(⛽/⭐/🌙/🌱) 순서를 기억하고 같은 순서로 눌러 6라운드 로켓을 발사하는 순서 기억 게임으로, 오답 시 감점 후 같은 패턴을 다시 보여주는 별 기록을 저장합니다. 그림자 발자국 탐정은 발자국 단서와 흐릿한 동물 그림자를 보고 4개 보기 중 정답 동물을 고르는 8라운드 관찰 놀이로, 연속 정답 보너스와 최고점을 저장합니다. 두 게임 모두 단일 HTML, 외부 의존성 없음, 모바일 터치 우선, 시작·종료 오버레이, 홈 링크, SVG 썸네일을 포함합니다.
- **📄 종이 접기 연구소 · 🔦 거울빛 구조대 추가 및 미로 탈출 드래그 수정 (2026-08-01)** — 종이 접기 연구소는 접기 순서에 따른 좌표 변환을 예측해 4개·8개 대칭 무늬를 만드는 6라운드 퍼즐이고, 거울빛 구조대는 거울을 직접 드래그해 반사광을 별까지 잇는 7라운드 공간 추론 게임입니다. 미로 탈출은 공을 누르지 않은 드래그를 무시하고 포인터 이동량을 연속적으로 따라가며, 닫힌 벽에서는 시작점으로 되돌아가지 않고 공 반지름을 고려한 벽 경계에 멈추도록 수정했습니다. 레벨 전환·pointer cancel에서는 드래그 상태를 안전하게 종료합니다. 카탈로그는 `games.json` 실측 200개로 동기화했습니다.

"""
        m_july = re.search(r'## 최근 변경사항 \(2026-07\)', txt)
        if m_july:
            rest_content = txt[m_july.start():]
            # 2026-06 뒤에 낀 중복 제거
            rest_content = re.sub(r'## 최근 변경사항 \(2026-09\)\s*- \*\*🍮 말랑말랑 젤리.*?(\n- \*\*달팽이 경주)', r'\1', rest_content, flags=re.DOTALL)
            # 2026-06과 2026-05 사이에 낀 중복 2026-07 제거
            rest_content = re.sub(r'\n## 최근 변경사항 \(2026-07\)\s*- \*\*🍀 네잎클로버.*?(\n## 최근 변경사항 \(2026-05\))', r'\1', rest_content, flags=re.DOTALL)
            rest_content = re.sub(r'## 최근 변경사항 \(2026-05\)\s*## 최근 변경사항 \(2026-09\)\s*- \*\*🍮 말랑말랑 젤리.*?(\n- \*\*동물원 탈출)', r'## 최근 변경사항 (2026-05)\n\1', rest_content, flags=re.DOTALL)
            rest_content = re.sub(r'## 최근 변경사항 \(2026-04\)\s*## 최근 변경사항 \(2026-09\)\s*- \*\*🍮 말랑말랑 젤리.*?(\n- \*\*색칠 놀이)', r'## 최근 변경사항 (2026-04)\n\1', rest_content, flags=re.DOTALL)
            rest_content = re.sub(r'\n+- 2026-08-28: `turtle-bubble-rescue`, `cosmic-star-baker` 추가됨\s*$', '\n', rest_content)
            rest_content = re.sub(r'\n+- 2026-08-28: turtle-bubble-rescue, cosmic-star-baker 추가됨\s*$', '\n', rest_content)

            txt = base_pre + clean_changes + rest_content
            print("[*] README.md 최근 변경사항 중복 정화 및 2026-09/2026-08 구조화 완료")

    README_MD.write_text(txt, encoding="utf-8")
    print(f"[*] README.md 전체 저장 완료 ({count_str}개)")

def polish_hero_svg(total_games):
    count_str = str(total_games)
    if HERO_SVG.exists():
        svg = HERO_SVG.read_text(encoding="utf-8")
        svg = re.sub(r'\d+개 어린이용', f'{count_str}개 어린이용', svg)
        svg = re.sub(r'시작하는 \d+개의', f'시작하는 {count_str}개의', svg)
        svg = re.sub(r'>\d+</text>', f'>{count_str}</text>', svg)
        HERO_SVG.write_text(svg, encoding="utf-8")
        print(f"[*] portfolio-hero.svg 카운터 확인/동기화 완료 ({count_str}개)")

def polish_index_html(total_games):
    count_str = str(total_games)
    if INDEX_HTML.exists():
        html = INDEX_HTML.read_text(encoding="utf-8")
        html = re.sub(r'content="장윤이를 위한 게임 모음[^"]*"', f'content="장윤이를 위한 게임 모음 - 총 {count_str}개의 타이핑, 퍼즐, 액션 게임을 한 곳에서"', html)
        INDEX_HTML.write_text(html, encoding="utf-8")
        print(f"[*] index.html 메타 설명 동기화 완료 ({count_str}개)")

def sync_gh_cli(total_games):
    count_str = str(total_games)
    desc = f"터치로 바로 즐기는 {count_str}개 어린이 미니게임 아케이드 — 학습, 액션, 퍼즐, 창의 놀이."
    try:
        res = subprocess.run(
            ["gh", "repo", "edit", "shinjaehyun20/jangyoon-s-game", "--description", desc],
            capture_output=True, text=True, check=False
        )
        if res.returncode == 0:
            print(f"[*] GitHub repo description 업데이트 성공: {desc}")
        else:
            print(f"[-] gh repo edit notice: {res.stderr.strip() or res.stdout.strip()}")
    except Exception as e:
        print(f"[-] gh repo edit 실행 실패: {e}")

def main():
    print("==================================================")
    print(" 🚀 jangyoon-s-game GitHub Polishing Pass 시작")
    print("==================================================")
    with open(GAMES_JSON, "r", encoding="utf-8") as f:
        games = json.load(f)
    total_games = len(games)
    print(f"[*] SSOT 기준 총 게임 수: {total_games}개")

    polish_github_about(total_games)
    polish_changes_md(total_games)
    polish_readme(total_games)
    polish_hero_svg(total_games)
    polish_index_html(total_games)
    sync_gh_cli(total_games)

    print("\n==================================================")
    print(" ✅ GitHub Polishing Pass 완료")
    print("==================================================")

if __name__ == "__main__":
    main()
