
// 게임 상태를 하나의 객체로 관리
const GameState = {
    inputBoard: null,
    currentBoard: null,
    candidates: null,
    solution: null,
    boardSize: 9,
    boxSize: 3,
    lives: 3,
    selectedNum: null,
    selectedTile: null,
    disableSelect: false,
    timerType: null
};

// 전역 변수 (원본 코드와의 호환성)
let board_size = 9;
let box_size = 3;
let currentBoard = null;
let solution = null;
let inputBoard = null;
let disableSelect = false;
let timerType = null;
let lives = 3;
let selectedNum = null;
let selectedTile = null;

// 유틸 함수 분리 (id, qs)
function id(id) { return document.getElementById(id); }
function qs(sel) { return document.querySelector(sel); }
function qsa(sel) { return document.querySelectorAll(sel); }


// Run script once DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // 초기화 및 이벤트 바인딩 함수 호출
    initializeSudokuLib();
    bindUIEvents();
});

function bindUIEvents() {
    id("start-btn").addEventListener("click", startGame);
    const themeBtn = id("theme-btn");
    if (themeBtn) {
        themeBtn.addEventListener("change", handleThemeToggle);
    }
    // 숫자 선택 이벤트
    const numContainer = id("number-container");
    for (let i = 0; i < numContainer.children.length; i++) {
        numContainer.children[i].addEventListener("click", handleNumberSelect);
    }
    id("solve-btn").addEventListener("click", show_solution);
    id("solve-one-step-btn").addEventListener("click", solve_one_step);
    id("refresh-btn").addEventListener("click", refresh_puzzle);
    id("restart-btn").addEventListener("click", restart_puzzle);
    id("pause-btn").addEventListener("click", pause);
    id("resume-btn").addEventListener("click", resume);
}

function handleThemeToggle(e) {
    const checked = e.target.checked;
    if (checked) {
        qs(".box").setAttribute('style', 'background-color:#CCCCCC;')
        qs(".ball").setAttribute('style', 'transform:translatex(100%);')
        document.body.classList.remove("light");
        document.body.classList.add("dark");
        qs(":root").style.setProperty('--digitColor', '#82FA58');
        qs(":root").style.setProperty('--digitBackgroundColor', '#505050');
        id("spinner-element-1").style.color = "#ff9419";
        id("spinner-element-2").style.color = "#ff9419";
        qs(".header").classList.remove("light");
        qs(".header").classList.add("dark");
    } else {
        qs(".box").setAttribute('style', 'background-color:black; color:white;')
        qs(".ball").setAttribute('style', 'transform:translatex(0%);')
        document.body.classList.remove("dark");
        document.body.classList.add("light");
        qs(":root").style.setProperty('--digitColor', 'black');
        qs(":root").style.setProperty('--digitBackgroundColor', '#EEEEEE');
        qs(".header").classList.remove("dark");
        qs(".header").classList.add("light");
    }
}

function handleNumberSelect() {
    if (disableSelect) return;
    if (this.classList.contains("selected")) {
        this.classList.remove("selected");
        selectedNum = null;
    } else {
        const numContainer = id("number-container");
        for (let i = 0; i < numContainer.children.length; i++) {
            numContainer.children[i].classList.remove("selected");
        }
        this.classList.add("selected");
        selectedNum = this;
        updateMove();
    }
}
    id("resume-btn").addEventListener("click", resume);
    // Add event listener to components of social media panel
    const floating_btn = qs(".floating-btn");
    const close_btn = qs(".close-btn");
    const social_panel_container = qs(".social-panel-container");

    // 안전 가드: 요소가 존재할 때만 이벤트 연결
    if (floating_btn && social_panel_container) {
        floating_btn.addEventListener("click", () => {
            social_panel_container.classList.toggle("visible");
        });
    } else {
        console.warn('[social-panel] \.floating-btn 또는 \.social-panel-container 가 없습니다. 토글을 건너뜁니다.');
    }

    if (close_btn && social_panel_container) {
        close_btn.addEventListener("click", () => {
            social_panel_container.classList.remove("visible");
        });
    } else {
        console.warn('[social-panel] .close-btn 또는 \.social-panel-container 가 없습니다. 닫기 연결을 건너뜁니다.');
    }

    // Keyboard input: when a tile is selected, allow typing 1-9
    const keyToId = { '1':'one','2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven','8':'eight','9':'nine' };

