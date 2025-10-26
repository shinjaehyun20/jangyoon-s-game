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

---

## 장윤이 한글 타이핑 연습 게임 🐘
- 2025.10-26추가 

초등학생을 위한 재미있는 한글 타이핑 학습 게임입니다.

### 주요 기능
- 3단계 난이도: 초급, 중급, 고급
- 점수 및 등급 시스템: S/A/B/C/D 등급
- 학습 기록 자동 저장: 최고 점수와 등급 저장
- 효과음: 정답/오답 피드백 사운드
- 애니메이션: 캐릭터 및 UI 애니메이션
- 설정 기능: 효과음, 글꼴 크기, 단어 수 조절
- 접근성: 키보드만으로 전체 조작 가능

### 실행 방법

1. `web` 폴더로 이동
2. Python 내장 서버 또는 Live Server로 실행
   - 예시:
     ```powershell
     cd web
     python -m http.server 8000
     ```
   - 브라우저에서 [http://localhost:8000](http://localhost:8000) 접속

### 폴더 구조
```
web/
├── index.html              # 메인 HTML
├── styles.css              # 전역 스타일
├── data/
│   └── words.json         # 단어 데이터
├── src/
│   ├── app.js             # 앱 진입점
│   ├── router.js          # 라우터
│   ├── utils/
│   │   ├── storage.js     # localStorage 관리
│   │   ├── sound.js       # 사운드 관리
│   │   └── grade.js       # 등급 계산
│   └── screens/
│       ├── home.js        # 홈 화면
│       ├── levelSelect.js # 레벨 선택
│       ├── game.js        # 게임 화면
│       ├── result.js      # 결과 화면
│       └── settings.js    # 설정 화면
└── README.md
```

### 등급 기준
- S등급: 100% 정확도 (완벽!)
- A등급: 90~99% 정확도
- B등급: 80~89% 정확도
- C등급: 70~79% 정확도
- D등급: 70% 미만

### 기술 스택
- 순수 JavaScript (ES6+)
- HTML5 & CSS3
- Web Audio API (사운드)
- localStorage API (데이터 저장)
- 모듈 시스템 (ES6 Modules)

### 라이선스
MIT License

---

