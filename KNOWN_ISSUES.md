# Known Issues — jangyoon-s-game

부수 발견된 기존 결함 추적. 발견 시 append, 해소 시 체크 후 날짜 기재.

## 2026-07-29 발견 (PHASE 4, nyx)
- [x] games.json에 `balloon-pop` 중복 id 잔존 — 해소 2026-07-29 (구버전 항목 제거, 2026-07-28 갱신본만 유지, menu.json label 동기화)
- [x] README.md 표/최근변경 섹션에 최근 게임(apple-basket·clover-find·teddy-dress 등) 다수 미반영 — 해소 2026-07-29 (표 143→193행, games.json SSOT 전량 대조, 뱃지/summary 194로 정정)
- [x] CHANGES.md 2026-07-28 항목에 제어문자 오염(`\x08`/`\x07`) — 해소 2026-07-29 (제어문자 제거, `balloon-pop`/`apple-basket` 원문 복원)

## 2026-07-30 발견·해소 (PHASE 4, nyx)

- [x] README.md 게임 표에 `typing-web`(외부 GitHub Pages 배포 항목, games.json에는 존재하나 로컬 `./id` 링크 패턴과 달라 누락) 1건 미반영 — 해소 2026-07-30 (표 193→194행, 외부 링크 형태로 추가, games.json/README 실측 diff로 재검증 완료)

## 2026-08-09 발견 (일일 게임 제작, nyx)

- [x] `hidden-object-hunt`·`rhythm-touch-beat`(커밋 a919eae, 2026-08-07 배포)가 README.md "최근 변경사항" 섹션 및 CHANGES.md 양쪽에 변경 이력 항목이 없다. — 해소 2026-08-10 (Gemini 굿모닝 래퍼 세션에서 README 최근 변경사항 및 CHANGES.md에 소급 반영 완료)