// 키보드 입력 이벤트는 전역에서 한 번만 바인딩
document.addEventListener('keydown', (e) => {
    if (GameState.disableSelect) return;
    // Require a tile to be selected first
    if (!GameState.selectedTile) return;
    const keyToId = { '1':'one','2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven','8':'eight','9':'nine' };
    if (keyToId[e.key]) {
        // Mirror number-button selection and apply move
        const numContainer = id("number-container");
        for (let i = 0; i < numContainer.children.length; i++) {
            numContainer.children[i].classList.remove("selected");
        }
        const numEl = id(keyToId[e.key]);
        if (numEl) {
            numEl.classList.add("selected");
            GameState.selectedNum = numEl;
            updateMove();
        }
    } else if (e.key === 'Backspace' || e.key === 'Delete') {
        // Clear the current selected tile if it is editable
        if (GameState.selectedTile && !GameState.disableSelect) {
            GameState.selectedTile.textContent = "";
        }
    }
});

function resetGame() {
    // Hide game components before loading a new puzzle
    id("game-container").style.visibility = "hidden";
    // Close alert if it exists
    if (id("alert-pause")) { $("#alert-pause").slideUp("200"); }
    // Initialize variables
    lives = 3;
    disableSelect = false;
    // Display number of lives remaining/left
    displayLives(lives);
    // Set how long the timer should be
    if (id("time-3mins").checked) {
        TIME_LIMIT = 60 * 3;
        timerType = "countdown";
    } else if (id("time-5mins").checked) {
        TIME_LIMIT = 60 * 5;
        timerType = "countdown";
    } else if (id("time-10mins").checked) {
        TIME_LIMIT = 60 * 10;
        timerType = "countdown";
    } else if (id("time-unlimited").checked) {
        // 제한 없음: 타이머 UI 자체를 숨기고 시간 표시를 하지 않음
        timerType = "none";
    } else if (id("time-stopwatch").checked) {
        timerType = "stopwatch";
    }
    // Set up elements
    if (timerType == "countdown") {
        id("time-1").classList.remove("hidden");
        id("time-2").classList.add("hidden");
        if (useProgressBar) {
            id("digital-timer-container").classList.remove("hidden");
            id("digital-timer-container").innerHTML =
                `<div id="digital-timer">
					<span class="digit"></span>
					<span class="digit"></span>
					<span class="colon"></span>
					<span class="digit"></span>
					<span class="digit"></span>
				</div>`;
            id("progress-bar-container").classList.remove("hidden");
            id("progress-bar-container").innerHTML =
                `<div id="progress-bar" class="green"></div>`;
            qs(":root").style.setProperty("--scalingFactorForTimer", "0.8");
            // Start countdown timer and progress bar
            startProgressBar();
            startTimer(TIME_LIMIT);
        } else {
            id("animated-timer-container").classList.remove("hidden");
            id("animated-timer-container").classList.add("placement");
            id("animated-timer-container").innerHTML =
                `<div class="base-timer">
				<svg class="base-timer__svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
					<g class="base-timer__circle">
						<circle class="base-timer__path-elapsed" cx="50" cy="50" r="45"></circle>
						<path
							id="base-timer-path-remaining"
							stroke-dasharray="283"
							class="base-timer__path-remaining ${remainingPathColor}"
							d="
								M 50, 50
								m -45, 0
								a 45,45 0 1,0 90,0
								a 45,45 0 1,0 -90,0
							"
						></path>
					</g>
				</svg>
				<div id="base-timer-label" class="base-timer__label">
					<span class="digit"></span>
					<span class="digit"></span>
					<span class="colon"></span>
					<span class="digit"></span>
					<span class="digit"></span>
				</div>
			</div>`;
            qs(":root").style.setProperty("--scalingFactorForTimer", "0.6");
            // Start countdown timer
            startTimer(TIME_LIMIT);
        }
    } else if (timerType == "stopwatch") {
        id("time-1").classList.add("hidden");
        id("time-2").classList.remove("hidden");
        id("stopwatch-container").classList.remove("hidden");
        id("stopwatch-container").innerHTML =
            `<div id="stopwatch">
				<span class="digit2"></span>
				<span class="digit2"></span>
				<span class="colon2"></span>
				<span class="digit2"></span>
				<span class="digit2"></span>
				<span class="colon2"></span>
				<span class="digit2"></span>
				<span class="digit2"></span>
			</div>`;
        qs(":root").style.setProperty("--scalingFactorForTimer", "0.8");
        // Start stopwatch
        startTimeCounter();
    } else if (timerType == "none") {
        // 모든 타이머 UI 숨김, 어떤 타이머도 시작하지 않음
        if (id("time-1")) id("time-1").classList.add("hidden");
        if (id("time-2")) id("time-2").classList.add("hidden");
        if (id("animated-timer-container")) {
            id("animated-timer-container").classList.add("hidden");
            id("animated-timer-container").innerHTML = "";
        }
        if (id("digital-timer-container")) {
            id("digital-timer-container").classList.add("hidden");
            id("digital-timer-container").innerHTML = "";
        }
        if (id("progress-bar-container")) {
            id("progress-bar-container").classList.add("hidden");
            id("progress-bar-container").innerHTML = "";
        }
        if (id("stopwatch-container")) {
            id("stopwatch-container").classList.add("hidden");
            id("stopwatch-container").innerHTML = "";
        }
        qs(":root").style.setProperty("--scalingFactorForTimer", "0.8");
    }
    // Show number containers
    id("number-container").classList.remove("hidden");
    // Set button accessibility
    id("solve-btn").disabled = false;
    id("solve-one-step-btn").disabled = false;
    id("refresh-btn").disabled = false;
    id("restart-btn").disabled = false;
    id("pause-btn").disabled = false;
    id("resume-btn").disabled = true;
}

