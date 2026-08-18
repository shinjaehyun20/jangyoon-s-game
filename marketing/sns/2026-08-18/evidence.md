# SNS 홍보 실행 증거 — 2026-08-18

- **task_id:** `hermes-sns-20260818-jangyoon-game`
- **정본:** `../../README.md`, `../../docs/github-about.md`, 공개 배포본 `https://shinjaehyun20.github.io/jangyoon-s-game/`
- **현재 사실 검증:** 로컬 `games.json`, `origin/main:games.json`, GitHub raw `main/games.json`이 모두 **228개**. 공개 Pages 메뉴에서 최신 게임 반영을 확인.
- **원고 톤:** 바쁜 날에도 함께 놀고 싶은 마음으로 하루 두 개씩 만들기 시작해 228개가 되었다는 창작자 서사. 아동 이름·얼굴·개인정보는 사용하지 않음.

## 자산 QA

| 채널 | 자산 | 규격 | SHA-256 | 결과 |
|---|---|---:|---|---|
| X | `assets/x-card.png` | 1600×900 | `c1702232e2b3030ac93899fd509ce5fbebc3a40e7ec4f7035883438e46ebf67b` | PASS — 228 표기, 과거 171 노출 없음, 텍스트 겹침/잘림 없음 |
| Threads | `assets/threads-card.png` | 1200×675 | `37b58e4ee5b641acbc138f5b725d28b4001d28971bff504374322d644d1e419a` | PASS — 228 표기, 과거 171 노출 없음, 텍스트 겹침/잘림 없음 |
| Instagram | `assets/instagram-card.png` | 1080×1350 | `5b44f827ffd761e2efa7b089e90c193e0bd5ea88a02343d24bfa5d163d471fe1` | PASS — 228 표기, 아동 식별 정보 없음, 텍스트 잘림 없음 |

## 게시 실행 결과

- **X:** `published_verified` — 성공 토스트 확인 후 공개 프로필의 최신 게시물 URL을 read-back.
  - URL: `https://x.com/shinjaehyun2018/status/2089495037231206725`
  - post ID: `2089495037231206725`
  - 게시 당시 스냅샷은 226개이며, 현재 공개 정본(228개)과 구분해 추적한다.
- **Instagram (`shinjaehyun2018`):** `published_profile_readback` — 4:5 crop에서 상단 라벨·226개·게임 카드·카테고리 문구를 확인하고, 캡션(259/2200)·해시태그를 read-back한 뒤 공유. `게시물이 공유되었습니다` 확인과 프로필 `게시물 1`/새 그리드 로딩까지 확인.
  - 프로필: `https://www.instagram.com/shinjaehyun2018/`
  - 개별 permalink/post ID: 화면에 노출되지 않아 미회수.
- **Threads:** `blocked_auth_required` — 기존 탭이 `Instagram으로 계속하기 shinjaehyun2018` 로그인 카드 상태. 계정 연결·로그인 동작은 수행하지 않았으며 게시물도 생성하지 않음.
- **Instagram (`jh_shinz`):** `published_profile_readback` — 카드 게시 완료 모달(`게시물이 공유되었습니다`)과 프로필 게시물 수 `7 → 8`, 최신 첫 그리드 카드의 `터치로 바로 즐기는 / 어린이 미니게임 228개`를 확인.
  - 최초 입력이 잘린 사실을 발견한 뒤, 게시물 편집 화면에서 기존 정본 캡션을 UTF-8 클립보드로 전체 교체했다. Composer read-back `454/2200`에서 제목·228개·URL·해시태그를 확인했고, 저장 후 공개 게시물에서 같은 전체 문구를 다시 확인.
  - AI label ON. Threads cross-post toggle은 ON으로 관찰됐으나 Threads 개별 permalink/공개 피드는 회수하지 못했으므로 Threads 게시 완료로 단정하지 않는다.
  - 프로필: `https://www.instagram.com/jh_shinz/`; 개별 Instagram permalink/post ID는 미회수.

## WarpCache 재사용 준비

- `verify_sns_package.py`를 canonical 프로젝트 경로에 추가하고 2026-08-18에 PASS: 원고 4종, 이미지 3종의 규격·SHA-256, `games.json` 게임 수, 금지 수치 171을 오프라인으로 점검한다.
- 현재 WarpCache Golden registry에는 이 SNS 유형의 적합한 verifier가 없어 query-only MISS로 처리했다. WarpCache worktree가 이미 dirty이므로 `golden-promote` registry 쓰기는 보류한다.
- clean registry 시 promotion 후보: `kind=script`, canonical=`marketing/sns/2026-08-18/verify_sns_package.py`, verifier=`py311-media/Scripts/python.exe marketing/sns/2026-08-18/verify_sns_package.py`, graph refs=`project:jangyoon-s-game`, `capability:sns-package-count-and-asset-verification`, `safety:no-session-or-credential-access`.

## 재개 조건

Threads 인증을 사용자가 완료하면, 이미 준비된 `threads.md` + `assets/threads-card.png`를 업로드 → 게시 → URL read-back만 수행하면 된다.
