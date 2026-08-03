## 2026-08-04 (일일 게임 제작, nyx)

- 게임 2종 추가: `bicycle-balance`(🚲 자전거 균형 타기), `fridge-sort`(🧊 냉장고 정리하기).
- `bicycle-balance` — 화면을 드래그해 균형 트랙의 마커를 초록 안전구역에 맞추고, 오른쪽 페달 버튼을 계속 눌러 앞으로 나아가는 실시간 균형 유지 게임. 균형점이 랜덤 방향으로 계속 표류하므로 지속적으로 재조정해야 하며, 안전구역을 550ms 이상 벗어나면 넘어짐. 기존 `balance-tower`(정적 블록 쌓기 타이밍)·`stone-balance-walk`(좌우 교차 버튼 균형)와 달리 연속적인 실시간 밸런스 조정이 핵심 차별점. 300m 도달 시 성공, `bicycle-balance_best`에 최고 거리 저장.
- `fridge-sort` — 냉장고 아이템(사과·우유·아이스크림 등)을 손가락으로 드래그해 냉장·냉동·실온 3칸 중 알맞은 칸에 넣는 40초 생활 인지 게임. 15% 확률로 등장하는 상한 음식은 어떤 칸에 넣어도 정답 처리(치우는 게 목표). 기존 `recycle-rescue`(재질별 분리수거)·`laundry-sort`(색깔별 분류)와 달리 "보관 온도"라는 새 분류 기준과 상한 음식 회피 요소가 차별점. 연속 정답 3개마다 보너스 점수, `fridge-sort_best`에 최고 점수 저장.
- 두 게임 모두 단일 HTML, 외부 의존성 없음, Pointer Events(pointerdown/move/up만 사용, touchstart/mousedown 미사용), 100dvh/overflow 보호, 시작·종료 오버레이, 홈 링크, localStorage 최고기록, SVG 썸네일 포함. JS 구문 검증(node --check) PASS.
- `games.json` 202→204, 고유 ID 204(중복 0건), `menu.json` kids 카테고리 최상단에 신규 2건 배치. README 뱃지·상단문구·게임 표·최근변경 섹션을 실측 204로 동기화.
- 부수 발견·해소: README.md "최근 변경사항 (2026-08)" 섹션에 2026-08-03 rocket-sequence-launch·shadow-trail-match 추가 항목이 누락돼 있어 함께 보완(CHANGES.md에는 기록됐으나 README에 미반영 상태였음).

## 2026-08-03 (굿모닝 wrapper, Codex)

- 게임 2종 추가: `rocket-sequence-launch`(🚀 로켓 순서 발사), `shadow-trail-match`(🐾 그림자 발자국 탐정).
- `rocket-sequence-launch` — 관제사가 보여주는 그림 명령(⛽/⭐/🌙/🌱) 순서를 기억하고 같은 순서로 눌러 6라운드 로켓을 발사하는 순서 기억 게임. 오답은 감점 후 같은 패턴을 다시 보여주고 `rocket-sequence-launch_best`에 최고 별 기록을 저장.
- `shadow-trail-match` — 발자국 단서와 흐릿한 동물 그림자를 보고 4개 보기 중 정답 동물을 고르는 8라운드 관찰 놀이. 연속 정답 보너스와 `shadow-trail-match_best` 최고점 저장.
- 두 게임 모두 단일 HTML, 외부 의존성 없음, 모바일 터치 우선, 시작/종료 오버레이, 홈 링크, SVG 썸네일 포함.
- `games.json` 200→202, 고유 ID 202, `menu.json` kids 항목과 README 뱃지·상단문구·summary·목록을 실측 동기화.

## 2026-08-01 (굿모닝 wrapper, Codex)

- 게임 2종 추가: `paper-fold-lab`(📄 종이 접기 연구소), `mirror-beam-rescue`(🔦 거울빛 구조대).
- `paper-fold-lab` — 접기 방향을 고르고 구멍을 찍은 뒤 역순으로 펼쳐 4개·8개 대칭 결과를 확인하는 6라운드 상태 변환 퍼즐. 오답은 감점 없이 힌트를 제공하고 `paper-fold-lab_best`에 최고 별 기록을 저장.
- `mirror-beam-rescue` — 거울 손잡이를 드래그해 입사각=반사각 경로를 만들고 별을 구조하는 7라운드 퍼즐. 후반에는 거울 2개 경로로 확장하고 `mirror-beam-rescue_best`에 최고점을 저장.
- `maze-escape` 드래그 버그 수정 — 공 hit-test, 활성 pointer ID, CSS/backing-store 좌표 환산, 작은 이동량 기반 연속 이동을 적용했다. 후속 실기 재현에서 닫힌 벽 충돌 시 시작점으로 되돌아가던 잔여 순간이동을 확인해, 공 반지름을 고려한 벽 경계 clamp와 동일 드래그 내 반대 방향 복귀로 교체했다. 레벨 전환·`pointercancel`·`lostpointercapture`에서는 드래그를 안전하게 종료한다.
- 세 게임 모두 390×664 Chromium 모바일 QA에서 스크롤·콘솔·페이지 오류 0건. 미로는 빈 영역 드래그 불변, 열린 통로 8px 연속 추적, 닫힌 벽에서 위치 단조 증가 후 경계 고정, 시작점 snap-back 0건, 벽에서 반대 방향 복귀를 확인.
- `games.json` 198→200, 고유 ID 200, `menu.json` kids 항목과 README 뱃지·상단문구·summary·목록을 실측 동기화.

## 2026-07-30 (굿모닝 PHASE 4, nyx)
- 게임 2종 추가: marble-roll (🔮 구슬 미로 굴리기), domino-chain (🁣 도미노 잇기)
- marble-roll — 화면 드래그로 방향·거리에 비례한 가속도를 구슬에 가해(마찰 0.985, 반발계수 0.55) requestAnimationFrame 물리 루프로 원-사각형 충돌 판정하는 5라운드 미로 게임. 라운드마다 벽 2→6개, 구멍 1→5개로 난이도 상승. 구멍에 빠지면 즉시 라운드 1부터 재시작, 별(목표)에 닿으면 자동으로 다음 라운드 진행. 기존 bounce-ball(농구공 드리블)과 달리 자유 2D 평면 물리 충돌 굴리기가 핵심. 외부 의존성 없음.
- domino-chain — 화면에 뱀 모양 경로로 배치된 도미노 N개(라운드마다 5→8→12개)에 랜덤 순번이 매겨지고, 제한시간 안에 1번부터 순서대로 터치하면 시각적 배치 순서대로 자동 연쇄 넘어짐 애니메이션이 재생되는 인지·순서 게임. 순서를 틀리면 하트(3개) 감소, 하트 소진 또는 시간 초과 시 실패. 기존 number-order(숫자 순서 맞추기)와 달리 정답 시 물리적 연쇄 반응 애니메이션 보상이 핵심 차별점. 외부 의존성 없음.
- 두 게임 모두 단일 HTML, Pointer Events(touchstart/mousedown 미사용), 100dvh/overflow 보호, 시작·종료 오버레이, 홈 링크, localStorage 최고기록(marble-roll_best/domino-chain_best), SVG 썸네일 포함. JS 구문 검증(node --check) PASS, fan-in 재검증(스크롤 없음·오버레이 2개·pointer 이벤트만 사용·localStorage 사용) 실측 확인.
- games.json 194→196, menu.json kids 카테고리 최상단 2건 추가, README 표/뱃지/summary/최근변경 196 실측 반영.
- 부수 발견·해소: README.md 게임 표에서 `typing-web`(외부 GitHub Pages 배포 게임, games.json에는 존재하나 로컬 링크 패턴과 달라 누락) 1건 미반영 확인 → 표 193→194행 보완 완료, KNOWN_ISSUES.md 기록.
- 재검증(이전 결함 3건, 2026-07-29 KNOWN_ISSUES): games.json 중복 id 0건, menu.json 파싱 성공, CHANGES.md 제어문자 오염 없음 — 모두 정상 해소 확인.