function initializeGame(inputBoard) {
    generateBoard(inputBoard);
    currentBoard = board_string_to_grid(inputBoard);
    // Compute solution for the given input Sudoku board
    solution = board_grid_to_string(solveSudoku(board_string_to_grid(inputBoard)));
    // Show game components when everything is ready
    id("game-container").style.visibility = "visible";
}

function startGame() {
    // Reset setting of the game
    resetGame();
    
    // 현재 선택된 난이도 확인
    let currentDifficulty = '';
    if (id("difficulty-easy").checked) {
        currentDifficulty = 'easy';
        // 랜덤 퍼즐 선택
        inputBoard = getRandomPuzzle('easy').replace(/0/g, '.');
    } else if (id("difficulty-medium").checked) {
        currentDifficulty = 'medium';
        inputBoard = getRandomPuzzle('medium').replace(/0/g, '.');
    } else if (id("difficulty-hard").checked) {
        currentDifficulty = 'hard';
        id("spinner-container").classList.remove("hidden");
        inputBoard = getRandomPuzzle('hard').replace(/0/g, '.');
        id("spinner-container").classList.add("hidden");
    } else if (id("difficulty-veryhard").checked) {
        currentDifficulty = 'veryhard';
        inputBoard = generateSudoku("very-hard");
    }
    
    // Lives 표시 제어: 어려움 이상에서만 보임
    const livesElement = id("lives");
    if (currentDifficulty === 'hard' || currentDifficulty === 'veryhard') {
        if (livesElement) livesElement.style.display = 'block';
    } else {
        if (livesElement) livesElement.style.display = 'none';
    }
    
    // Initialize game with the given inputBoard
    initializeGame(inputBoard);
}

function endGame() {
    disableSelect = true;
    if (timerType == "countdown") {
        cancelAnimationFrame(countdown_timer);
        var t = formatTime(timeLeft).split(":");
        var m = t[0];
        var s = t[1];
        if (lives == 0 || (parseInt(m, 10) == 0 && parseInt(s, 10) == 0)) {
            var x = id("snackbar-lose");
            var audio = new Audio('./audio/audio-lose.wav');
            title_txt = "GAME OVER.😮";
        } else {
            var x = id("snackbar-win");
            var audio = new Audio('./audio/audio-win.wav');
            title_txt = "Congrats!🎉";
        }
    } else if (timerType == "stopwatch") {
        cancelAnimationFrame(stopwatch);
        if (lives == 0) {
            var x = id("snackbar-lose");
            var audio = new Audio('./audio/audio-lose.wav');
            title_txt = "GAME OVER.😮";
        } else {
            var x = id("snackbar-win");
            var audio = new Audio('./audio/audio-win.wav');
            title_txt = "Congrats!🎉";
        }
    }
    audio.play();
    x.classList.add("show");
    setTimeout(function() {
        x.classList.remove("show");
    }, 2999);
    
    // 초기화면으로 돌아가는 함수
    function resetToInitialScreen() {
        console.log('초기화면으로 이동 시작');
        
        // 혹시 남아있을 모달 닫기 (중복 안전)
        if (typeof swal === 'function') {
            try { swal.close(); } catch (e) {}
        }
        
        // 게임 보드 숨기기
        id("game-container").style.visibility = "hidden";
        id("board").style.visibility = "hidden";
        id("number-container").classList.add("hidden");
        
        // 시작 오버레이 다시 표시
        const startOverlay = id("start-overlay");
        if (startOverlay) {
            startOverlay.classList.remove("hidden");
            startOverlay.style.display = "flex";
        }
        
        // 타이머 초기화
        if (typeof timer !== 'undefined' && timer) {
            clearInterval(timer);
            timer = null;
        }
        
        // 게임 상태 초기화
        lives = 3;
        disableSelect = false;
        
        // 버튼 활성화 복구
        id("solve-btn").disabled = false;
        id("solve-one-step-btn").disabled = false;
        id("pause-btn").disabled = false;
        id("resume-btn").disabled = false;
        
        console.log('초기화면으로 이동 완료');
    }
    
    // SweetAlert 팝업
    swal({
        title: title_txt,
        text: "Try again? Press 'New game!' or 'Refresh/Restart puzzle' button.🚀",
        icon: "info",
        button: {
            text: "OK",
            closeModal: true
        },
        closeOnClickOutside: false,
        closeOnEsc: false
    }).then(() => {
        // 모달이 닫힌 직후 초기 화면으로
        resetToInitialScreen();
    });
    
    // Set button accessibility (팝업 닫힐 때까지 비활성화)
    id("solve-btn").disabled = true;
    id("solve-one-step-btn").disabled = true;
    id("pause-btn").disabled = true;
    id("resume-btn").disabled = true;
}

