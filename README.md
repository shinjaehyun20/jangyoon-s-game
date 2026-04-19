# 장윤이 게임 모음 (Jangyoon's Games)

장윤이를 위한 웹 기반 미니게임 모음. 각 게임은 순수 HTML/CSS/JavaScript로 작성되어 있으며, 외부 의존성 없이 GitHub Pages에서 바로 동작한다.

🔗 **배포 주소**: <https://shinjaehyun20.github.io/jangyoon-s-game/>

## 게임 목록

| 게임 | 설명 | 카테고리 |
|---|---|---|
| [우주 장윤이 (space-catcher)](./space-catcher) | 떨어지는 별을 좌우 이동으로 잡는 액션 게임 | 액션 |
| [달리는 장윤이 (runner-game)](./runner-game) | 위/아래 이동으로 아이템을 모으는 러너 게임 | 액션 |
| [한글 타이핑 (typing)](./typing) | 한글 단어 타이핑 연습 (스테이지별) | 학습 |
| [자바스크립트 테트리스 (tetris)](./tetris) | 클래식 테트리스 | 퍼즐 |
| [2048](./2048) | 숫자 합치기 퍼즐 | 퍼즐 |
| [스도쿠 (sudoku)](./sudoku) | 9×9 숫자 퍼즐, 난이도·타이머·Lives 시스템 | 퍼즐 |
| [우봉고 (ubongo)](./ubongo) | 폴리오미노 조각 배치 속도 퍼즐 (9라운드) | 퍼즐 |