## 2026-07-29 (KNOWN_ISSUES 정합성 수정, nyx)
- games.json `balloon-pop` 중복 id 해소: 구버전 항목(id 최초 등장, "풍선 터뜨리기"/폭탄 회피 설명, 2026-04-20 추가분)을 제거하고 2026-07-28 갱신본("풍선 터트리기"/별 풍선 보너스, 실제 폴더 index.html과 일치)만 유지. games.json 194→194(중복 제거로 unique count 195→194 표기 정정, 실제 폴더 194개는 불변). menu.json label도 "풍선 터트리기"로 동기화.
- README.md 게임 표(games.json 순서 SSOT) 143→193행으로 51개 누락분(apple-basket·clover-find·teddy-dress 등) 전량 반영 + 뱃지/상단문구/summary 195→194 실측 정정 + "최근 변경사항" 2026-07-28 항목(balloon-pop·apple-basket) 신규 추가.
- CHANGES.md 2026-07-28 항목의 제어문자(`\x08`/`\x07`) 제거 — `\x08alloon-pop`→`balloon-pop`, `\x07pple-basket`→`apple-basket` 원문 복원.
- KNOWN_ISSUES.md 3개 항목 체크·해소일 기재.

## 2026-07-29
- 게임 2종 추가: lightning-dodge (⚡ 번개 피하기), watering-plant (🌱 식물 키우기)
- lightning-dodge — 먹구름 예고 후 번개가 떨어지는 3레인 반사 게임. 위험 신호(구름)를 먼저 보여준 뒤 낙하물이 오는 예고-반응 구조가 기존 rain-dodge/snow-dodge/train-dodge의 즉시 회피형과 다름. 외부 의존성 없음.
- watering-plant — 물뿌리개 버튼 hold-to-release로 게이지를 목표 구간에 맞추는 6라운드 육성 게임. seed-sprout-race(경주형)와 달리 단계별 성장(씨앗→새싹→꽃) + 과다/과소 급수 판정. 외부 의존성 없음.
- 두 게임 모두 단일 HTML, Pointer Events, 100dvh/overflow 보호, 시작·종료 오버레이, 홈 링크, localStorage 최고기록, SVG 썸네일 포함
- 총 게임 수 195개 달성 (games.json/menu.json 실측 동치 확인) — **[2026-07-29 정정]** balloon-pop 중복 id가 섞여 있던 카운트였음, 중복 제거 후 실제 194개(games.json unique 실측). 정정 근거는 위 "2026-07-29 (KNOWN_ISSUES 정합성 수정)" 항목 참조
- 부수 보완: menu.json kids 카테고리에서 누락돼 있던 apple-basket(2026-07-28 추가분)을 백필. README 표/최근변경 백필은 범위 밖 별도 필요 → **[2026-07-29 완료]** 위 항목에서 README 표/최근변경 백필 완료

## 2026-07-28
- 게임 2종 추가: balloon-pop (🎈 풍선 터트리기), apple-basket (🍎 떨어지는 사과 담기)
- 총 게임 수 193개 달성

﻿## [2026-07-27]
- Add `clover-find`: 🍀 네잎클로버 찾기 (밭에 숨은 네잎클로버를 찾아라! 오탭 시 시간 감소, 레벨업으로 난이도 상승)
- Add `teddy-dress`: 🧸 곰돌이 옷 입히기 (미션에 맞는 옷을 탭해 곰돌이를 꾸며요! 10라운드 콤보 점수 도전)

# 변경 이력

## 2026-07-24 — 신호등 안전 건너기 · 숨결 비눗방울

- **traffic-light-crossing / 🚦 신호등 안전 건너기** — 빨간불·노란불에는 기다리고 초록불일 때만 건너기 버튼을 누르는 45초 생활 안전 게임. 정답은 +10점, 잘못 건너면 기회만 차감하며 `traffic-light-crossing_best` 최고점을 저장한다. 기존 `traffic-cross`의 차량 회피 이동과 달리 신호 관찰과 행동 억제가 핵심이다.
- **breath-bubble / 🫧 숨결 비눗방울** — 버튼을 누르는 동안 방울이 커지고 점선 목표 원과 비슷해졌을 때 손을 떼는 8라운드 hold-to-release 게임. 크기 오차별 100/60/30/10점과 `breath-bubble_best` 최고점을 저장한다. 기존 `soap-bubble-catch`의 드래그 포획과 달리 누름 시간 조절과 릴리즈 판단이 핵심이다.
- 두 게임 모두 단일 HTML, 외부 의존성 없음, Pointer Events, 100dvh/overflow 보호, 시작·종료 오버레이, 홈 링크, SVG 썸네일을 포함한다.

## 2026-07-23 — 날씨 옷장 탐험 · 마음 거울

- **weather-outfit** — 햇빛·비·눈·바람·더위·추위 6개 날씨 장면을 보고 알맞은 옷을 고르는 45초 생활 판단 게임. 매 라운드 보기 4개의 위치를 섞고, 오답은 감점 대신 구체적인 날씨 힌트만 제공하며 `weather-outfit_best` localStorage 최고 기록을 저장한다. 기존 `bandage-doctor`의 증상-도구 추론과 달리 계절·기상 조건을 일상 자기관리 행동으로 연결한다.
- **emotion-mirror** — 선물·퍼즐·천둥·소풍 등 생활 장면을 읽고 기쁨·슬픔·화남·무서움·뿌듯함·놀람 중 가장 가까운 감정을 고르는 8라운드 사회정서 게임. 틀리면 감정 단서를 보여주고 같은 장면에 다시 도전하며 `emotion-mirror_best` localStorage 최고 마음 별을 저장한다. 기존 반응·수학 게임과 달리 상황 이해와 감정 어휘화가 핵심이다.
- 두 게임 모두 모바일 터치 우선 단일 HTML, 외부 의존성 없음, 44px 이상 터치 버튼, 시작/종료 오버레이, 홈 링크, 100dvh/overflow 보호, SVG 썸네일을 포함한다.

