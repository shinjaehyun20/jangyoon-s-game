우봉고 (Ubongo)
======================

> HTML, CSS, JavaScript로 개발된 폴리오미노 속도 퍼즐 게임 - 데스크톱과 모바일 모두에서 플레이 가능

**Original Board Game**: [Ubongo by Grzegorz Rejchtman (Kosmos, 2003)](https://boardgamegeek.com/boardgame/16986/ubongo)
**Web Adaptation**: 2026년 4월

---

## 주요 기능 (Features)

### 🎮 게임 플레이
- **9라운드 타임어택**: 한 게임당 9개의 퍼즐을 순차적으로 해결
- **2가지 난이도**:
  - **EASY**: 3조각 퍼즐, 60초 제한
  - **HARD**: 4조각 퍼즐, 90초 제한
- **60개 검증 퍼즐**: Easy 30 + Hard 30, 모두 풀이 가능성 사전 검증됨
- **12종 폴리오미노**: 4칸 테트로미노 6종 + 5칸 펜토미노 6종

### 💎 점수 시스템
- **시간 보너스**: 잔여 시간 × 10점
- **보석 획득**: 완성 시 4종 보석 중 랜덤 획득
  - 🔴 레드: 4점 (15% 확률)
  - 🔵 블루: 3점 (25% 확률)
  - 🟢 그린: 2점 (30% 확률)
  - 🟤 브라운: 1점 (30% 확률)
- **최고 기록 저장**: 난이도별 localStorage 저장

### 🎨 UI/UX
- **데스크톱 레이아웃**: 좌측 보드 + 우측 트레이 (1280×800 최적화)
- **모바일 레이아웃**: 상단 보드 + 하단 트레이 + 컨트롤바
- **가로모드 대응**: 낮은 높이 화면 자동 감지
- **다크 테마**: 기존 사이트 스타일과 통일, 앰버/오커 액센트
- **Canvas 2D 렌더링**: 그라디언트 타일, DPR 보정 고해상도

---

## 조작 (Controls)

| 동작 | 데스크톱 | 모바일 |
|---|---|---|
| 조각 선택/이동 | 마우스 드래그 | 터치 드래그 |
| 90도 회전 | `R` 키 | 하단 ↻ 버튼 |
| 좌우 반전 | `F` 키 | 하단 ⇆ 버튼 |
| 트레이로 되돌리기 | `Esc` 키 | 하단 ✕ 버튼 |
| 라운드 건너뛰기 | `건너뛰기` 버튼 | `건너뛰기` 버튼 |

---

## 로컬 실행 방법 (Local Setup)

### Python 내장 서버로 실행
```bash
cd ubongo
python -m http.server 8000
```
브라우저에서 [http://localhost:8000](http://localhost:8000) 접속

### VS Code Live Server
`index.html` 우클릭 → `Open with Live Server`

### 배포 주소 (GitHub Pages)
https://shinjaehyun20.github.io/jangyoon-s-game/ubongo/

---

## 폴더 구조 (Project Structure)

```
ubongo/
├── index.html        # 메인 HTML (인트로/게임/종료 3화면 전환)
├── style.css         # 반응형 스타일시트
├── pieces.js         # 12개 폴리오미노 정의 + 회전/반전 유틸 함수
├── puzzles.js        # 자동 생성된 60개 검증 퍼즐 뱅크
├── renderer.js       # Canvas 2D 렌더러 (보드, 조각, 고스트)
├── game.js           # 게임 상태 관리 + Pointer Events 입력 처리
├── thumb.svg         # 게임 목록 썸네일
└── README.md         # 이 문서
```

---

## 기술 스택 (Tech Stack)

- **순수 JavaScript (ES6+)** — 외부 라이브러리·프레임워크 의존성 없음
- **HTML5 Canvas 2D API** — 보드·조각 렌더링, 디바이스 픽셀 비율(DPR) 보정
- **Pointer Events API** — 마우스/터치/펜 입력을 단일 경로로 통합
- **CSS Grid + Media Queries** — `≥900px` / `<900px` / `<480px` / 가로모드 분기
- **localStorage** — 난이도별 최고 점수 영구 저장
- **백트래킹 솔버** — 퍼즐 뱅크 생성 시 풀이 가능성 사전 검증

---

## 개발 메모 (Development Notes)

### 퍼즐 뱅크 생성 방식
`puzzles.js`의 퍼즐들은 빌드 시점에 자동 생성된 것으로, 다음 과정을 거쳤습니다:
1. 12개 조각에서 3개(Easy) 또는 4개(Hard)를 무작위 선택
2. 7×7 가상 보드에 조각들을 연결되게 배치 (4방향 인접 보장)
3. 배치된 결과를 bounding box로 크롭하여 목표 모양(target shape) 추출
4. 백트래킹 솔버로 해당 조각 조합이 해당 모양을 완전히 덮을 수 있는지 재검증
5. 중복/비연결/크기 부적합 제거 후 각 난이도당 30개 확보

### 입력 처리 원칙
Pointer Events로 마우스·터치를 통합했으므로 코드상 분기가 없습니다. 단, 모바일 UX를 위해:
- `touch-action: none` 으로 핀치줌/스크롤 차단 (보드 영역)
- 트레이 영역은 평상시 스크롤 허용, 드래그 중에만 차단
- 하단 컨트롤바는 조각 선택 시에만 노출

### 검증 내역
- Playwright E2E 테스트로 실제 마우스 드래그 3회 → `_checkSolved() = true` 확인
- 12개 조각 회전/반전 involutive 속성(R×4 = F×2 = identity) 검증
- 60개 퍼즐 모두 솔버 통과 + 4방향 연결성 보장

---

## 라이선스 (License)
MIT License

원작 보드게임 *Ubongo*의 저작권은 Grzegorz Rejchtman 및 Kosmos에 있습니다. 이 웹 구현은 게임 메커니즘에서 영감을 받은 독립 팬메이드 작품이며, 원작의 예술 자산이나 상표를 사용하지 않았습니다.