function readInput(file) {
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function() {
        if (rawFile.readyState === 4) {
            if (rawFile.status === 200 || rawFile.status == 0) {
                var allText = rawFile.responseText.split("\n");
                inputBoard = '';
                for (let i = 1; i < allText.length; i++) {
                    inputBoard += allText[i];
                }
                inputBoard = inputBoard.replaceAll('0', '.');
                inputBoard = inputBoard.replaceAll(' ', '');
            }
        }
    }
    rawFile.send(null);
    return inputBoard;
}

function generateBoard(board) {
    clearPrevious();
    for (let i = 0; i < board.length; i++) {
        let tile = document.createElement("p");
        if (board[i] == BLANK_CHAR) {
            tile.addEventListener("click", function() {
                if (!disableSelect) {
                    if (tile.classList.contains("selected")) {
                        tile.classList.remove("selected");
                        selectedTile = null;
                    } else {
                        let tiles = qsa(".tile");
                        for (let i = 0; i < tiles.length; i++) {
                            tiles[i].classList.remove("selected");
                        }
                        this.classList.add("selected");
                        selectedTile = tile;
                        updateMove();
                    }
                }
            });
        } else {
            tile.textContent = board[i];
        }
        tile.id = i;
        tile.classList.add("tile");
        id("board").appendChild(tile);
        let row = Math.floor(i / board_size) + 1;
        let col = i % board_size + 1;
        if (col % box_size == 0 && col != board_size) {
            tile.classList.add("rightBorder");
        }
        if (row % box_size == 0 && row != board_size) {
            tile.classList.add("bottomBorder");
        }
    }
}

function updateMove() {
    if (selectedTile && selectedNum) {
        selectedTile.textContent = selectedNum.textContent;
        if (isCorrect(selectedTile)) {
            // Update the curernt status of Sudoku board
            currentBoard[Math.floor(selectedTile.id / board_size)][selectedTile.id % board_size] =
                selectedNum.textContent;
            // Update selectedTile and selectedNum
            selectedTile.classList.remove("selected");
            selectedNum.classList.remove("selected");
            selectedTile = null;
            selectedNum = null;
            if (isDone()) { endGame(); }
        } else {
            // 오답 처리
            disableSelect = true;
            selectedTile.classList.add("incorrect");
            
            // Lives가 표시되는 경우(어려움 이상)에만 감소 및 게임 오버 체크
            const livesElement = id("lives");
            const livesEnabled = livesElement && livesElement.style.display !== 'none';
            
            setTimeout(function() {
                if (livesEnabled) {
                    lives--;
                    displayLives(lives);
                    if (lives == 0) {
                        endGame();
                        return;
                    }
                }
                disableSelect = false;
                selectedTile.classList.remove("incorrect");
                selectedTile.classList.remove("selected");
                selectedNum.classList.remove("selected");
                selectedTile.textContent = "";
                selectedTile = null;
                selectedNum = null;
            }, 1000);
        }
    }
}

function isCorrect(tile) {
    if (solution[tile.id] == tile.textContent) { return true; } else { return false; }
}

function isDone() {
    let tiles = qsa(".tile");
    for (let i = 0; i < tiles.length; i++) {
        if (tiles[i].textContent === "") return false;
    }
    return true;
}

function clearPrevious() {
    let tiles = qsa(".tile");
    for (let i = 0; i < tiles.length; i++) {
        tiles[i].remove();
    }
    for (let i = 0; i < id("number-container").children.length; i++) {
        id("number-container").children[i].classList.remove("selected");
    }
    selectedTile = null;
    selectedNum = null;
}