## 2026-07-22 — 반창고 동물병원 · 편지 배달 놀이

- **bandage-doctor** — 다친 동물의 증상 아이콘(🤕/🤒/🥶/🤢)을 보고 알맞은 치료 도구(🩹/🌡️/🧣/🍵)를 45초 동안 골라주는 인지 반응 게임. 매 환자마다 도구 버튼 4개 위치가 셔플되어 위치 암기가 아닌 실제 증상 판별이 필요, 오답 무감점(가벼운 흔들림만), `bandage-doctor_best` localStorage 최고점 저장. 기존 `pet-feed`(단순 먹이 주기)와 달리 증상→원인 매칭 추론이 핵심.
- **letter-delivery** — 편지에 적힌 숫자와 같은 번호의 우체통으로 드래그해 배달하는 40초 게임. 우체통 3개 중 정답 1개, 배치가 매 라운드 섞여 재탐색 필요, 오답 드롭은 편지가 제자리로 복귀(무감점), `letter-delivery_best` localStorage 최고점 저장. 기존 `recycle-rescue`(재질 판단 드래그 분류, 고정 3통)와 달리 숫자 인식 + 매 라운드 위치 재탐색이 핵심.
- 두 게임 모두 모바일 터치 우선 단일 HTML, 외부 의존성 없음, 시작/종료 오버레이, 홈 링크, Pointer Events(letter-delivery)/Click(bandage-doctor), 100dvh/overflow 보호, SVG 썸네일 포함. 검증은 Playwright 미가용 환경이라 Node vm DOM mock 하네스(2026-07-13 gonggi-nori 선례 준용, `runtime/audit/2026-07-22/jangyoon-games/verify-harness.js`)로 fan-in 후 fresh 재검증: happy-path 5라운드 전승 + 타이머 만료 종료 오버레이 전환, 런타임 예외 0건.

## 2026-07-21 — 행성 궤도 주차 · 기차표 도장 찍기

- **planet-orbit-park** — 손가락으로 달을 원형 드래그해 초록 궤도 구역에 맞춘 뒤 손을 떼는 orbit parking 게임. 7라운드, 각도 오차별 점수, `planet-orbit-park_best` localStorage 최고점 저장. 기존 `lighthouse-guide`/`meteor-shield`의 회전 유도·방어와 달리 목표 각도에 직접 주차 후 릴리즈하는 공간 감각 메커니즘.
- **train-ticket-stamp** — 이동하는 기차표 스트립에서 별표 표가 가운데 올 때 도장을 꾹 누르고 떼는 hold-to-punch 타이밍 게임. 12장 도전, 거리 오차별 점수, `train-ticket-stamp_best` localStorage 최고점 저장. 기존 단순 탭·스와이프류와 달리 누름 상태 시각 피드백과 릴리즈 판정을 결합.
- 두 게임 모두 모바일 터치 우선 단일 HTML, 외부 의존성 없음, 시작/종료 오버레이, 홈 링크, Pointer Events, 100dvh/overflow 보호, SVG 썸네일 포함.

## 2026-07-20 — 태권도 품새 리듬 · 받침 낚시왕

- **taekwondo-poomsae** — 표시된 `지르기/앞차기/막기/서기` 동작을 45초 동안 맞추는 반응·리듬 수련. 연속 정답 콤보, 오답 무감점, localStorage 최고점 저장.
- **batchim-fishing** — `고□→공`처럼 낱말을 소리 내어 읽고 알맞은 받침을 고르는 10라운드 한글 놀이. 정답을 고르면 물고기가 낚이는 시각 피드백, 연속 정답 별 보너스, localStorage 최고별 저장.
- 두 게임 모두 모바일 터치 우선 단일 HTML, 외부 의존성 없음, 시작/종료 오버레이와 44px 이상 터치 버튼 포함.

## 2026-07-18 — 분리수거 구조대 · 달빛 순서 탐험

- **recycle-rescue** — 종이·플라스틱·캔 물건을 알맞은 통으로 직접 끌어 넣는 40초 환경 학습 게임. 기존 `laundry-sort`의 색상 버튼 선택과 달리 재질 판단과 공간 드롭이 핵심이며, 오답 감점 없이 재도전하고 연속 분류 보너스와 localStorage 최고점을 저장.
- **moon-phase-quest** — 섞인 네 가지 달 모양을 어두운 달부터 밝은 달까지 복원하는 5단계 우주 학습 게임. 기존 `pattern-parade`의 반복 규칙 추론과 달리 자연 현상의 밝기 변화를 순서화하며, 오답 감점 없이 반복하고 localStorage 최고 별 수를 저장.
- 두 게임 모두 모바일 터치 우선 단일 HTML과 SVG 썸네일, Pointer Events, 시작/종료 오버레이, 외부 의존성 0건을 포함.

## 2026-07-06 — 고양이 낚싯대 놀이 (cat-teaser-play) · 종이비행기 날리기 (paper-airplane-fly)

- **cat-teaser-play** — 화면을 드래그해 깃털(🪶)을 움직이면 고양이(🐱)가 lerp 추적(`CAT_LERP: 0.09`, dt 정규화)으로 따라와 실뭉치(🧶)를 낚아채는 드래그 유도 게임. 실뭉치는 최대 2개 동시 등장(`MAX_YARN: 2`), 포획 반경 32px, `YARN_LIFETIME_MS: 5000` 안에 못 잡으면 fade-out 후 재등장. 40초 타임어택, localStorage 최고점(`cat-teaser-play_best`). CSS `perspective`+`rotateX` 원근 방바닥(diving-board-jump 기법 재사용)과 그림자+본체 레이어 분리 3D 카드.
- **paper-airplane-fly** — 화면을 톡톡 터치할 때마다 `FLAP_VELOCITY: -370`의 상승 임펄스를 받고 중력(`GRAVITY: 1300`)으로 자연히 하강하는 플랩 물리 비행 게임. ⭐별(`STAR_CHANCE: 0.45`)은 +10점, 🌩️먹구름은 목숨 감소(`LIVES: 3`, 실패해도 계속 진행하는 7살 친화 톤). 비행기는 수직 속도에 비례해 기울어지는 회전 피드백(`tilt = velocityY/11`), 배경 장식 구름은 `translateZ(-220px)` 패럴랙스. 40초 도전, localStorage 최고점(`paper-airplane-fly_best`).
- 두 게임 모두 Playwright iPhone 12 viewport(390×664) 검증: 스크롤 없음·시작 오버레이 표시·home-link 존재·핵심 메커니즘(고양이 포획/비행기 flap+충돌) 런타임 에러 0건 확인.
- 각 단일 HTML + SVG 썸네일(320x180, 우하단 타이틀 규격), 외부 의존성 0건. 굿모닝 07-06 PHASE 4 자동 제작.

## 2026-07-05 — 몬스터 파크 (monster-park)

