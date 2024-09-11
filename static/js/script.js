document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('gameForm');
    const board = document.getElementById('board');
    const resultDiv = document.getElementById('result');
    const resetButton = document.getElementById('resetGame');
    let timerInterval;

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        const x = document.getElementById('x').value;
        const y = document.getElementById('y').value;

        fetch('/play', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `x=${x}&y=${y}`
        })
            .then(response => response.json())
            .then(data => {
                resultDiv.textContent = data.result;
                updateBoard(data.board);

                if (data.game_over) {
                    clearInterval(timerInterval); // Остановить таймер при завершении игры
                    resultDiv.textContent += " Игра окончена!";
                }
            });
    });

    resetButton.addEventListener('click', function () {
        fetch('/reset', {
            method: 'POST'
        })
            .then(response => response.json())
            .then(data => {
                resetTimer();
                updateBoard(data.board);
                resultDiv.textContent = data.result;
                startTimer(); // Перезапуск таймера при начале новой игры
            });
    });

    function updateBoard(newBoard) {
        const rows = newBoard.trim().split('\n');
        for (let i = 0; i < rows.length; i++) {
            const cells = rows[i].trim().split(' ');
            for (let j = 0; j < cells.length; j++) {
                const cell = board.rows[i].cells[j];
                cell.className = cells[j].toLowerCase();
                cell.textContent = cells[j] === 'S' ? '' : cells[j];
            }
        }
    }

    function startTimer() {
        const timer = document.getElementById('timer');
        let seconds = 0;

        timerInterval = setInterval(function () {
            seconds++;
            const minutes = Math.floor(seconds / 60);
            const displaySeconds = seconds % 60;
            timer.textContent = `Время: ${String(minutes).padStart(2, '0')}:${String(displaySeconds).padStart(2, '0')}`;
        }, 1000);
    }

    function resetTimer() {
        clearInterval(timerInterval);
        const timer = document.getElementById('timer');
        timer.textContent = "Время: 00:00";
    }

    board.addEventListener('click', function (event) {
        if (event.target.tagName === 'TD') {
            const x = parseInt(event.target.getAttribute('data-x')) + 1;
            const y = parseInt(event.target.getAttribute('data-y')) + 1;

            document.getElementById('x').value = x;
            document.getElementById('y').value = y;
        }
    });

    startTimer(); // Запуск таймера при загрузке страницы
});
