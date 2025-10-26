# PythonW Games

이 저장소는 다양한 웹 기반 미니게임 모음입니다. 각 게임은 독립적으로 실행 가능하며, HTML/CSS/JavaScript로 작성되었습니다.

## 게임 목록

- [달리는 장윤이 (runner-game)](./runner-game)
- [스페이스 캐처 (space-catcher)](./space-catcher)
- [타자 게임 (typing)](./typing)

## 실행 방법 (공통)

1. 각 게임 폴더로 이동합니다.
2. `index.html` 파일을 웹 브라우저에서 열거나, Python 내장 서버 또는 VS Code Live Server로 실행합니다.
   - Python 내장 서버 예시:
     ```powershell
     cd "게임폴더경로"
     python -m http.server 8000
     ```
   - 브라우저에서 [http://localhost:8000](http://localhost:8000) 접속

## 폴더 구조 예시
- `index.html` : 메인 HTML 파일
- `script.js` : 게임 로직
- `style.css` : 스타일시트
- `images/` : 이미지 리소스 (있는 경우)
- `README.md` : 각 게임별 설명 및 실행법