- **monster-park** — 공원에 나타나는 몬스터를 탭해서 포획하는 수집형 게임. 12종 몬스터를 등장 확률 가중치(희귀할수록 낮음, `weight` 필드)로 랜덤 스폰(`SPAWN_INTERVAL_MS: 850`, 최대 5마리 동시 등장, 생존시간 1.4~2.4초), 탭하면 포획 애니메이션(pop) + 도감(dex) 등록. 같은 몬스터 3마리 모으면 레벨업(`LEVEL_UP_COUNT: 3`), 12종 완전 수집이 목표. 45초 타임어택(`ROUND_SECONDS: 45`), localStorage에 도감 진행도(`monster-park_dex`)와 최고 포획 수(`monster-park_best`) 저장.
- 단일 HTML + SVG 썸네일(320x180, 우하단 타이틀 규격), 이모지 기반이라 이미지 자산 없음(외부 의존성 0건).

## 2026-07-04 — 터널 달리기 (tunnel-dash) · 다이빙대 점프 (diving-board-jump)

- **오늘 특이사항**: Hermes 커밋 `80be45f`(runner-game/space-catcher 3D 스프라이트)에서 실측한 CSS 3D 기법을 신규 게임 2종에 적용 — WebGL/three.js 없이 `perspective` + `transform-style: preserve-3d` + `translateZ()` 레이어 분리만으로 원근·깊이감 구현.
- **tunnel-dash** — `#gameArea`에 `perspective: 620px`, 터널 링 4개가 `translateZ(-900px)→translateZ(220px)` 애니메이션으로 화면을 향해 다가오는 터널 러너. 좌우 3레인 이동(버튼/탭/화살표키)으로 장애물(🪨, translateZ 큐브형 정면+측면 레이어)은 피하고 보석(💎)은 획득. 30초 타임어택, localStorage 최고점(`tunnel-dash_best`). 캐릭터는 runner-game과 동일한 그림자(translateZ -24px)+측면(translateZ -8px)+정면(translateZ 16px) 레이어 카드 기법 재사용.
- **diving-board-jump** — 다이빙대에서 좌우로 ping-pong 스윕하는 물결 링에 타이밍 맞춰 점프하는 게임. 수면은 `rotateX(72deg) translateZ(10px)`로 원근 바닥(space-catcher의 `ship-ring` 기법과 동일 계열)을, 낙하 시 다이버는 `translateZ` 증가+scale 확대로 카메라에 가까워지는 착시를 구현. 착수 정확도(스윕 중앙과의 거리)로 100/70/40/15점 차등, 5회 도전, localStorage 최고점(`diving-board-jump_best`).
- 각 단일 HTML + SVG 썸네일(320x180, 우하단 타이틀 규격), 이미지 자산은 게임 폴더 자체 보유(외부 의존성 0건). 굿모닝 07-04 PHASE 4 자동 제작.

## 2026-07-03 — 햄스터 쳇바퀴 달리기 (hamster-wheel-run) · 무당벌레 잎사귀 건너기 (ladybug-leaf-hop)

- **hamster-wheel-run** — 화면을 빠르게 탭할수록 쳇바퀴가 회전하고 거리가 쌓이는 탭 스피드 게임. 지나가는 도토리(🌰)를 탭하면 보너스 거리, 탭을 멈추면 자연 감속, 30초 타임어택, localStorage 최고 거리. 기존 반사류(bounce-ball 등)와 달리 연속 탭 리듬 유지가 핵심 메커니즘.
- **ladybug-leaf-hop** — 반짝이는 다음 잎사귀만 순서대로 탭해야 무당벌레가 폴짝 뛰어 건너가는 순서 판단 게임. 잘못된 잎사귀를 탭하면 풍덩(리플 이펙트)과 함께 목숨 감소(목숨 3개), localStorage 최고점. 기존 frog-jump(1버튼 타이밍 점프)와 달리 다중 타겟 중 정답 선택이 핵심.
- 각 단일 HTML + SVG 썸네일, 외부 의존성 0건. 굿모닝 PHASE 4 자동 제작.

## 2026-07-02 — 개구리 파리 잡기 (frog-tongue-catch) · 회전초밥 주문받기 (sushi-conveyor)

- **frog-tongue-catch** — 날아다니는 곤충을 탭하면 개구리 혀가 뻗어 포획하는 조준·반사 게임. 🐝벌은 감점, 40초 타임어택, localStorage 최고점. 기존 frog-jump(점프형)와 달리 혀 조준-포획 메커니즘.
- **sushi-conveyor** — 손님 주문과 같은 초밥이 회전 벨트로 지나갈 때 탭하는 주문-매칭 게임. 콤보 보너스, 50초 타임어택. 기존 queue-train(색 라우팅)·emoji-chef/pizza-maker(드래그 레시피)와 다른 컨베이어-매칭 메커니즘.
- 각 단일 HTML + SVG 썸네일, 외부 의존성 0건. 굿모닝 PHASE 5 자동 제작.

## 2026-06-28 — 무지개 레일 공방 (rainbow-rail-builder)
- 빈 5×5 판에 손가락으로 직접 레일을 그려 미션 스티커를 순서대로 지나가는 5레벨 드로잉 퍼즐로 전면 개편.
- 기존 회전 타일 퍼즐과 겹치지 않도록 `draw_to_connect` 체감으로 변경: 출발역에서 목표역까지 직접 경로를 그린 뒤 기차가 따라 달림.
- 모바일 우선 5×5 드로잉 보드, 미션 스티커 순서 검증, 시작/종료 오버레이, localStorage 최고기록(`rainbow-rail-builder_best`), 외부 의존성 없는 SVG 썸네일 포함.

## 2026-06-27 — 눈방울 구조대 (bubble-snow-rescue)
- Bubble Bobble/Snow Bros 감성을 장윤이용으로 순화한 신규 5스테이지 2.5D 액션 퍼즐 추가.
- 모바일 전용 원형 조이스틱 + A/B 액션 버튼, 데스크탑 키보드(←→/A/D, Space/W, J) 호환.
- 눈방울 발사 → 몬스터 말랑눈덩이화 → 굴림/연쇄 구조 → 스테이지 클리어 루프와 localStorage 최고기록 저장 적용.
- 조이스틱 위 입력과 B 점프를 edge-trigger 방식으로 보정해 대각선 점프가 이동 방향과 함께 적용되고, 버튼/조이스틱을 계속 누를 때 엉뚱한 위치에서 재점프하지 않도록 수정.
- 5스테이지에서 위로 못 올라가던 문제를 고치기 위해 보스 스테이지 발판을 계단형으로 재배치하고, 플레이어가 발판 옆면 충돌에 끼지 않도록 수평 발판 충돌을 제거했으며, 조이스틱 위 입력을 착지 시 재도약 가능한 짧은 쿨다운 방식으로 보강.
- 단일 HTML + SVG 썸네일, 외부 의존성 없음.

## 2026-06-27 — 달 로켓 연료 계산 (moon-rocket-math)
- 덧셈·뺄셈 정답을 탭해 로켓 연료를 채우는 45초 수학 게임 추가.
- 단일 HTML + SVG 썸네일, 외부 의존성 없음.

## 변경사항 (2026-06-27 — 코덱스 로봇 연구소 신규)

