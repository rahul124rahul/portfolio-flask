// Number Path Game - Connect Numbers in Order
(function() {
  var gameContainer = document.getElementById('numberGameContainer');
  if (!gameContainer) return;

  var GRID_SIZE = 4;
  var cells = [];
  var nextNumber = 1;
  var isGameComplete = false;
  var startTime = null;
  var elapsedTime = 0;
  var timerInterval = null;

  // Initialize game
  function initGame() {
    // Generate random numbers
    var numbers = [];
    for (var i = 1; i <= GRID_SIZE * GRID_SIZE; i++) {
      numbers.push(i);
    }

    // Shuffle array
    for (var i = numbers.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var temp = numbers[i];
      numbers[i] = numbers[j];
      numbers[j] = temp;
    }

    // Clear grid
    var gridContainer = document.getElementById('gameGrid');
    gridContainer.innerHTML = '';
    cells = [];
    nextNumber = 1;
    isGameComplete = false;
    startTime = null;
    elapsedTime = 0;
    clearInterval(timerInterval);

    // Create cells
    for (var i = 0; i < numbers.length; i++) {
      var cell = document.createElement('div');
      cell.className = 'game-cell';
      cell.textContent = numbers[i];
      cell.dataset.number = numbers[i];
      cell.addEventListener('click', function() {
        handleCellClick(this);
      });

      if (i === 0) {
        cell.classList.add('next');
      }

      cells.push(cell);
      gridContainer.appendChild(cell);
    }

    // Hide completion message
    var completionDiv = document.getElementById('gameCompletion');
    if (completionDiv) {
      completionDiv.style.display = 'none';
      completionDiv.innerHTML = '';
    }

    document.getElementById('gameTimer').textContent = '0s';
    updateStats();
  }

  // Handle cell click
  function handleCellClick(cell) {
    if (isGameComplete) return;

    var number = parseInt(cell.dataset.number);

    // Start timer on first click
    if (!startTime) {
      startTime = Date.now();
      timerInterval = setInterval(updateTimer, 100);
    }

    // Check if correct number
    if (number === nextNumber) {
      cell.classList.add('connected');
      cell.classList.remove('next');
      nextNumber++;
      updateStats();

      // Check if game is complete
      if (nextNumber > GRID_SIZE * GRID_SIZE) {
        completeGame();
      } else {
        // Highlight next number
        cells.forEach(function(c) {
          if (parseInt(c.dataset.number) === nextNumber) {
            c.classList.add('next');
          }
        });
      }
    }
  }

  // Update timer
  function updateTimer() {
    if (startTime) {
      elapsedTime = Math.floor((Date.now() - startTime) / 1000);
      var mins = Math.floor(elapsedTime / 60);
      var secs = elapsedTime % 60;
      document.getElementById('gameTimer').textContent =
        (mins > 0 ? mins + 'm ' : '') + secs + 's';
    }
  }

  // Update stats display
  function updateStats() {
    var connected = nextNumber - 1;
    var remaining = GRID_SIZE * GRID_SIZE - connected;
    document.getElementById('connectedCount').textContent = connected;
    document.getElementById('remainingCount').textContent = remaining;
  }

  // Complete game
  function completeGame() {
    isGameComplete = true;
    clearInterval(timerInterval);

    var completionDiv = document.getElementById('gameCompletion');
    if (completionDiv) {
      var mins = Math.floor(elapsedTime / 60);
      var secs = elapsedTime % 60;
      completionDiv.innerHTML = `
        <div class="completion-message">Congratulations!</div>
        <div class="completion-time">${mins > 0 ? mins + 'm ' : ''}${secs}s</div>
        <div style="font-size: 1rem; opacity: 0.9;">You connected all numbers perfectly!</div>
      `;
      completionDiv.style.display = 'block';
    }
  }

  // New game button
  var newGameBtn = document.getElementById('numberNewGameBtn');
  if (newGameBtn) {
    newGameBtn.addEventListener('click', initGame);
  }

  // Start the game
  initGame();
})();
