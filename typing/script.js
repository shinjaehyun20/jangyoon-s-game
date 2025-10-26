const missionText = document.getElementById("missionText");
const userInput = document.getElementById("userInput");
const message = document.getElementById("message");
const nextBtn = document.getElementById("nextBtn");
const stageInfo = document.querySelector(".stage-info");

// 스테이지별 10개 단어
const stages = [
  ["코끼리", "장윤", "나무", "사과", "산책", "강아지", "꽃", "하늘", "비행기", "달"],
  ["학교", "친구", "책", "컴퓨터", "자동차", "바다", "산", "음악", "노래", "영화"],
  ["선생님", "연필", "책상", "의자", "시계", "달력", "창문", "문", "가방", "운동장"]
];
let currentStage = 0;
let currentWordIndex = 0;

function updateMission() {
  missionText.textContent = `한글을 입력해 보세요: ${stages[currentStage][currentWordIndex]}`;
  // 입력창 초기화를 더 강력하게 수행
  userInput.blur(); // 포커스 해제
  userInput.value = ""; // 값 초기화
  // 약간의 지연 후 포커스
  setTimeout(() => {
    userInput.focus();
  }, 10);
  message.textContent = "";
  nextBtn.style.display = "none";
  stageInfo.textContent = `스테이지 ${currentStage + 1} - 단어 ${currentWordIndex + 1} / 10`;
}

let isComposing = false; // IME 조합 상태 추적

// IME 조합 시작
userInput.addEventListener("compositionstart", () => {
  isComposing = true;
});

// IME 조합 완료
userInput.addEventListener("compositionend", () => {
  isComposing = false;
  checkAnswer();
});

// 일반 입력 체크
userInput.addEventListener("input", (e) => {
  if (!isComposing) { // IME 조합 중이 아닐 때만 체크
    checkAnswer();
  }
});

function checkAnswer() {
  if (isComposing) return; // IME 조합 중이면 체크하지 않음
  
  const answer = stages[currentStage][currentWordIndex];
  if (userInput.value === answer) {
    message.style.color = "#00e676";
    message.textContent = "정답! 🎉";
    currentWordIndex++;
    
    // 입력창 초기화를 더 안전하게 수행
    userInput.blur(); // 포커스 해제
    userInput.value = ""; // 값 초기화
    
    if (currentWordIndex < 10) {
      setTimeout(() => {
        updateMission();
      }, 800);
    } else {
      nextBtn.style.display = "block";
      message.textContent = "모든 단어를 맞췄어요! 다음 스테이지로 가요!";
    }
  } else {
    message.style.color = "#ff1744";
    message.textContent = "계속 입력하세요...";
    nextBtn.style.display = "none";
  }
}

nextBtn.addEventListener("click", () => {
  if (currentStage < stages.length - 1) {
    currentStage++;
    currentWordIndex = 0;
    updateMission();
  } else {
    missionText.textContent = "모든 스테이지를 완료했습니다! 축하해요! 🎉";
    message.textContent = "";
    userInput.style.display = "none";
    nextBtn.style.display = "none";
    stageInfo.textContent = "";
  }
});

updateMission();
