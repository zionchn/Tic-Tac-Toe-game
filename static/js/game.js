
const cells = document.querySelectorAll(".cell");
const statusMessage = document.querySelector("#status-message");
const difficultySelect = document.querySelector("#difficulty");

let currentPlayer = "X";
let gameOver = false;
let gameMode = "pvp";
let isComputerThinking = false;

let xScore = 0;
let oScore = 0;
let drawScore = 0;

const xScoreDisplay = document.querySelector("#x-score");
const oScoreDisplay = document.querySelector("#o-score");
const drawScoreDisplay = document.querySelector("#draw-score");

const restartButton = document.querySelector("#restart-btn");
const themeToggle = document.querySelector("#theme-toggle");

const pvpButton = document.querySelector("#pvp-btn");
const computerButton = document.querySelector("#computer-btn");

// All possible winning combinations
const winningCombinations = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
];

// Check if someone has won
function checkWinner() {

    for (let combination of winningCombinations) {

        const [a, b, c] = combination;

        if (
            cells[a].textContent === currentPlayer &&
            cells[b].textContent === currentPlayer &&
            cells[c].textContent === currentPlayer
        ) {

            cells[a].classList.add("winner");
            cells[b].classList.add("winner");
            cells[c].classList.add("winner");

            return true;
        }
    }

    return false;
}

// Check if the board is full
function checkDraw() {

    return [...cells].every(function(cell) {
        return cell.textContent.trim() !== "";
    });

}

// Update the scoreboard
function updateScore() {

    if (currentPlayer === "X") {
        xScore++;
        xScoreDisplay.textContent = xScore;
    } else {
        oScore++;
        oScoreDisplay.textContent = oScore;
    }

}

// Check the result after a move
function finishTurn() {

    if (checkWinner()) {

        statusMessage.textContent = `${currentPlayer === "O" && gameMode === "computer" ? "Computer" : "Player " + currentPlayer} wins! 🎉`;

        updateScore();

        gameOver = true;
        return true;
    }

    if (checkDraw()) {

        statusMessage.textContent = "It's a draw! 🤝";

        drawScore++;
        drawScoreDisplay.textContent = drawScore;

        gameOver = true;
        return true;
    }

    return false;
}

// Handle human clicks
cells.forEach(function(cell) {

    cell.addEventListener("click", async function() {

        if (
            gameOver ||
            isComputerThinking ||
            cell.textContent.trim() !== ""
        ) {
            return;
        }

        cell.textContent = currentPlayer;
        cell.classList.add("animate");

        if (finishTurn()) {
            return;
        }

        // Player vs Computer
        if (gameMode === "computer") {

            currentPlayer = "O";
            isComputerThinking = true;
            statusMessage.textContent = "Computer is thinking... 🤖";

            restartButton.disabled = true;

            await new Promise(resolve => setTimeout(resolve, 1500));

            await computerMove();

            restartButton.disabled = false;
            isComputerThinking = false;

            return;
        }

        // Player vs Player
        currentPlayer = currentPlayer === "X" ? "O" : "X";

        statusMessage.textContent = `Player ${currentPlayer}'s turn`;

    });

});

// Ask Python to choose the computer's move
async function computerMove() {

    const board = Array.from(cells).map(function(cell) {
        return cell.textContent.trim();
    });

    try {

        const response = await fetch("/computer-move", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                board: board,
                difficulty: difficultySelect.value
            })
        });

        if (!response.ok) {
            throw new Error("Could not get computer move");
        }

        const data = await response.json();

        if (
            !Number.isInteger(data.move) ||
            data.move < 0 ||
            data.move > 8 ||
            board[data.move] !== ""
        ) {
            throw new Error("Invalid computer move");
        }

        cells[data.move].textContent = "O";
        cells[data.move].classList.add("animate");

        currentPlayer = "O";

        if (finishTurn()) {
            return;
        }

        currentPlayer = "X";
        statusMessage.textContent = "Player X's turn";

    } catch (error) {

        console.error(error);
        statusMessage.textContent = "Something went wrong. Please restart.";

        gameOver = true;

    }

}

// Reset the board without resetting scores
function resetBoard() {

    cells.forEach(function(cell) {
        cell.textContent = "";
        cell.classList.remove("winner");
        cell.classList.remove("animate");
    });

    currentPlayer = "X";
    gameOver = false;

    statusMessage.textContent = "Player X's turn";

}

// Restart button
restartButton.addEventListener("click", function() {

    if (isComputerThinking) {
        return;
    }

    resetBoard();

});

// Player vs Player button
pvpButton.addEventListener("click", function() {

    if (isComputerThinking) {
        return;
    }

    gameMode = "pvp";
    resetBoard();

    statusMessage.textContent = "Player X's turn";

});

// Player vs Computer button
computerButton.addEventListener("click", function() {

    if (isComputerThinking) {
        return;
    }

    gameMode = "computer";
    resetBoard();

    statusMessage.textContent = "Your turn! You're X.";

});

// Theme toggle
themeToggle.addEventListener("click", function() {

    document.body.classList.toggle("light-theme");

    if (document.body.classList.contains("light-theme")) {
        themeToggle.textContent = "🌙 Dark Mode";
    } else {
        themeToggle.textContent = "☀️ Light Mode";
    }

});
