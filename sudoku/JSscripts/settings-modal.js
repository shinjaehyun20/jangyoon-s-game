/**
 * Settings Modal Handler
 * Manages difficulty, time selection modals and pause functionality
 */

// 난이도 아이콘 매핑
const difficultyIcons = {
    'easy': 'fa-dice-one',
    'medium': 'fa-dice-two',
    'hard': 'fa-dice-three',
    'veryhard': 'fa-dice-four'
};

// 난이도 텍스트 매핑
const difficultyText = {
    'easy': '쉬움',
    'medium': '보통',
    'hard': '어려움',
    'veryhard': '매우 어려움'
};

// 시간 아이콘 매핑
const timeIcons = {
    'three': 'fa-hourglass-start',
    'five': 'fa-hourglass-start',
    'ten': 'fa-hourglass-start',
    'unlimited': 'fa-infinity',
    'stopwatch': 'fa-stopwatch'
};

// 시간 텍스트 매핑
const timeText = {
    'three': '3분',
    'five': '5분',
    'ten': '10분',
    'stopwatch': '스톱워치',
    'unlimited': '제한없음'
};

// 게임 상태
let isGamePaused = false;
let isGameStarted = false;
// 옵션(난이도/시간) 변경 여부 플래그: 변경 후 재개 버튼을 누르면 새 게임으로 반영
let settingsChanged = false;
// 인트로 모달 표시 여부
let introShown = false;

// 모달 열기
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // 스크롤 방지
    }
}

// 모달 닫기
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = ''; // 스크롤 복원
    }
}

// 일시정지
function pauseGame() {
    if (!isGameStarted || isGamePaused) return;
    
    isGamePaused = true;
    
    // 오버레이 표시
    const overlay = document.getElementById('pause-overlay');
    if (overlay) {
        overlay.classList.add('active');
    }
    
    // 보드 딤 처리
    const board = document.getElementById('board');
    if (board) {
        board.classList.add('dimmed');
    }
    
    // 상단 일시정지 알림 숨김
    const alertPause = document.getElementById('alert-pause');
    if (alertPause) {
        alertPause.classList.add('hidden');
    }
    
    // 기존 일시정지 버튼 클릭 (타이머 멈춤)
    const originalPauseBtn = document.querySelector('#pause-btn.btn-secondary');
    if (originalPauseBtn && !originalPauseBtn.disabled) {
        originalPauseBtn.click();
    }
}

// 재개
function resumeGame() {
    console.log('resumeGame 함수 호출됨');
    if (!isGamePaused) {
        console.log('게임이 일시정지 상태가 아님');
        return;
    }

    // 오버레이/딤 먼저 정리
    isGamePaused = false;

    const overlay = document.getElementById('pause-overlay');
    if (overlay) overlay.classList.remove('active');

    const board = document.getElementById('board');
    if (board) board.classList.remove('dimmed');

    // 옵션 변경이 있었다면: 새 게임으로 재시작(현재 라디오 선택값 반영)
    if (settingsChanged) {
        const startBtn = document.getElementById('start-btn');
        if (startBtn) startBtn.click();
        settingsChanged = false;
        return; // 타이머 재개 불필요(새 게임 시작)
    }

    // 옵션 변경이 없다면: 기존처럼 타이머 재개만 수행
    const originalResumeBtn = document.querySelector('#resume-btn.btn-secondary');
    if (originalResumeBtn && !originalResumeBtn.disabled) {
        originalResumeBtn.click();
    }
}

// 다시하기 (처음부터)
function restartGame() {
    const restartBtn = document.getElementById('restart-btn');
    if (restartBtn) {
        restartBtn.click();
    }
    closeModal('settings-menu-modal');
}

// 뒤로 가기 (모달 닫기)
function goBack(modalId) {
    closeModal(modalId);
}

