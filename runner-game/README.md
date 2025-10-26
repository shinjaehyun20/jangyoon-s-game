# 달리는 장윤이 (Runner Game)

이 게임은 HTML, CSS, JavaScript로 만들어진 간단한 러너 게임입니다. 아래 안내에 따라 실행하고 플레이할 수 있습니다.

## 실행 방법

1. **웹 브라우저에서 직접 실행**
   - `index.html` 파일을 더블 클릭하거나, 브라우저에서 열어 실행할 수 있습니다.

2. **로컬 서버에서 실행 (권장)**
   - 일부 브라우저에서는 보안 정책 때문에 이미지나 스크립트가 정상적으로 동작하지 않을 수 있습니다.
   - 아래 방법 중 하나로 로컬 서버를 실행하세요:

   ### Python 내장 서버 사용
   ```powershell
   cd "E:\dev aug\pythonw\games\runner-game"
   python -m http.server 8000
   ```
   - 브라우저에서 [http://localhost:8000](http://localhost:8000) 접속

   ### VS Code Live Server 확장 사용
   - VS Code에서 `index.html` 파일을 열고, 우측 하단 "Go Live" 버튼 클릭

## 게임 방법
- 시작하기 버튼을 누르면 게임이 시작됩니다.
- ↑(위) / ↓(아래) 키로 캐릭터를 이동시켜 아이템을 모으세요.
- 제한 시간 내에 최대한 많은 점수를 획득하세요.
- 모바일에서는 ▲/▼ 버튼을 터치해 조작할 수 있습니다.

## 파일 구성
- `index.html` : 게임 메인 HTML
- `script.js` : 게임 로직 JavaScript
- `style.css` : 스타일시트
- `images/` : 게임에 사용되는 이미지 리소스

---
문의: 개발자에게 직접 문의하세요.
