# AGENTS.md — jangyoon-s-game

## 정의
장윤이를 위한 웹 기반 미니게임 모음(100+ 게임). 순수 HTML/CSS/JS, 외부 의존성 없이 GitHub Pages(`shinjaehyun20.github.io/jangyoon-s-game`)에서 동작. [SOURCE: README.md:1-5]

## 정본 경로
`D:\workspace\projects\active\jangyoon-s-game`

## Write Boundary
- 신규 게임은 루트에 독립 폴더 + `games.json`/`menu.json` 항목 추가 규약 준수(README §"새 게임 추가하는 법"). 커밋&푸시로 GitHub Pages 자동 배포.
- 폴리싱 전용 파생 작업면은 `github-polish/jangyoon-s-game/`(nested clone) — 그쪽에서 먼저 검증 후 이 정본에 반영.

## 커밋·푸시 순서 (필수 — 위반 시 CI 실패)
아침 자동 생성이 게임 폴더를 메타데이터보다 먼저 푸시해 `Game Arcade Integrity Check`가 반복 실패했다
(2449f7d: 미등록 게임 폴더 / 92076f2: 7대 문서 카운터 미동기화). 아래 순서를 지킨다.

1. 게임 폴더 작성 (`<slug>/index.html`, `thumb.svg`)
2. `games.json` 등록 + `menu.json` 항목 추가 — description은 한국어 지시문(필수)
3. `python scripts/sync_metadata.py` — menu/README/docs/index.html/portfolio-hero.svg/CHANGES.md 7대 동기화
4. `python -m unittest discover -s scripts -p 'test_*.py'` 또는 `python scripts/verify_integrity.py`
5. **4까지 통과한 뒤** 커밋 → `main`·`master` 동시 푸시

- 한 번에 처리: `python scripts/morning_publish.py --message "feat(morning): add <slug> with 7-point sync" [--wait-ci]`
  (1~5를 순서대로 실행하고, 검증 실패 시 커밋·푸시를 아예 하지 않는다. `--dry-run`은 검증만)
- **금지**: 게임 폴더만 담은 커밋을 먼저 푸시한 뒤 메타데이터를 다음 커밋에서 맞추는 2단 푸시.
- 푸시 가드: `git config core.hooksPath .githooks`로 `.githooks/pre-push`를 걸면 커밋된 HEAD가
  무결성 검증을 통과하지 못할 때 `git push` 자체가 중단된다(우회는 `--no-verify`, 권장하지 않음).
- 배포/CI: `.github/workflows/integrity-check.yml` — `verify`(unittest + verify_integrity) 통과 시에만
  GitHub Pages `deploy`가 실행된다. `main`·`master` 두 브랜치 모두 검증 대상이며 내용은 동일하게 유지한다.

## Cross-Runtime 계약
- 전 런타임 공유 계약: `D:\workspace\runtime\registry\CROSS-RUNTIME-OPERATING-CONTRACT.md`
- Artifact-Split(§3.1) 준수.

## 소유 런타임
`claude` [SOURCE: runtime/registry/project-context-index.json — jangyoon-s-game last_known_runtime_activity]