- **🤖 코덱스 로봇 연구소 (codex-robot-lab)** — Wikidocs 링크와 Codex 플러그인 호환 설계에서 뽑은 `계획 → 수정 → 검증 → 마무리` 루프를 장윤이용 명령 카드 게임으로 변환.
- **적용 포인트**: 읽기/계획/worktree/patch/test/review/commit/push 카드를 조합해 파이프라인을 만들고, 실패 시 repair → re-verify로 다시 도전하는 흐름을 시각화.
- **비주얼**: 모바일 단일 HTML, 2.5D 로봇·터미널 패널·네온 연구소·파티클 보상·WebAudio 피드백. 외부 CDN/이미지 없음.

## 변경사항 (2026-06-26 — 꿈인형 뽑기 시범 3D풍 업그레이드)

- **claw-machine** — 단순 이모지 인형 대신, 레이어 분리·깜빡임·부유·기울기·측면 두께를 가진 귀여운 2.5D 꿈인형 캐릭터 세트로 교체. 뽑은 인형은 컬러 배지 트로피로 기록되도록 수정.
- `runner-game` 대신 별도 게임으로 시범 적용하여, `진짜 3D는 아니지만 더 귀엽고 손맛 있는` 방향의 후보 스타일을 검증.

## 변경사항 (2026-06-26 — 장윤이 이미지 3D 애니메이션 업그레이드)

- **space-catcher** — 기존 평면 PNG 낙하물/플레이어를 3D 포토카드형 스프라이트로 교체. 전면/후면 레이어, 글로우, 그림자, 회전·부유 애니메이션, 캐치 시 확대 피드백 적용.
- **runner-game** — 장윤이 러너와 수집 아이템 모두 3D 카드형 비주얼로 업그레이드. 시점 기울기, 공중 부유, 깊이 스케일, 점수 획득 시 펄스 피드백 적용.
- 두 게임 모두 원본 `images/jangyoon.PNG` 그대로 사용하면서 "2D 사진 붙임" 느낌을 줄이고 입체감/움직임을 강화.

## 변경사항 (2026-06-26 — 큐큐 기차역 신규)

- **🚂 큐큐 기차역 (queue-train)** — 자료구조 시각화 아이디어를 장윤이용 게임으로 번역한 Queue 학습 놀이. 기차 칸이 줄(Queue)로 서고, 플레이어는 **맨 앞 칸(front)** 색을 보고 같은 색 역 버튼으로 보낸다.
- **구조 적용 포인트**: 정적 무대(선로·역·대기칸)와 동적 객체(기관차·칸·파티클)를 분리하고, `QueueModel / View / App` 역할 분리로 구현.
- **게임성**: 45초 타임어택, 연속 정답 콤보 보너스, 하트 3개, localStorage 최고 기록(`queue-train_best`) 저장.

## 변경사항 (2026-06-24 — 페널티킥·미니골프 2종 신규)

- **⚽ 페널티킥 (penalty-kick)** — 공을 스와이프해 방향과 파워를 정하고, 좌/중/우로 다이브하는 골키퍼를 피해 골을 넣는 슈팅 게임. 5킥 도전, 라운드마다 키퍼 난이도 상승, 최고기록 저장. 저장소 첫 축구 게임.
- **⛳ 미니골프 (mini-golf)** — 공을 반대로 당겼다 놓아 굴리는 새총식 퍼팅. 벽 반사·장애물을 넘어 홀에 넣고, 적은 타수일수록 높은 ★ 등급. 저장소 첫 골프 게임.

## 변경사항 (2026-06-23 — 볼링·낙하산 착륙 2종 신규)

- **🎳 볼링 (bowling)** — 아래→위 스와이프로 공을 굴려 핀을 쓰러뜨리는 10프레임 볼링. 스트라이크·스페어 판정, 점수 누적.
- **🪂 낙하산 착륙 (parachute-drop)** — 좌우 탭/기기 기울임으로 낙하산을 조종해 녹색 착륙 패드에 안전 착지. 바람·새 회피, 레벨업마다 패드 폭 축소.

## 변경사항 (2026-06-20 — 슈퍼 점프 모험 후속 수정: 워프·크라우치·5스테이지·보스)

### 🍄 슈퍼 점프 모험 (super-mario) 플레이 피드백 반영 수정

- **워프 보너스 룸 데드엔드 수정**: 복귀 파이프 위에 잠깐 서거나 룸 오른쪽에 도달하면 자동 복귀(▲▼로 즉시 탈출도 가능). 더 이상 못 나오는 일 없음
- **큰 마리오 ▼ 숙이기(크라우치)** 추가. 코요테 타임 도입으로 점프·크라우치 판정 안정화
- **정규 5스테이지(1-1~1-5) + 보스 성 스테이지**로 확장. 각 스테이지는 **깃발 클리어 연출**(깃대 슬라이드)로 마무리 후 다음 스테이지
- **보스는 파워업 없이도 처치 가능**: 머리 밟기 판정 완화 + 보스 성 끝의 **도끼**에 도달하면 즉시 처치(원작식). 파이어볼도 가능
- **효과음 구분**: 커짐(버섯)·파이어(꽃)·작아짐(피격) 사운드 분리
- 재시작/전환 시 잔여 배너·타이머가 새 판을 멈추던 버그 수정(initState 초기화)
- 헤드리스 하니스 13개 항목(워프·크라우치·5스테이지 진행·보스 2경로·회귀) 검증 통과

## 변경사항 (2026-06-20 — 슈퍼 점프 모험 대확장: 스테이지·보스·파워업)

### 🍄 슈퍼 점프 모험 (super-mario) 대규모 업데이트

원작 슈퍼마리오를 벤치마킹해 단일 레벨 플랫포머를 **월드 1(스테이지 1-1·1-2·1-3 + 👑 보스전)** 구조로 확장.

- **스테이지 진행**: 깃발 도달 시 다음 스테이지로, 마지막 보스를 무찌르면 월드 클리어. 스테이지 전환 배너 + 테마(들판/동굴/성)
- **파워 티어(원작식)**: 작은 마리오 → 🍄버섯(큰 마리오) → 🌸꽃(파이어). 피격 시 한 단계만 하락
- **🔥 파이어볼**: 파이어 상태에서 슈팅 버튼 등장 → 바닥을 튕기며 적을 처치(동시 최대 2발)
- **⭐ 무적 별(superduper)**: 일정 시간 무지개 반짝임 + 접촉만으로 적 처치 + 속도 부스트
- **숨은 블록(H/h)**: 공개 전에는 통과되고, 머리로 치면 나타나 코인/파워업 지급
- **파이프 비밀길**: 워프 파이프 위에서 ▼ → 코인 보너스 룸, ▲로 본선 복귀(진척 보존)
- **👑 보스전**: HP 바를 가진 보스(좌우 이동·점프·불꽃 발사), 파이어볼/밟기로 처치
- **방향패드(◀▶▲▼) 조작** + 점프 + 상황별 🔥슈팅 버튼, 키보드 매핑 병행
- 헤드리스 하니스(`window.__TEST__` 훅, 비커밋)로 스테이지 진행·파이어볼·별 무적·워프·히든블록·보스 처치 13개 항목 자동 검증
- localStorage 키: `super-mario_best`

