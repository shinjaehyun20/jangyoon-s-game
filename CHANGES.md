# 변경 이력

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