외부 링크로 게임 하나 더 포함: [한글 타이핑 (웹 배포)](https://shinjaehyun20.github.io/02-hangul-typing-game/#home)

## 프로젝트 구조

```
jangyoon-s-game/
├── index.html        # 게임 목록 페이지 (루트)
├── script.js         # 목록 페이지 로직
├── styles.css        # 목록 페이지 스타일
├── games.json        # 게임 메타데이터 (타일 렌더용)
├── menu.json         # 사이드바 메뉴 데이터
├── README.md
├── CHANGES.md        # 최근 변경사항 요약
├── space-catcher/    # 각 게임 폴더 (독립 동작)
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   ├── thumb.svg     # 게임 목록 썸네일
│   └── images/
├── runner-game/
├── typing/
├── tetris/
├── 2048/
├── sudoku/
└── ubongo/
```

각 게임 폴더는 독립 실행 가능하며, 루트 `index.html`은 `games.json`을 읽어 타일 그리드를 렌더링한다.

## 실행 방법

### 1. 바로 보기 (권장)

배포된 <https://shinjaehyun20.github.io/jangyoon-s-game/> 에서 바로 플레이.

### 2. 로컬 실행

저장소를 클론한 뒤 내장 웹서버로 띄운다. (단순히 `index.html`을 더블클릭으로 여는 것은 `fetch`로 `games.json`을 불러오지 못해 빈 화면이 뜨므로 **웹서버 경유가 필수**다.)

```powershell
# Windows PowerShell
git clone https://github.com/shinjaehyun20/jangyoon-s-game.git
cd jangyoon-s-game
python -m http.server 8000
# 브라우저에서 http://localhost:8000 접속
```

```bash
# macOS / Linux
git clone https://github.com/shinjaehyun20/jangyoon-s-game.git
cd jangyoon-s-game
python3 -m http.server 8000
```

VS Code `Live Server` 확장을 써도 된다.

## 새 게임 추가하는 법

1. 저장소 루트에 새 폴더 생성 (예: `new-game/`)
2. 그 안에 `index.html`, 필요한 자원, 그리고 `thumb.svg` 썸네일 배치
3. 루트 `games.json`에 항목 추가:
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
4. `menu.json`에도 사이드바 항목 추가
5. 커밋 & 푸시 → GitHub Pages 자동 배포

외부 호스팅 게임은 `path`에 전체 URL을 적으면 되고, 목록 페이지가 자동으로 새 탭 열기 + ↗ 배지를 붙여준다.

## 썸네일 디자인 가이드

모든 게임 썸네일은 다음 시스템을 따른다:
- **사이즈**: 320×180 viewBox (16:9)
- **프레임**: 1px 내부 경계선 `rgba(255, 255, 255, 0.08)`
- **타이틀**: 우하단 고정 — 한글 타이틀(22pt Bold) + 영문 서브타이틀(10pt, 자간 2)
- **폰트**: Pretendard / Noto Sans KR 계열
- **컬러**: 게임별 특성 유지. 다크 계열 권장, 게임 고유 액센트 1색 정도.

## 목록 페이지 기능

- **반응형**: 데스크톱(멀티컬럼) / 태블릿 / 모바일(1컬럼)
- **스켈레톤 로더**: JSON 로드 전 빈 타일 3개로 레이아웃 점프 방지
- **외부 링크 자동 감지**: `http(s)://` 경로는 새 탭 + ↗ 배지
- **접근성**: ARIA 속성, 키보드 포커스 아웃라인, `prefers-reduced-motion` 배려
- **게임 개수 표시**: 헤더에 "총 N개 게임"

## 주요 게임 설명

### 우봉고 (Ubongo)
폴리오미노 12종을 조합해 목표 모양을 완성하는 속도 퍼즐. 9라운드 구성.
- Easy(3조각 · 60초) / Hard(4조각 · 90초) 난이도 선택
- 드래그 + 회전(R / ↻) + 반전(F / ⇆) 조작
- 퍼즐 뱅크 60개(Easy 30 + Hard 30)는 백트래킹 솔버로 사전 검증된 풀이 가능 문제만 수록
- 보석 시스템(레드 4 / 블루 3 / 그린 2 / 브라운 1점) + 잔여 시간 보너스
- 최고 기록은 `localStorage`에 저장

### 스도쿠 (Sudoku)
난이도 선택(쉬움/보통/어려움), 타이머, Lives(하트 3개) 시스템 탑재. 오답 시 하트 차감.

### 한글 타이핑 (Typing)
3 스테이지 × 10 단어 구성. IME(한글 입력기) 조합 상태를 고려해 정답 판정.

## 기술 스택

- **프론트엔드 전용** — 순수 HTML5 / CSS3 / JavaScript (ES6+)
- **외부 의존성 없음** — CDN 스크립트 로드 없음 (일부 게임의 배경 이미지 제외)
- **API 사용**: `fetch`, `Canvas 2D`, `Pointer Events`, `localStorage`, `ResizeObserver`
- **호스팅**: GitHub Pages (정적)

## 최근 변경사항 (2026-04)

- **썸네일 7개 전면 재제작** — 통일된 디자인 시스템으로 일관성 확보
- **루트 목록 페이지 리팩토링** — 시맨틱 HTML, 접근성, 반응형 개선
- **중복 폴더 정리** — `tetris_javascript/` 제거 (원작자 MIT LICENSE는 `tetris/LICENSE`로 보존)
- **커스텀 게임 코드 정리** — space-catcher, runner-game, typing의 `script.js` 리팩토링 (로직은 100% 보존)
- **runner-game 버그 수정** — 게임 종료 메시지의 깨진 문자 복구
- **우봉고 안정화** — 모바일 드래그 중 캔버스 잔상 문제 해결 (ResizeObserver 적용)

자세한 내용은 [CHANGES.md](./CHANGES.md) 참조.

## 기여

새 게임을 추가하거나 개선사항이 있으면 PR을 보내주세요. 기존 게임 리팩토링 시 원본 로직을 보존하는 것을 우선합니다.

## 라이선스

- 루트 목록 페이지 및 우봉고: MIT License
- `tetris/`: MIT License (Jake Gordon, 2011-2016) — `tetris/LICENSE` 참조
- 그 외 각 게임 폴더의 라이선스는 개별 `README.md` 또는 `LICENSE` 파일 참조