function displayLives(lives) {
    if (lives == 0) {
        id("lives").textContent = "Lives: 0";
    } else {
        id("lives").textContent = "Lives: " + "🖤".repeat(lives);
    }
}

function display_tips() {
    // Get and print candidates of each empty cell on the current board
    candidates = get_candidates(board_grid_to_string(currentBoard));
    console.log(board_grid_to_display_string(candidates));
    qs(".toast-body").textContent = board_grid_to_display_string(candidates);
    // Initialize bootstrap toast instance
    var myToast = new bootstrap.Toast(id("myToast"), {
        delay: 3000
    });
    myToast.show();
}

function show_solution() {
    // Display solution to the current Sudoku puzzle, highlighting the answers with green color
    for (let i = 0; i < id("board").children.length; i++) {
        var tile = id("board").children[i];
        if (tile.textContent != solution[tile.id]) {
            tile.textContent = solution[tile.id];
            // Update the curernt status of Sudoku board
            currentBoard[Math.floor(tile.id / board_size)][tile.id % board_size] = solution[tile.id];
            tile.classList.add("green-text");
        }
    }
    // Display solution to the console
    console.log(board_string_to_display_string(solution));
    // Pause countdown timer or stopwatch
    pause();
    // Set button accessibility
    id("solve-btn").disabled = true;
    id("solve-one-step-btn").disabled = true;
    id("resume-btn").disabled = true;
    // Display message to the user
    swal({
        title: "Try again?😉",
        text: "Press 'New game!' or 'Refresh/Restart puzzle' button.🚀",
        icon: "info",
        button: {
            text: "OK",
            closeModal: true
        },
        closeOnClickOutside: true,
        closeOnEsc: true
    }).then(() => {
        // 다이얼로그 닫힌 후, 새 게임을 바로 시작하지는 않지만
        // 사용자가 하단의 '새 게임!' 버튼을 누를 수 있도록 UI가 완전히 활성 상태임을 보장
        // 별도의 상태 변경은 불필요 (start-btn은 기본적으로 활성)
    });
}

function solve_one_step() {
    for (let i = 0; i < id("board").children.length; i++) {
        var tile = id("board").children[i];
        // 현재 타일이 비어있고, solution에 답이 있으면 채움
        if (tile.textContent === "" || tile.textContent === ".") {
            if (solution[tile.id] && solution[tile.id] !== "." && solution[tile.id] !== " ") {
                tile.textContent = solution[tile.id];
                // Update the current status of Sudoku board
                currentBoard[Math.floor(tile.id / board_size)][tile.id % board_size] = solution[tile.id];
                tile.classList.add("green-text");
                break;
            }
        }
    }
}

function refresh_puzzle() {
    // Reset setting of the game
    resetGame();
    // Choose board difficulty and initialize the Sudoku board accordingly
    if (id("difficulty-easy").checked) {
        inputBoard = getRandomPuzzle('easy').replace(/0/g, '.');
    } else if (id("difficulty-medium").checked) {
        inputBoard = getRandomPuzzle('medium').replace(/0/g, '.');
    } else if (id("difficulty-hard").checked) {
        inputBoard = getRandomPuzzle('hard').replace(/0/g, '.');
    } else if (id("difficulty-veryhard").checked) {
        inputBoard = generateSudoku("very-hard");
    }
    // Initialize game with the given inputBoard
    initializeGame(inputBoard);
}

function restart_puzzle() {
    resetGame();
    initializeGame(inputBoard);
}

function pause() {
    disableSelect = true;
    if (timerType == "countdown") {
        pauseTimer();
    } else if (timerType == "stopwatch") {
        pauseTimeCounter();
    }
    // Set button accessibility
    id("solve-btn").disabled = true;
    id("solve-one-step-btn").disabled = true;
}

function resume() {
    disableSelect = false;
    if (timerType == "countdown") {
        resumeTimer();
    } else if (timerType == "stopwatch") {
        resumeTimeCounter();
    }
    // Set button accessibility
    id("solve-btn").disabled = false;
    id("solve-one-step-btn").disabled = false;
}

// Helper functions
function id(id) {
    return document.getElementById(id);
}

function qs(selectors) {
    return document.querySelector(selectors);
}

function qsa(selectors) {
    return document.querySelectorAll(selectors);
}

function setIntervalImmediately(func, interval) {
    func();
    return setInterval(func, interval);
}

// In JavaScript, strings are immutable.
// You cannot do an in-place replacement, but creating a new string and returns it.
function setCharAt(str, index, chr) {
    if (index > str.length - 1) return str;
    return str.substring(0, index) + chr + str.substring(index + 1);
}