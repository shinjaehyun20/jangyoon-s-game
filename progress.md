Original prompt: https://shinjaehyun20.github.io/jangyoon-s-game/ 여기 디렉토리에, 테트리스 게임, 모바일로 실행하면, 키가 안나와. 해당 프로젝트 확인하고 수정하자.

- 2026-04-18: Cloned `shinjaehyun20/jangyoon-s-game` into `projects/active/jangyoon-s-game`.
- 2026-04-18: Confirmed `tetris/index.html` only supports keyboard input; no mobile touch controls are implemented yet.
- 2026-04-18: User clarified target is `tetris_javascript`; confirmed it also only supports keyboard input and patched `tetris_javascript/index.html` with on-screen touch controls and touch bindings.
- 2026-04-18: Added mobile-only `홈으로` links to each game detail page (`2048`, `runner-game`, `space-catcher`, `sudoku`, `tetris`, `tetris_javascript`, `typing`) pointing back to `../index.html`.
- 2026-04-18: Applied broader mobile polish pass:
- home grid becomes 1-column at <= 480px
- `space-catcher` and `runner-game` touch controls enlarged and viewport-height adjusted with `svh`
- `typing` now uses fluid width, `100dvh`, and iOS zoom-safe input sizing
- `tetris` and `tetris_javascript` now support swipe gestures and touch-based start binding in addition to on-screen controls
- TODO: Verify the new mobile controls and footer home links in an actual mobile viewport/browser.

- 2026-04-19: Added `ubongo/` — 폴리오미노 속도 퍼즐 게임 (9라운드, Easy/Hard, 60개 사전 검증 퍼즐 뱅크, ResizeObserver 기반 캔버스 안정화).
- 2026-04-19: Unified thumbnails across all 7 games — common design system (320×180, bottom-right title, 1px inner border) while preserving each game's color/motif.
- 2026-04-19: Refactored root listing page (`index.html` / `script.js` / `styles.css`) — semantic HTML, ARIA attributes, skeleton loader, external link badges, `100dvh`, `prefers-reduced-motion` support.
- 2026-04-19: Removed duplicate `tetris_javascript/` folder (identical to `tetris/` except `.github` and `LICENSE`, and not referenced in `games.json`). Preserved the original MIT `LICENSE` (Jake Gordon, 2011-2016) by moving it to `tetris/LICENSE`.
- 2026-04-19: Refactored custom game scripts (`space-catcher`, `runner-game`, `typing`) — CONFIG constants, IIFE wrapper, state objects, helper functions. Logic preserved 100%.
- 2026-04-19: Fixed runner-game bug — broken emoji character (`�`) in end-game message → 🏁.
- 2026-04-19: Updated `games.json` thumbnail paths: `tetris/texture.jpg` → `tetris/thumb.svg`, `2048/favicon.ico` → `2048/thumb.svg`.
