# Jangyoon's Game Collection

> HTML/CSS/JavaScript로 만든 어린이용 브라우저 미니게임 컬렉션입니다.
>
> A child-friendly browser mini-game collection built with plain HTML, CSS, and JavaScript.

[![Static Site](https://img.shields.io/badge/site-GitHub%20Pages-2ea44f)](https://shinjaehyun20.github.io/jangyoon-s-game/) [![No Framework](https://img.shields.io/badge/frontend-vanilla%20JS-f7df1e)](#technology) [![Games](https://img.shields.io/badge/games-146-7c3aed)](./docs/games-catalog.md)

## Why this exists

이 저장소는 아이가 바로 눌러보고 놀 수 있는 작은 웹 게임을 빠르게 만들고, 그 결과를 한 곳에서 실행·관리하기 위한 가족/학습형 프로젝트입니다. 각 게임은 독립 폴더로 분리되어 있고, 루트 페이지는 `games.json`과 `menu.json`을 읽어 전체 목록을 보여줍니다.

## Live demo

- **Play now:** <https://shinjaehyun20.github.io/jangyoon-s-game/>
- **Full catalog:** [docs/games-catalog.md](./docs/games-catalog.md)
- **Change log:** [CHANGES.md](./CHANGES.md)
- **Progress notes:** [progress.md](./progress.md)

## Highlights

| Game | English title | What it does |
|---|---|---|
| [🚒 소방차 출동](./firetruck-rescue/) | Firetruck Rescue | 불(🔥)을 탭하면 물줄기로 꺼져요! 라운드마다 빨라지는 불 끄기 도전 |
| [⭐ 별 잇기 숫자놀이](./star-trace-number/) | Star Trace Number | 1번부터 순서대로 별을 탭해 별자리를 완성! 1~10 숫자 학습 5단계 |
| [🌈 무지개 레일 공방](./rainbow-rail-builder/) | Rainbow Rail Workshop | 빈 판에 손가락으로 레일을 직접 그려 미션역을 순서대로 잇는 5레벨 드로잉 퍼즐 |
| [🌊 바다 청소부](./ocean-cleanup/) | Ocean Cleanup | 잠수함을 드래그해 바닷속 쓰레기를 모으고 물고기는 피하세요! 40초 환경 도전 |
| [🎂 케이크 꾸미기](./cake-decor/) | Cake Decor | 레시피대로 케이크에 크림·과일·초코를 올려 완성! 10가지 케이크 도전 |
| [🌙 달 로켓 연료 계산](./moon-rocket-math/) | Moon Rocket Math | 덧셈·뺄셈 정답 연료를 골라 로켓을 달까지 보내는 45초 숫자 게임 |
| [🤖 코덱스 로봇 연구소](./codex-robot-lab/) | Codex Robot Lab | 명령 카드를 순서대로 골라 계획→수정→검증→커밋/푸시 파이프라인을 완성해요! |
| [슈퍼 점프 모험](./super-mario/) | Super Jump Adventure | 5스테이지+보스 성 옆스크롤 플랫포머! 버섯·불꽃·별, 숨은 블록·파이프 비밀길, 숙이기·보스 도끼 |
| [장윤 한글 타이핑 (로컬)](./typing/) | Typing (로컬) | 한글 단어를 입력하는 타자 연습 게임 (로컬 실행) |
| [자바스크립트 테트리스](./tetris/) | Javascript Tetris | 클래식 테트리스 게임 (자바스크립트) |
| [2048 퍼즐](./2048/) | 2048 | 2048 숫자 퍼즐 게임 (오픈소스) |
| [스도쿠](./sudoku/) | Sudoku | 숫자 퍼즐 게임 - 난이도 선택, 타이머, Lives 시스템 포함 |

## Features

- **146 standalone mini-games** managed from one static site.
- **No app install required**: runs in a modern browser through GitHub Pages or a local static server.
- **Kid-friendly interactions**: tap, drag, swipe, simple keyboard controls, forgiving failure patterns.
- **Learning + play mix**: math, Hangul typing, memory, rhythm, sorting, puzzles, reflex games, and creative play.
- **Portable structure**: each game folder can be opened, tested, or improved independently.
- **Static-first architecture**: no backend, database, build step, or framework dependency for the main collection.

## Quick start

### Play online

Open the GitHub Pages site:

```text
https://shinjaehyun20.github.io/jangyoon-s-game/
```

### Run locally

Because the landing page loads `games.json` with `fetch`, use a local web server instead of opening `index.html` directly.

```bash
git clone https://github.com/shinjaehyun20/jangyoon-s-game.git
cd jangyoon-s-game
python3 -m http.server 8000
# open http://localhost:8000
```

On Windows, `python -m http.server 8000` works when Python is registered as `python`.

## Project structure

```text
jangyoon-s-game/
├── index.html                    # Collection landing page
├── script.js                     # Game grid/catalog rendering
├── styles.css                    # Landing page styles
├── games.json                    # Main game metadata used by the grid
├── menu.json                     # Sidebar/menu metadata
├── CHANGES.md                    # Detailed change history
├── progress.md                   # Working progress notes
├── docs/
│   ├── README.md                 # Documentation index
│   ├── games-catalog.md          # Generated readable catalog
│   └── publication-checklist.md  # Checklist for adding/publishing games
└── <game-id>/
    ├── index.html                # Standalone game entry
    ├── script.js                 # Game logic when split out
    ├── style.css                 # Game-specific style when split out
    └── thumb.svg                 # Catalog thumbnail when available
```

## Adding a new game

1. Create a new folder at the repository root, for example `new-game/`.
2. Add the game entry point, usually `new-game/index.html`.
3. Add a thumbnail, preferably `new-game/thumb.svg` with a 16:9 layout.
4. Add the game to `games.json`:

```json
{
  "id": "new-game",
  "title": "New Game",
  "title_ko": "새 게임",
  "description": "짧은 설명",
  "thumbnail": "new-game/thumb.svg",
  "path": "new-game/index.html"
}
```

5. Add or update the corresponding `menu.json` entry when the sidebar/menu should expose it.
6. Run the checks in [docs/publication-checklist.md](./docs/publication-checklist.md) before publishing.

## Technology

- HTML5
- CSS3
- JavaScript ES6+
- Canvas 2D / Pointer Events / Web Audio API where individual games need them
- `localStorage` for lightweight best-score records in selected games
- GitHub Pages for static hosting

## Roadmap

- Add screenshot/GIF evidence for representative games.
- Keep `docs/games-catalog.md` synchronized with `games.json`.
- Add lightweight mobile/touch smoke checks for recently added games.
- Group games by learning type and interaction type on the landing page.
- Add a small QA checklist per game folder for entry point, thumbnail, metadata, and mobile viewport.

## License

- Root landing page and selected custom games: MIT-style project use unless a game folder states otherwise.
- `tetris/`: MIT License from the original author; see `tetris/LICENSE`.
- Check individual game folders for any game-specific license notes.