## 변경사항 (2026-06-16 — 슈퍼 점프 모험 추가 · 미로 탈출 시간 제한 제거)

### 🍄 슈퍼 점프 모험 (super-mario) 추가

달리고 점프해서 코인을 모으고 적(굼바)을 위에서 밟아 처치, 깃발에 도착하면 클리어하는 캔버스 기반 옆스크롤 플랫포머.

- 기존 dino-run(탭 점프 회피)·cloud-jump(수직 상승)과 달리 좌우 자유 이동 + 블록 상호작용 + 적 밟기 + 깃발 골인의 정통 플랫포머 메커니즘
- 약 132칸 타일맵 레벨(땅·벽돌·물음표/파워업 블록·파이프·구덩이), 중력/관성 물리, 카메라 추적, 패럴럭스 배경(구름·언덕)
- 키보드(← → · 스페이스/위)와 모바일 터치 버튼(◀ ▶ · 점프) 동시 지원, **가변 점프 높이**(오래 누르면 더 높이)
- **🍄 슈퍼버섯 파워업**: 파워업 블록(★)에서 버섯이 나오고, 먹으면 큰 마리오가 되어 적 피격 시 죽지 않고 작아짐(실드)
- **WebAudio 인라인 효과음**: 점프·코인·블록·벽돌·적 처치·파워업·피격·클리어
- 구덩이 추락 시 마지막 안전 위치로 부활(즉시 사망 루프 방지), 캔버스 `object-fit: contain`으로 모바일 화면 비율 보존
- 시간 제한 없는 완주형, localStorage 키: `super-mario_best`
- 자동 플레이 하니스로 깃발 도달 클리어·파워업·실드 동작 검증

### 🌀 미로 탈출 (maze-escape) 시간 제한 제거

60초 카운트다운으로 강제 종료되던 방식을 없애고, 시계에 쫓기지 않고 모든 난이도 미로를 완주하는 방식으로 변경.

- 타이머는 "걸린 시간" 카운트업 기록으로 전환, 최고 기록 = 최단 완주 시간(`maze-escape_besttime`)
- 4단계 난이도(7×7 → 9×9 → 11×11 → 13×11) 모두 풀면 완주 클리어
- 순수 타임어택/생존형 게임(과일 자르기·대포알·기차 피하기 등)의 시간 제한은 의도된 핵심 룰이라 그대로 유지

## 변경사항 (2026-06-10 — 탱그램 퍼즐 추가)

### 🔶 탱그램 퍼즐 (tangram-puzzle) 추가

7가지 탱그램 조각을 드래그해서 목표 실루엣 모양(집·고양이·오리·물고기·배)에 맞추는 공간 감각 퍼즐 게임.

- 기존 jigsaw-mini(사진 조각)·ubongo(폴리오미노)와 달리 고전 탱그램 7조각 형태
- 목표 실루엣을 보고 조각을 스냅 방식으로 배치, 7개 모두 맞추면 레벨 완성
- 5가지 목표 모양 (레벨이 올라갈수록 어려운 모양)
- 배치된 조각을 다시 드래그해서 되돌리기 가능, localStorage 최고 레벨 저장

## 변경사항 (2026-06-10 — 별 더하기 추가)

### ⭐ 별 더하기 (star-adder) 추가

두 그룹의 별을 탭해서 바구니에 넣고 덧셈 합산을 맞추는 시각적 수학 학습 게임.

- 기존 math-quiz(텍스트 문제풀기)·number-order(순서 탭)와 달리 별 오브젝트를 직접 이동하는 조작감
- 그룹 A + 그룹 B 별을 개별 탭 → 바구니로, 바구니 탭 → 돌려보내기 가능
- 5레벨 (그룹당 최대 9개), 목숨 3개, 연속 정답 시 레벨업
- 레벨별 점수 배수(score × level), localStorage 최고기록 저장

## 변경사항 (2026-05-30 — 보물 잠수·색깔 로켓 추가)

### 🤿 보물 잠수 (treasure-dive) 추가

화면을 탭하는 동안 다이버가 아래로 내려가고, 손을 떼면 위로 올라오는 수직 탐험 액션 게임.

- 탭 유지→잠수, 손 떼기→부상 메커닉 — 기존 submarine-dodge(수평 드래그)·fish-catch(위에서 잡기)와 차별화
- 💎 보물(6종) 잡으면 10점, 🫧 공기방울로 숨 채우기, 🦈 상어·오징어·바위 회피
- 공기 게이지 — 0이 되면 생명 차감, 생명 3개 도전
- 깊이(m) 표시 + 40m마다 자동 보너스 3점 누적

### 🚀 색깔 로켓 (color-rocket) 추가

하늘에서 떨어지는 색깔 별(빨·파·노·초)을 같은 색 발사대 로켓으로 드래그해 분류하는 인지+드래그 게임.

- 기존 shape-sort(모양 분류)·color-tap(텍스트 색 판독)과 달리 드래그 매칭 인터랙션
- 콤보 연결(2개마다 +5 보너스), 바닥 도달 시 콤보 리셋
- 40초 타임어택, 토요일 휴일 테마 — 우주 배경 + 컬러풀 별들

---

## 변경사항 (2026-05-28 — 반딧불이 잡기·블록 탑 쌓기 추가)

### 🌙 반딧불이 잡기 (firefly-catch) 추가

밤하늘에서 반짝이는 반딧불이를 탭해 잡는 반사 신경 게임. 기존 tap 게임들과 달리 "빛날 때만 잡을 수 있다"는 타이밍 요소가 차별화 포인트.

- 반딧불이가 주기적으로 빛났다 꺼짐 — 빛날 때만 탭 성공
- 8마리가 동시에 유영, 30초 타임어택
- 어두운 밤하늘 + 별 반짝임 + 달 배경

### 🏗️ 블록 탑 쌓기 (balance-tower) 추가

좌우로 움직이는 블록을 탭해서 쌓는 물리 기반 타이밍 게임. 퍼펙트 정렬 시 폭 유지 보너스.

- 탭 타이밍으로 블록 낙하 — 겹치는 부분만 살아남아 점점 좁아짐
- 퍼펙트 ±6px 이내 시 폭 유지, 콤보 카운트
- Canvas 기반 렌더링 + 카메라 스크롤로 무한 상승 연출

---

## 변경사항 (2026-05-18 — 미로 탈출·색깔 피아노 추가)

### 🔵 미로 탈출 (maze-escape) 추가

DFS 알고리즘으로 매판 다른 미로를 자동 생성하는 퍼즐 게임을 추가했다.

- 보라 공을 드래그해서 미로 탈출
- 4단계 난이도 (레벨이 오를수록 미로 크기 증가)
- 60초 타임어택

### 🎹 색깔 피아노 (color-piano) 추가

Web Audio API를 활용한 7색 건반 피아노 게임을 추가했다.

