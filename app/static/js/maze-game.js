// Maze Game - Random Maze Generator & Player Navigation
(function() {
  var canvas = document.getElementById('mazeCanvas');
  if (!canvas) return;

  var ctx = canvas.getContext('2d');
  var CELL_SIZE = 20;
  var MAZE_WIDTH = 21;
  var MAZE_HEIGHT = 21;

  var maze = [];
  var player = { x: 1, y: 1 };
  var exit = { x: MAZE_WIDTH - 2, y: MAZE_HEIGHT - 2 };
  var isGameComplete = false;
  var startTime = null;
  var elapsedTime = 0;
  var timerInterval = null;

  // Set canvas size
  function resizeCanvas() {
    canvas.width = MAZE_WIDTH * CELL_SIZE;
    canvas.height = MAZE_HEIGHT * CELL_SIZE;
  }

  // Generate random maze using recursive backtracking
  function generateMaze() {
    // Initialize maze with all walls
    maze = Array(MAZE_HEIGHT).fill(null).map(() => Array(MAZE_WIDTH).fill(1));

    var stack = [];
    var current = { x: 1, y: 1 };
    maze[current.y][current.x] = 0;

    while (stack.length > 0 || true) {
      var neighbors = [];

      // Check all 4 directions
      var directions = [
        { x: 0, y: -2 }, // up
        { x: 2, y: 0 },  // right
        { x: 0, y: 2 },  // down
        { x: -2, y: 0 }  // left
      ];

      directions.forEach(dir => {
        var nx = current.x + dir.x;
        var ny = current.y + dir.y;
        if (nx > 0 && nx < MAZE_WIDTH - 1 && ny > 0 && ny < MAZE_HEIGHT - 1) {
          if (maze[ny][nx] === 1) {
            neighbors.push({ x: nx, y: ny, dx: dir.x, dy: dir.y });
          }
        }
      });

      if (neighbors.length > 0) {
        var next = neighbors[Math.floor(Math.random() * neighbors.length)];
        maze[current.y + next.dy / 2][current.x + next.dx / 2] = 0;
        maze[next.y][next.x] = 0;
        stack.push(current);
        current = { x: next.x, y: next.y };
      } else if (stack.length > 0) {
        current = stack.pop();
      } else {
        break;
      }
    }

    // Ensure exit is open
    maze[exit.y][exit.x] = 0;
  }

  // Draw maze
  function drawMaze() {
    ctx.fillStyle = '#f8f9fa';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw walls
    ctx.fillStyle = '#333';
    for (var y = 0; y < MAZE_HEIGHT; y++) {
      for (var x = 0; x < MAZE_WIDTH; x++) {
        if (maze[y][x] === 1) {
          ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
        }
      }
    }

    // Draw exit (goal)
    ctx.fillStyle = '#4CAF50';
    ctx.fillRect(exit.x * CELL_SIZE, exit.y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
    ctx.fillStyle = '#fff';
    ctx.font = 'bold 12px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('END', exit.x * CELL_SIZE + CELL_SIZE / 2, exit.y * CELL_SIZE + CELL_SIZE / 2);

    // Draw player
    ctx.fillStyle = '#667eea';
    ctx.beginPath();
    ctx.arc(player.x * CELL_SIZE + CELL_SIZE / 2, player.y * CELL_SIZE + CELL_SIZE / 2, CELL_SIZE / 3, 0, Math.PI * 2);
    ctx.fill();
  }

  // Update timer
  function updateTimer() {
    if (startTime) {
      elapsedTime = Math.floor((Date.now() - startTime) / 1000);
      var mins = Math.floor(elapsedTime / 60);
      var secs = elapsedTime % 60;
      document.getElementById('mazeTimer').textContent =
        (mins > 0 ? mins + 'm ' : '') + secs + 's';
    }
  }

  // Check if player won
  function checkWin() {
    if (player.x === exit.x && player.y === exit.y) {
      isGameComplete = true;
      clearInterval(timerInterval);
      showCompletion();
    }
  }

  // Move player
  function movePlayer(dx, dy) {
    var newX = player.x + dx;
    var newY = player.y + dy;

    if (newX >= 0 && newX < MAZE_WIDTH && newY >= 0 && newY < MAZE_HEIGHT) {
      if (maze[newY][newX] === 0) {
        player.x = newX;
        player.y = newY;

        if (!startTime && (dx !== 0 || dy !== 0)) {
          startTime = Date.now();
          timerInterval = setInterval(updateTimer, 100);
        }

        checkWin();
      }
    }
  }

  // Show completion message
  function showCompletion() {
    var completionDiv = document.getElementById('mazeCompletion');
    if (completionDiv) {
      var mins = Math.floor(elapsedTime / 60);
      var secs = elapsedTime % 60;
      completionDiv.innerHTML = `
        <div style="animation: slideIn 0.5s ease;">
          <p style="margin: 0 0 0.5rem 0; font-size: 1.1rem;">Congratulations!</p>
          <div class="maze-completion-time">${mins > 0 ? mins + 'm ' : ''}${secs}s</div>
          <p style="margin: 0; opacity: 0.9;">You completed the maze!</p>
        </div>
      `;
      completionDiv.style.display = 'block';
    }
  }

  // Initialize game
  function init() {
    resizeCanvas();
    generateMaze();
    isGameComplete = false;
    player = { x: 1, y: 1 };
    startTime = null;
    elapsedTime = 0;
    clearInterval(timerInterval);

    var completionDiv = document.getElementById('mazeCompletion');
    if (completionDiv) {
      completionDiv.style.display = 'none';
      completionDiv.innerHTML = '';
    }

    document.getElementById('mazeTimer').textContent = '0s';
    draw();
  }

  // Draw function
  function draw() {
    drawMaze();
    updateTimer();
    if (!isGameComplete) {
      requestAnimationFrame(draw);
    }
  }

  // Keyboard controls
  document.addEventListener('keydown', function(e) {
    if (isGameComplete) return;

    switch (e.key) {
      case 'ArrowUp':
      case 'W':
      case 'w':
        e.preventDefault();
        movePlayer(0, -1);
        break;
      case 'ArrowDown':
      case 'S':
      case 's':
        e.preventDefault();
        movePlayer(0, 1);
        break;
      case 'ArrowLeft':
      case 'A':
      case 'a':
        e.preventDefault();
        movePlayer(-1, 0);
        break;
      case 'ArrowRight':
      case 'D':
      case 'd':
        e.preventDefault();
        movePlayer(1, 0);
        break;
    }
  });

  // Mouse controls (click on canvas)
  var lastMoveTime = 0;
  canvas.addEventListener('click', function(e) {
    if (isGameComplete) return;

    var now = Date.now();
    if (now - lastMoveTime < 100) return; // Debounce
    lastMoveTime = now;

    var rect = canvas.getBoundingClientRect();
    var clickX = Math.floor((e.clientX - rect.left) / CELL_SIZE);
    var clickY = Math.floor((e.clientY - rect.top) / CELL_SIZE);

    // Move towards click
    if (Math.abs(clickX - player.x) > Math.abs(clickY - player.y)) {
      movePlayer(clickX > player.x ? 1 : -1, 0);
    } else {
      movePlayer(0, clickY > player.y ? 1 : -1);
    }
  });

  // New game button
  var newGameBtn = document.getElementById('mazeNewGameBtn');
  if (newGameBtn) {
    newGameBtn.addEventListener('click', init);
  }

  // Start the game
  init();
})();
