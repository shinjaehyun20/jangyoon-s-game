웹 스도쿠 퍼즐 게임 (Web Sudoku Puzzle Game)
======================

> HTML, CSS, JavaScript로 개발된 인터랙티브 웹 스도쿠 퍼즐 게임 - 한글 UI 적용 및 반응형 레이아웃 개선 버전

**Original Project**: [huaminghuangtw/Web-Sudoku-Puzzle-Game](https://github.com/huaminghuangtw/Web-Sudoku-Puzzle-Game)  
**Korean Localization & UI Enhancements**: 2025년 11월

---

## 주요 기능 (Features)

### 🎮 게임 플레이
- **4가지 난이도**: 쉬움, 보통, 어려움, 매우 어려움
- **시간 제한 모드**: 3분, 5분, 10분 제한 또는 스톱워치 모드
- **생명(Lives)**: 3번의 실수 기회 (하트 ❤️ 표시)
- **키보드 입력**: 타일 선택 후 키보드 1~9 입력, Backspace/Delete로 지우기
- **마우스 입력**: 타일 클릭 → 숫자 버튼 클릭 순서로 입력

### 🛠️ 도움 기능
- **힌트 (Tips)**: 각 빈 칸에 가능한 숫자 후보 표시
- **한 칸 풀기**: 한 번에 한 칸씩 자동으로 풀어줌
- **정답 보기**: 전체 정답 표시
- **퍼즐 새로고침**: 같은 난이도로 새 퍼즐 생성
- **처음부터**: 입력한 값 초기화

### 🎨 UI/UX 개선 사항
- **한글 UI**: 모든 버튼, 메시지, 안내문 한글화
- **반응형 레이아웃**: 데스크톱/모바일 화면에 자동 최적화
- **정사각형 타일**: aspect-ratio로 보드 비율 유지
- **다크/라이트 테마 토글**: 테마 전환 버튼 제공

---

## 로컬 실행 방법 (Local Setup)

### 1. 간단한 HTTP 서버로 실행
```bash
# Python 3
cd /Users/jaehyunshin/Desktop/macbookDev/sudoku
python3 -m http.server 8001
```
브라우저에서 `http://localhost:8001/` 접속

### 2. VS Code Live Server 확장 사용
1. [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) 설치
2. `index.html` 우클릭 → "Open with Live Server"

---

## 프로젝트 구조 (Project Structure)

```
sudoku/
├── index.html              # 메인 HTML (한글 UI 적용)
├── sudoku-icon.png         # 파비콘
├── README.md               # 본 문서
├── LICENSE                 # MIT 라이선스
├── CSSstyles/              # 스타일시트
│   ├── styles.css          # 메인 스타일 (반응형 개선)
│   ├── mybootstrap.css     # Bootstrap 커스텀
│   ├── digital-timer.css   # 디지털 타이머
│   ├── animated-countdown-timer.css
│   ├── progress-bar.css
│   ├── snackbar-and-alert.css
│   ├── social-media-panel.css
│   └── theme-toggle-button.css
├── JSscripts/              # JavaScript 로직
│   ├── app.js              # 메인 게임 로직 (키보드 입력 추가)
│   ├── helperSudoku.js     # 스도쿠 라이브러리 헬퍼
│   ├── utilitySudoku.js    # 보드 변환 유틸리티
│   ├── solveSudoku.js      # 백트래킹 솔버
│   ├── generateSudoku.js   # 퍼즐 생성기
│   ├── candidatesSudoku.js # 후보 숫자 계산
│   ├── countdown-timer.js  # 카운트다운 타이머
│   ├── stopwatch.js        # 스톱워치
│   └── progress-bar.js     # 진행바
├── Test_Cases/             # 난이도별 초기 퍼즐
│   ├── 9x9_easy.txt
│   ├── 9x9_medium.txt
│   └── 9x9_hard.txt
└── audio/                  # 효과음
    ├── audio-win.wav
    └── audio-lose.wav
```

---

## 기술 스택 (Tech Stack)

- **Frontend**: HTML5, CSS3 (Flexbox, Grid), Vanilla JavaScript
- **알고리즘**: 
  - 백트래킹(Backtracking) 기반 스도쿠 솔버
  - 제약 전파(Constraint Propagation)로 후보 숫자 계산
  - Rob McGuire의 스도쿠 생성 알고리즘 ([sudoku.js](https://github.com/robatron/sudoku.js))
- **라이브러리**: 
  - Bootstrap 5.1.3
  - jQuery 3.6.0
  - SweetAlert (팝업 알림)
  - Font Awesome 5.15.4 (아이콘)

---

## 개선 이력 (Changelog)

### 2025년 11월 1일
- 한글 UI 전면 적용 (난이도, 시간 선택, 버튼, 알림 메시지)
- 반응형 레이아웃 개선 (모바일/데스크톱 자동 조정)
- 키보드 입력 지원 추가 (1~9, Backspace/Delete)
- 정사각형 타일 유지 (aspect-ratio 적용)
- 보드/숫자 패드 중앙 정렬 최적화

### Original Version
- 기본 스도쿠 게임 로직 구현 (Hua-Ming Huang)
- 4가지 난이도 및 타이머 기능
- 힌트/정답보기/일시정지 기능

---

### License

This project is licensed under the terms of [![MIT](https://img.shields.io/github/license/huaminghuangtw/Web-Sudoku-Puzzle-Game.svg?style=flat-square&label=License&colorB=black)](./LICENSE).