// 이벤트 리스너 설정
document.addEventListener('DOMContentLoaded', function() {
    console.log('Settings modal JS 로드됨');
    
    // 인트로 모달 처리
    const introModal = document.getElementById('intro-modal');
    const introStartBtn = document.getElementById('intro-start-btn');
    
    // 인트로 "시작하기" 버튼
    if (introStartBtn) {
        introStartBtn.addEventListener('click', () => {
            // 인트로 모달 닫기
            if (introModal) {
                introModal.classList.remove('active');
                introShown = true;
            }
            // 게임 시작
            const startBtn = document.getElementById('start-btn');
            if (startBtn) {
                startBtn.click();
            }
        });
    }
    
    // 인트로에서 난이도/시간 선택 시 해당 모달 열기
    const introDifficultyBtn = document.querySelector('[data-action="intro-difficulty"]');
    if (introDifficultyBtn) {
        introDifficultyBtn.addEventListener('click', () => {
            openModal('difficulty-modal');
        });
    }
    
    const introTimeBtn = document.querySelector('[data-action="intro-time"]');
    if (introTimeBtn) {
        introTimeBtn.addEventListener('click', () => {
            openModal('time-modal');
        });
    }
    
    // 옵션 버튼
    const settingsBtn = document.getElementById('settings-btn');
    if (settingsBtn) {
        settingsBtn.addEventListener('click', () => {
            // 옵션을 열 때는 항상 타이머를 잠시 멈춤 (요구사항 반영)
            try { pauseGame(); } catch (e) {}
            openModal('settings-menu-modal');
        });
    }
    
    // 헤더 일시정지 버튼
    const headerPauseBtn = document.querySelector('#pause-btn.control-btn');
    if (headerPauseBtn) {
        headerPauseBtn.addEventListener('click', pauseGame);
    }
    
    // 재개하기 버튼 (오버레이 버튼)
    const resumeBtnOverlay = document.getElementById('resume-overlay-btn');
    if (resumeBtnOverlay) {
        resumeBtnOverlay.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            console.log('재개 버튼 클릭됨! 이벤트:', e);
            resumeGame();
        });
    }
    
    // 추가: pause-overlay 클릭으로도 재개 가능하게
    const pauseOverlay = document.getElementById('pause-overlay');
    if (pauseOverlay) {
        pauseOverlay.addEventListener('click', function(e) {
            // 오버레이 배경 클릭 시 (버튼이 아닌 경우)
            if (e.target === pauseOverlay) {
                console.log('오버레이 배경 클릭됨');
                resumeGame();
            }
        });
    }
    
    // 옵션 메뉴 아이템들
    const menuItems = document.querySelectorAll('.settings-menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            const action = this.getAttribute('data-action');
            
            switch(action) {
                case 'difficulty':
                    closeModal('settings-menu-modal');
                    setTimeout(() => openModal('difficulty-modal'), 300);
                    break;
                case 'time':
                    closeModal('settings-menu-modal');
                    setTimeout(() => openModal('time-modal'), 300);
                    break;
                case 'restart':
                    restartGame();
                    break;
                case 'back':
                    closeModal('settings-menu-modal');
                    break;
            }
        });
    });
    
    // 뒤로 버튼들
    const backButtons = document.querySelectorAll('.modal-back-btn');
    backButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const modalId = this.getAttribute('data-modal');
            if (modalId) {
                goBack(modalId);
            }
        });
    });
    
    // 모달 닫기 버튼들
    const closeButtons = document.querySelectorAll('.modal-close');
    closeButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const modalId = this.getAttribute('data-modal');
            closeModal(modalId);
        });
    });
    
    // 모달 배경 클릭 시 닫기
    const modals = document.querySelectorAll('.settings-modal');
    modals.forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal(this.id);
            }
        });
    });
    
    // ESC 키로 모달 닫기
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const activeModal = document.querySelector('.settings-modal.active');
            if (activeModal) {
                closeModal(activeModal.id);
            } else if (isGamePaused) {
                resumeGame();
            }
        }
    });
    
    // 난이도 선택 변경 시
    const difficultyInputs = document.querySelectorAll('input[name="diff"]');
    difficultyInputs.forEach(input => {
        input.addEventListener('change', function() {
            settingsChanged = true;
            // 선택 후 0.5초 뒤 모달 자동 닫기
            setTimeout(() => {
                closeModal('difficulty-modal');
                // 인트로 모달이 활성화되어 있으면 다시 보여주기
                if (introModal && !introShown) {
                    introModal.classList.add('active');
                }
            }, 500);
        });
    });
    
    // 시간 선택 변경 시
    const timeInputs = document.querySelectorAll('input[name="time"]');
    timeInputs.forEach(input => {
        input.addEventListener('change', function() {
            settingsChanged = true;
            // 선택 후 0.5초 뒤 모달 자동 닫기
            setTimeout(() => {
                closeModal('time-modal');
                // 인트로 모달이 활성화되어 있으면 다시 보여주기
                if (introModal && !introShown) {
                    introModal.classList.add('active');
                }
            }, 500);
        });
    });
    
    // 게임 시작 감지
    const startBtn = document.getElementById('start-btn');
    if (startBtn) {
        startBtn.addEventListener('click', function() {
            isGameStarted = true;
            isGamePaused = false;
            settingsChanged = false; // 새 게임 시작 시 플래그 초기화
            
            // 일시정지 버튼 표시
            const pauseBtn = document.querySelector('#pause-btn.control-btn');
            if (pauseBtn) {
                pauseBtn.style.display = 'flex';
            }
            
            // 보드 위 시작 오버레이 숨김
            const startOverlay = document.getElementById('start-overlay');
            if (startOverlay) {
                startOverlay.classList.add('hidden');
            }
        });
    }
    
    // 보드 위 시작 버튼
    const startOverlayBtn = document.getElementById('start-overlay-btn');
    if (startOverlayBtn) {
        startOverlayBtn.addEventListener('click', function() {
            // 하단 시작 버튼 클릭
            const startBtn = document.getElementById('start-btn');
            if (startBtn) {
                startBtn.click();
            }
        });
    }
    
    // 기존 컨트롤 숨기기
    const observer = new MutationObserver(() => {
        // 기존 버튼 그룹들 숨기기
        const btnGroups = document.querySelectorAll('.btn-group');
        btnGroups.forEach(group => {
            const refreshBtn = group.querySelector('#refresh-btn');
            const restartBtn = group.querySelector('#restart-btn');
            const pauseBtn = group.querySelector('#pause-btn.btn-secondary');
            const resumeBtn = group.querySelector('#resume-btn.btn-secondary');
            
            if (refreshBtn || restartBtn || pauseBtn || resumeBtn) {
                group.style.display = 'none';
            }
        });
    });
    
    observer.observe(document.body, { childList: true, subtree: true });
});
