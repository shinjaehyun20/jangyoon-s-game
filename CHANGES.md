# 변경사항 요약 (2026-04-19)

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