- 빨·주·노·초·파·남·보 7색 건반, 탭하면 음계 재생
- 자유 연주 모드: 원하는 음을 자유롭게 연주
- 따라치기 모드: 제시되는 순서대로 건반을 탭해 곡 완성

---

## 변경사항 (2026-05-10 — 우리말 쇼다운 모바일 화면 압축)

### 📝 우리말 쇼다운 모바일 가독성 조정

모바일에서 문제 화면 진입 시 `확인 버튼`이 너무 아래로 밀리고, 문제 문장과 상단 정보가 과하게 크게 보이던 부분을 정리했다.

- 상단 HUD 패딩과 숫자 카드 높이 축소
- 문제 문장, 선택지, 입력창, 버튼 폰트 크기 한 단계 축소
- 제출 전 해설 패널 문구를 짧게 줄이고 패널 높이 최소화
- 모바일 하단 고정 패널 높이와 페이지 여백을 함께 줄여 첫 문제 화면 밀도 개선

---

## 변경사항 (2026-05-09 — 우리말 쇼다운 추가)

### 📝 우리말 쇼다운 (urimal-showdown) 추가

공개 자료 기반 시드에서 문제 유형만 참고하고, 실제 문제는 응용형 라운드로 다시 구성한 어린이용 우리말 퀴즈 게임을 추가했다.

- **첫 화면에서 유형 선택**: 몸풀기, 맞춤법·띄어쓰기, 응용형 변주, 압박 라운드, 달인전 중 원하는 문제부터 시작
- **어린이 접근성 보강**: 어두운 배경 대신 밝은 카드형 UI, 진한 글자 대비, 큰 문제 문장, 또렷한 버튼/입력창
- **해설 중심 진행**: 정답/오답/시간 종료와 관계없이 모든 문항에서 아래 해설 패널이 열려 학습 흐름 유지
- **정적 배포 대응**: GitHub Pages에서도 동작하도록 서버 API 의존 없이 정적 데이터 모드로 빌드해 포함

비고:

- 원문 방송 문제를 그대로 싣지 않고 `뜻풀이`, `순화어`, `맞춤법`, `띄어쓰기`, `속담`, `관용구`, `한자어` 축을 응용한 파생 문항만 사용
- 운영용 콘텐츠 관리 화면은 GitHub Pages 배포본에서 숨김 처리

---

## 핫픽스 (2026-05-03 — 애벌레 먹이주기 시작하기 버튼 무동작)

### 버그 원인

`caterpillar-feed/index.html`의 `bindStart()` 헬퍼 함수에서
`pointerdown` 이벤트 핸들러가 `e.preventDefault()`를 호출하여
iOS Safari를 포함한 일부 모바일 브라우저에서 터치 이벤트 자체가 취소됨.
동시에 `click` 이벤트에는 `e.preventDefault()`만 달아두고 `fn()`을 호출하지 않아
어떤 경로로도 `resetGame()`이 실행되지 않는 상태.

### 수정 내용

- `bindStart()` 함수 전체 제거
- `btnStart`/`btnRestart` 모두 단순 `click` 이벤트 리스너로 교체

```js
// Before (버그)
function bindStart(el, fn) { ... pointerdown + e.preventDefault() ... }
bindStart(btnStart, resetGame);
bindStart(btnRestart, resetGame);

// After (수정)
btnStart.addEventListener('click', resetGame);
btnRestart.addEventListener('click', resetGame);
```

---

## 변경사항 (2026-04-27 — 신규 게임 2종 추가)

### 🎹 피아노 놀이 (piano-tiles) 추가

건반을 탭해서 직접 음악을 연주하는 음악 놀이 게임.

- **자유 연주 모드**: 도레미파솔라시도 8건반 + 검은건반 5개, 마음대로 탭해서 소리 내기
- **따라하기 모드**: 나비야·반짝반짝·메리의 양·생일 축하합니다 4곡 악보 순서 따라 탭, 빠를수록 보너스 점수
- Web Audio API (triangle oscillator) 기반 브라우저 내장 음원, 외부 의존 없음
- 탭 시 이모지 이펙트(🎵🎶✨) 팝업, 최고 점수 localStorage 저장
- 모바일 iPhone SE 375×667 검증 완료

### 🔷 모양 분류 놀이 (shape-sort) 추가

나타나는 도형을 올바른 바구니에 빠르게 분류하는 인지/학습 게임.

- **모양 분류** 모드: 원·사각형·세모·별 4가지 바구니
- **색깔 분류** 모드: 빨강·파랑·노랑·초록 4가지 바구니
- **모양+색 분류** 모드: 빨간 원·파란 사각형·노란 별·빨간 하트 복합 분류
- 타이머 바로 제한 시간 시각화, 8문제마다 레벨업(제한 시간 0.4초 단축)
- 정답 시 남은 시간에 따른 보너스 점수, 3회 오답 게임 오버
- 모바일 iPhone SE 375×667 검증 완료

---

## 변경사항 (2026-04-25 — 종료버튼 공통화)

### 전 게임 "🏠 게임 목록으로" 종료버튼 일괄 적용

28개 전 게임의 게임오버/클리어/종료 화면에 "🏠 게임 목록으로" 버튼 통일.

#### 목표

- min-height 56px (7살 손가락 기준)
- 기존 3개(tetris/balloon-pop/caterpillar-feed)와 스타일·문구 통일
- 헤더/footer 홈 링크 문구도 "← 홈으로" → "🏠 게임 목록으로" 통일

#### 적용 방식별 분류

| 방식 | 게임 |
| --- | --- |
| overlay-card + btn-home CSS | bounce-ball, bubble-pop-color, color-tap, fish-catch, fruit-catch, jigsaw-mini, memory-match, number-order, rabbit-maze, rhythm-tap, robot-game, space-shooter, star-connect, star-counting, target-hit, whack-a-mole, word-picture-match |
| JS endGame() innerHTML (message div) | space-catcher, runner-game |
| 완성버튼 후 홈버튼 팝업 (celebrate div) | animal-coloring, princess-dressup |
| game-message div 내 (2048 외부 CSS) | 2048 |
| mobile-home-link 문구 통일 | sudoku, typing, tetris, runner-game, space-catcher |
| 이미 완료 (이전 커밋) | tetris, balloon-pop, caterpillar-feed |
| 종료버튼 있음 (ubongo) | ubongo (btn-ghost로 이미 존재) |

#### princess-dressup thumb.svg 개선

개선된 버전으로 커밋 (더 상세한 A라인 드레스, 별 파티클, 글로우 효과 추가).

---

## 변경사항 (2026-04-25 — 버그 수정 3건, commit 00373c8)

### 테트리스 모바일 개선

- 모바일 보드 크기 확대 (viewport meta 추가)
- 버튼 확대 (min-height 56px)
- 게임오버 오버레이 추가

### 풍선 터뜨리기 (balloon-pop) 터치버그 강화

- 폭탄/풍선 터치 판정 개선

### 애벌레 먹이주기 (caterpillar-feed) 시작버튼 무반응 수정

