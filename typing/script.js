/**
 * 장윤 한글 타이핑
 * 스테이지별 10개 단어를 정확히 입력하면 진행.
 * IME(한글 입력기) 조합 상태를 고려해 검사한다.
 */

(function () {
  'use strict';

  // ================== 설정 ==================
  const CONFIG = {
    WORDS_PER_STAGE: 10,
    NEXT_WORD_DELAY: 800,   // ms
    FOCUS_DELAY: 10,        // ms
    STAGES: [
      ['코끼리', '장윤', '나무', '사과', '산책', '강아지', '꽃', '하늘', '비행기', '달'],
      ['학교', '친구', '책', '컴퓨터', '자동차', '바다', '산', '음악', '노래', '영화'],
      ['선생님', '연필', '책상', '의자', '시계', '달력', '창문', '문', '가방', '운동장'],
    ],
    COLOR_CORRECT: '#00e676',
    COLOR_TYPING: '#ff1744',
  };

  // ================== DOM ==================
  const $ = (id) => document.getElementById(id);
  const missionText = $('missionText');
  const userInput = $('userInput');
  const message = $('message');
  const nextBtn = $('nextBtn');
  const stageInfo = document.querySelector('.stage-info');

  // ================== 상태 ==================
  const state = {
    stageIdx: 0,
    wordIdx: 0,
    isComposing: false, // IME 조합 중 여부
  };

  // ================== 표시 업데이트 ==================
  function currentWord() {
    return CONFIG.STAGES[state.stageIdx][state.wordIdx];
  }

  function clearInput() {
    userInput.blur();
    userInput.value = '';
  }

  function updateMission() {
    missionText.textContent = `한글을 입력해 보세요: ${currentWord()}`;
    clearInput();
    // blur 직후 focus가 같은 프레임에서 실행되면 모바일에서 키보드가 올라오지 않을 수 있어 약간 지연
    setTimeout(() => userInput.focus(), CONFIG.FOCUS_DELAY);
    message.textContent = '';
    nextBtn.style.display = 'none';
    stageInfo.textContent =
      `스테이지 ${state.stageIdx + 1} - 단어 ${state.wordIdx + 1} / ${CONFIG.WORDS_PER_STAGE}`;
  }

  function showStageComplete() {
    nextBtn.style.display = 'block';
    message.style.color = CONFIG.COLOR_CORRECT;
    message.textContent = '모든 단어를 맞췄어요! 다음 스테이지로 가요!';
  }

  function showAllComplete() {
    missionText.textContent = '모든 스테이지를 완료했습니다! 축하해요! 🎉';
    message.textContent = '';
    userInput.style.display = 'none';
    nextBtn.style.display = 'none';
    stageInfo.textContent = '';
  }

  // ================== 정답 체크 ==================
  function checkAnswer() {
    if (state.isComposing) return; // IME 조합 중이면 검사 연기

    if (userInput.value !== currentWord()) {
      message.style.color = CONFIG.COLOR_TYPING;
      message.textContent = '계속 입력하세요...';
      nextBtn.style.display = 'none';
      return;
    }

    // 정답
    message.style.color = CONFIG.COLOR_CORRECT;
    message.textContent = '정답! 🎉';
    state.wordIdx++;
    clearInput();

    if (state.wordIdx < CONFIG.WORDS_PER_STAGE) {
      setTimeout(updateMission, CONFIG.NEXT_WORD_DELAY);
    } else {
      showStageComplete();
    }
  }

  // ================== 이벤트 ==================
  function bindInputEvents() {
    userInput.addEventListener('compositionstart', () => {
      state.isComposing = true;
    });
    userInput.addEventListener('compositionend', () => {
      state.isComposing = false;
      checkAnswer();
    });
    userInput.addEventListener('input', () => {
      if (!state.isComposing) checkAnswer();
    });
  }

  function bindNextButton() {
    nextBtn.addEventListener('click', () => {
      if (state.stageIdx < CONFIG.STAGES.length - 1) {
        state.stageIdx++;
        state.wordIdx = 0;
        updateMission();
      } else {
        showAllComplete();
      }
    });
  }

  // ================== 초기화 ==================
  bindInputEvents();
  bindNextButton();
  updateMission();
})();
