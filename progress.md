Original prompt: https://shinjaehyun20.github.io/jangyoon-s-game/ 여기 디렉토리에, 테트리스 게임, 모바일로 실행하면, 키가 안나와. 해당 프로젝트 확인하고 수정하자.

- 2026-04-18: Cloned `shinjaehyun20/jangyoon-s-game` into `projects/active/jangyoon-s-game`.
- 2026-04-18: Confirmed `tetris/index.html` only supports keyboard input; no mobile touch controls are implemented yet.
- 2026-04-18: User clarified target is `tetris_javascript`; confirmed it also only supports keyboard input and patched `tetris_javascript/index.html` with on-screen touch controls and touch bindings.
- 2026-04-18: Added mobile-only `홈으로` links to each game detail page (`2048`, `runner-game`, `space-catcher`, `sudoku`, `tetris`, `tetris_javascript`, `typing`) pointing back to `../index.html`.
- TODO: Verify the new mobile controls and footer home links in an actual mobile viewport/browser.