- 시작버튼 pointerdown 이벤트 바인딩 수정

---

## 변경사항 (2026-04-19)

## 커버 이미지 통일
7개 게임 썸네일을 **통일된 디자인 시스템**으로 재제작:
- 공통 프레임 (320×180, 1px 내부 경계선, 우하단 타이틀)
- 공통 타이포그래피 (Pretendard + 한글 타이틀 + 영문 서브타이틀)
- 게임별 특성은 유지 (컬러·모티브):
  - space-catcher: 다크 네이비 + 오렌지 별
  - runner-game: 시안 러너 + 속도선
  - typing: 초록 한글 키캡
  - tetris: 테트로미노 4색 + 퍼플 그리드
  - 2048: 베이지 + 샌드 톤
  - sudoku: 슬레이트 + 보라
  - ubongo: 다크 + 앰버/에메랄드

## 루트 목록 페이지 리팩토링
**index.html / script.js / styles.css 전면 개편**:

### 기능 개선
- 시맨틱 HTML (`<main>`, `<aside>`, `<header>` 등) + ARIA 속성
- 키보드 접근성 (`focus-visible` 아웃라인)
- 스켈레톤 로더 (로딩 중 시각적 피드백)
- 외부 링크 자동 감지 및 ↗ 배지 + `target=_blank` + `rel=noopener`
- 게임 개수 표시 ("총 N개 게임")
- SVG 파비콘 인라인 추가
- `prefers-reduced-motion` 배려

### 코드 품질
- IIFE로 전역 네임스페이스 오염 방지
- `document.createElement` 기반 안전한 DOM 생성 (XSS 방지)
- 에러 처리 개선 (fetch 실패 시 명시적 빈 상태)
- CSS 변수 확장, 디자인 토큰 정리

### 반응형
- 900px 이하: 사이드바 숨김
- 480px 이하: 그리드 1컬럼
- `100dvh` 지원 (모바일 주소창 대응)

## 중복 폴더 제거
- `tetris_javascript/` 제거 (`tetris/`와 거의 동일, games.json에서 미사용)
- **원작자 MIT LICENSE 보존**: `tetris_javascript/LICENSE` (Jake Gordon, 2011-2016) → `tetris/LICENSE`로 이전

## games.json 업데이트
- 테트리스 썸네일: `tetris/texture.jpg` → `tetris/thumb.svg`
- 2048 썸네일: `2048/favicon.ico` → `2048/thumb.svg`

## 커스텀 게임 내부 리팩토링
**로직 100% 보존**, 코드 정리만 수행:

### space-catcher/script.js
- 설정값 `CONFIG` 객체로 분리 (매직 넘버 제거)
- IIFE로 감싸서 전역 오염 방지
- 상태를 `state` 객체로 일원화
- 함수 책임 분리 (`updatePlayerPosition`, `updateStars`)
- 미사용 변수 `playerX` 제거

### runner-game/script.js
- 설정값 상수화
- **버그 수정**: 깨진 이모지 문자(`�`) → 🏁
- 버튼 홀드 이벤트 중첩 문제 해결 (`bindHoldButton` 헬퍼)
- 충돌 판정 함수 분리 (`collidesWithPlayer`)
- 미사용 매개변수 정리

### typing/script.js
- 단어 목록 + 스테이지 설정을 `CONFIG.STAGES`로 통합
- 마법 숫자(10, 800) 상수화
- 상태 관리 일원화 (`state.stageIdx`, `state.wordIdx`, `state.isComposing`)
- 반복되는 `blur + value=""` 로직을 `clearInput()` 헬퍼로 통합
- 중복 코드 제거

## 우봉고 안정화
- `ResizeObserver`로 canvas 크기 변화 자동 감지
- `draw()`에서 CSS/버퍼 크기 불일치 자동 복구 → 드래그 중 잔상 완전 해결
- `clearRect`를 버퍼 크기 기준으로 지우도록 변경
- `100dvh` 적용으로 iOS 주소창 대응

## 테트리스 모바일 레이아웃 수정 (2026-04-19 추가)
모바일에서 게임 보드가 화면의 ~30%만 차지하던 문제 해결.

**근본 원인**: `tetris/index.html`에 viewport meta 태그가 없어 모바일 브라우저가 980px 데스크톱 모드로 페이지를 렌더링.

**수정사항** (모두 `tetris/index.html` CSS만 변경, 게임 로직은 무변경):
- `<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />` 추가
- 모바일 미디어 쿼리(`(pointer: coarse), (max-width: 700px)`) 전면 재작성:
  - `#menu`: `inline-block` → `flex` 가로 압축 배치 (캔버스 위)
  - `#canvas`: `min(55vw, 14rem) × min(110vw, 28rem)` — **항상 2:1 비율 유지** (테트리스 10×20 격자)
  - 모바일 컨트롤 버튼 크기·간격 조정
  - FPS 디버그 위젯 모바일에서 숨김
- 결과: iPhone 12 viewport(390×664) 기준 canvas 219×433 — 화면의 ~50% 차지

## 미변경 파일
다음은 오픈소스 기반이라 **의도적으로 건드리지 않음** (기능 회귀 리스크 방지):
- `2048/` (전체)
- `tetris/index.html`, `stats.js`, `texture.jpg`
- `sudoku/` (전체)

이 파일들은 썸네일만 새로 추가하고 기존 코드는 그대로 유지했다.

## 검증 결과

| 게임 | 런타임 에러 | 핵심 동작 |
|---|---|---|
| space-catcher | 0건 | 별 스폰 + 플레이어 이동 ✓ |
| runner-game | 0건 | 아이템 스폰 + 플레이어 위치 ✓ |
| typing | 외부 이미지 CDN 403 (원본에도 존재, 배포 환경선 정상) | 미션 표시 + 입력 ✓ |
| tetris | 0건 | 캔버스 렌더링 ✓ |
| 2048 | 0건 | 타일 컨테이너 + 새 게임 버튼 ✓ |
| sudoku | 0건 | 페이지 로드 ✓ |
| ubongo | 0건 | 인트로 화면 + 60개 퍼즐 ✓ |

---

## 배포 방법

로컬 `jangyoon-s-game/` 저장소에서:

1. 기존 파일 전체를 이 zip 내용으로 교체 (또는 덮어쓰기)
2. `tetris_javascript/` 폴더를 Git에서 제거: `git rm -r tetris_javascript`
3. 커밋 & 푸시:

```bash
git add -A
git commit -m "Refactor: unified thumbnails, modernize listing page, cleanup custom games"
git push
```

## 게임 2종 추가 (2026-06-18 굿모닝)

- **버블티 만들기 (bubble-tea-maker)** — 손님 주문대로 시럽·펄·토핑 매칭, 60초 타임어택.
- **소원등 띄우기 (lantern-float)** — 탭으로 등불 켜서 밤하늘로 띄우기, 장애물 회피.

ID는 빌드 전 games.json에 사전 예약 후 단일 작성자 fan-in(병렬 JSON 충돌 방지).
