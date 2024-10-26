var generation, finished = true, current, path, paths, grids = []
const breakWallChance = 0.01, splitChance = 0.1

function generateMaze_backtracker() {
	grid.start.setCol(grid.grid[0][0])
	grid.end.setCol(grid.grid[grid.grid.length-1][grid.grid[grid.grid.length-1].length - 1])
	for (let j = 0; j < grid.grid.length; j++) {
		for (let i = 0; i < grid.grid[j].length; i++) {
			grid.grid[j][i].setType('wall')
		}
	}
	finished = false
	current = grid.grid[0][0]
	path = [current]

	backtrackerStep()
}
function backtrackerStep() {

	if (stopGenerate) {
		stopGenerate = false
		return false
	}

	path.push(current)

	let pool = []
	// Top - y-1
	if (current.y > 0 && grid.grid[current.y - 1][current.x].type === 'wall' && backtracker_checkNeighbors(current.x, current.y - 1, 'u') && current.x > 0) {
		pool.push(grid.grid[current.y - 1][current.x])
	}
	// Left - x-1
	if (current.x > 0 && grid.grid[current.y][current.x - 1].type === 'wall' && backtracker_checkNeighbors(current.x - 1, current.y, 'l') && current.y > 0) {
		pool.push(grid.grid[current.y][current.x - 1])
	}
	// Bottom - y+1
	if (current.y < grid.rows - 1 && grid.grid[current.y + 1][current.x].type === 'wall' && backtracker_checkNeighbors(current.x, current.y + 1, 'd')) {
		pool.push(grid.grid[current.y + 1][current.x])
	}
	// Right - x+1s
	if (current.x < grid.cols - 1 && grid.grid[current.y][current.x + 1].type === 'wall' && backtracker_checkNeighbors(current.x + 1, current.y, 'r')) {
		pool.push(grid.grid[current.y][current.x + 1])
	}

	//Backtracking
	if (pool.length === 0) {
		if ((current.x === 0 && current.y === 0) || path.length === 0) {
			finished = true
			backtracker_clear()
			return false
		}
		current.setType('empty')
		path.pop()
		current = path.pop()
		setTimeout(backtrackerStep, map(speed.value, 0, 100, 500, 20))
		return false
	}

	let rand = pool[Math.floor(Math.random()*pool.length)];

	current = rand
	current.setType('path')

	setTimeout(backtrackerStep, map(speed.value, 0, 100, 500, 20))
}

function generateMaze_backtracker_multi() {
	console.log('Generating backtracker-multi')
	grid.start.setCol(grid.grid[0][0])
	grid.end.setCol(grid.grid[grid.grid.length-1][grid.grid[grid.grid.length-1].length - 1])
	for (let j = 0; j < grid.grid.length; j++) {
		for (let i = 0; i < grid.grid[j].length; i++) {
			grid.grid[j][i].setType('wall')
		}
	}
	finished = false
	paths = [[grid.grid[0][0]]]

	backtrackerMultiStep()

}
function backtrackerMultiStep() {

	if (stopGenerate) {
		stopGenerate = false
		return false
	}

	for (let i = paths.length-1; i >= 0; i--) {

		if (paths[i].length === 0) {
			if (paths.length === 1) {
				finished = true
				backtracker_clear()
				return false;
			}
			else {
				paths.splice(i, 1)
			}
			continue
		}

		let currentCol = paths[i][paths[i].length-1]

		let pool = []
		// Top - y-1
		if (currentCol.y > 0 && grid.grid[currentCol.y - 1][currentCol.x].type === 'wall' && backtracker_checkNeighbors(currentCol.x, currentCol.y - 1, 'u') && currentCol.x > 0) {
			pool.push(grid.grid[currentCol.y - 1][currentCol.x])
		}
		// Left - x-1
		if (currentCol.x > 0 && grid.grid[currentCol.y][currentCol.x - 1].type === 'wall' && backtracker_checkNeighbors(currentCol.x - 1, currentCol.y, 'l') && currentCol.y > 0) {
			pool.push(grid.grid[currentCol.y][currentCol.x - 1])
		}
		// Bottom - y+1
		if (currentCol.y < grid.rows - 1 && grid.grid[currentCol.y + 1][currentCol.x].type === 'wall' && backtracker_checkNeighbors(currentCol.x, currentCol.y + 1, 'd')) {
			pool.push(grid.grid[currentCol.y + 1][currentCol.x])
		}
		// Right - x+1s
		if (currentCol.x < grid.cols - 1 && grid.grid[currentCol.y][currentCol.x + 1].type === 'wall' && backtracker_checkNeighbors(currentCol.x + 1, currentCol.y, 'r')) {
			pool.push(grid.grid[currentCol.y][currentCol.x + 1])
		}

		//Backtracking
		if (pool.length === 0) {
			if (paths[i].length === 0) {
				if (paths.length === 1) {
					finished = true
					backtracker_clear()
					return false
				}
				else {
					paths.splice(i, 1)
				}
				continue
			}
			currentCol.setType('empty')
			currentCol = paths[i].pop()
			continue
		}

		let randI = Math.floor(Math.random()*pool.length)
		let rand = pool[randI];
		pool.splice(randI, 1)

		rand.setType('path')
		paths[i].push(rand)

		if (pool.length > 0 && Math.random() < splitChance/paths.length) {
			let randI = Math.floor(Math.random()*pool.length)
			let rand = pool[randI];
			let path = []
			rand.setType('path')
			path.push(rand)
			paths.push(path)
		}
	}

	setTimeout(backtrackerMultiStep, map(speed.value, 0, 100, 500, 20))
}

function backtracker_checkNeighbors(x, y, move = null) {

	if (x > 0) {
		// Top left corner
		if (y > 0) {
			if (grid.grid[y][x-1].type !== 'wall' && grid.grid[y-1][x].type !== 'wall' && grid.grid[y-1][x-1].type !== 'wall') {
				return false
			}
		}
		// Bottom left corner
		if (y < grid.rows - 1) {
			if (grid.grid[y][x-1].type !== 'wall' && grid.grid[y+1][x].type !== 'wall' && grid.grid[y+1][x-1].type !== 'wall') {
				return false
			}
		}
	}
	if (x < grid.cols - 1) {
		// Top right corner
		if (y > 0) {
			if (grid.grid[y][x+1].type !== 'wall' && grid.grid[y-1][x].type !== 'wall' && grid.grid[y-1][x+1].type !== 'wall') {
				return false
			}
		}
		// Bottom right corner
		if (y < grid.rows - 1) {
			if (grid.grid[y][x+1].type !== 'wall' && grid.grid[y+1][x].type !== 'wall' && grid.grid[y+1][x+1].type !== 'wall') {
				return false
			}
		}
	}

	if (move) {return backtracker_checkWallBreak(x,y,move)}
	return true

}
function backtracker_checkWallBreak(x, y, move) {
	let r = Math.random()
	switch (move) {
		case 'u':
			if (x > 0 && y > 0 && x < grid.cols-1 && (grid.grid[y][x-1].type !== 'wall' || grid.grid[y][x+1].type !== 'wall' || grid.grid[y-1][x].type !== 'wall')) {
				if (r >= breakWallChance) {
					return false
				}
			}
			else if (x > 0 && y > 0 && x >= grid.cols-1 && (grid.grid[y][x-1].type !== 'wall' || grid.grid[y-1][x].type !== 'wall')) {
				if (r >= breakWallChance) {
					return false
				}
			}
			else if (x > 0 && y <= 0 && x < grid.cols-1 && (grid.grid[y][x-1].type !== 'wall' || grid.grid[y][x+1].type !== 'wall')) {
				if (r >= breakWallChance) {
					return false
				}
			}
			else if (x <= 0 && y > 0 && x < grid.cols-1 && (grid.grid[y][x+1].type !== 'wall' || grid.grid[y-1][x].type !== 'wall')) {
				if (r >= breakWallChance) {
					return false
				}
			}
			break;
		case 'l':
			if (x > 0 && y > 0 && y < grid.rows-1 && (grid.grid[y][x-1].type !== 'wall' || grid.grid[y-1][x].type !== 'wall' || grid.grid[y+1][x].type !== 'wall')) {
				if (r >= breakWallChance) {
					return false
				}
			}
			else if (x > 0 && y > 0 && y >= grid.rows-1 && (grid.grid[y][x-1].type !== 'wall' || grid.grid[y-1][x].type !== 'wall')) {
				if (r >= breakWallChance) {
					return false
				}
			}
			else if (x > 0 && y <= 0 && y < grid.rows-1 && (grid.grid[y][x-1].type !== 'wall' || grid.grid[y+1][x].type !== 'wall')) {
				if (r >= breakWallChance) {
					return false
				}
			}
			else if (x <= 0 && y > 0 && y < grid.rows-1 && (grid.grid[y-1][x].type !== 'wall' || grid.grid[y+1][x].type !== 'wall')) {
				if (r >= breakWallChance) {
					return false
				}
			}
			break;
		case 'd':
			if (x > 0 && y < grid.rows-1 && x < grid.cols-1 && (grid.grid[y][x-1].type !== 'wall' || grid.grid[y+1][x].type !== 'wall' || grid.grid[y+1][x].type !== 'wall')) {
				if (r >= breakWallChance) {
					return false
				}
			}
			else if (x > 0 && y < grid.rows-1 && x >= grid.cols-1 && (grid.grid[y][x-1].type !== 'wall' || grid.grid[y+1][x].type !== 'wall')) {
				if (r >= breakWallChance) {
					return false
				}
			}
			else if (x > 0 && y >= grid.rows-1 && x < grid.cols-1 && (grid.grid[y][x-1].type !== 'wall' || grid.grid[y][x+1].type !== 'wall')) {
				if (r >= breakWallChance) {
					return false
				}
			}
			else if (x <= 0 && y < grid.rows-1 && x < grid.cols-1 && (grid.grid[y+1][x].type !== 'wall' || grid.grid[y][x+1].type !== 'wall')) {
				if (r >= breakWallChance) {
					return false
				}
			}
			break;
		case 'r':
			if (x < grid.cols-1 && y > 0 && y < grid.rows-1 && (grid.grid[y][x+1].type !== 'wall' || grid.grid[y-1][x].type !== 'wall' || grid.grid[y+1][x].type !== 'wall')) {
				if (r >= breakWallChance) {
					return false
				}
			}
			else if (x < grid.cols-1 && y > 0 && y >= grid.rows-1 && (grid.grid[y][x+1].type !== 'wall' || grid.grid[y-1][x].type !== 'wall')) {
				if (r >= breakWallChance) {
					return false
				}
			}
			else if (x < grid.cols-1 && y <= 0 && y < grid.rows-1 && (grid.grid[y][x+1].type !== 'wall' || grid.grid[y+1][x].type !== 'wall')) {
				if (r >= breakWallChance) {
					return false
				}
			}
			else if (x >= grid.cols-1 && y > 0 && y < grid.rows-1 && (grid.grid[y-1][x].type !== 'wall' || grid.grid[y+1][x].type !== 'wall')) {
				if (r >= breakWallChance) {
					return false
				}
			}
			break;
	}
	return true
}
function backtracker_clear() {
	for (let j = 0; j < grid.grid.length; j++) {
		for (let i = 0; i < grid.grid[j].length; i++) {
			if (grid.grid[j][i].type !== 'wall') {grid.grid[j][i].setType('empty')}
		}
	}
	grid.start.setCol(grid.grid[0][0])
	grid.end.setCol(grid.grid[grid.grid.length-1][grid.grid[grid.grid.length-1].length - 1])
}

function generateMaze_huntAndKill() {
	grid.start.setCol(grid.grid[0][0])
	grid.end.setCol(grid.grid[grid.grid.length-1][grid.grid[grid.grid.length-1].length - 1])
	for (let j = 0; j < grid.grid.length; j++) {
		for (let i = 0; i < grid.grid[j].length; i++) {
			grid.grid[j][i].setType('wall')
		}
	}
	finished = false
	current = grid.grid[0][0]
	huntAndKillStep()
}
function huntAndKillStep() {

	if (stopGenerate) {
		stopGenerate = false
		return false
	}

	let pool = []
	// Top - y-1
	if (current.y > 0 && grid.grid[current.y - 1][current.x].type === 'wall' && backtracker_checkNeighbors(current.x, current.y - 1, 'u') && current.x > 0) {
		pool.push(grid.grid[current.y - 1][current.x])
	}
	// Left - x-1
	if (current.x > 0 && grid.grid[current.y][current.x - 1].type === 'wall' && backtracker_checkNeighbors(current.x - 1, current.y, 'l') && current.y > 0) {
		pool.push(grid.grid[current.y][current.x - 1])
	}
	// Bottom - y+1
	if (current.y < grid.rows - 1 && grid.grid[current.y + 1][current.x].type === 'wall' && backtracker_checkNeighbors(current.x, current.y + 1, 'd')) {
		pool.push(grid.grid[current.y + 1][current.x])
	}
	// Right - x+1s
	if (current.x < grid.cols - 1 && grid.grid[current.y][current.x + 1].type === 'wall' && backtracker_checkNeighbors(current.x + 1, current.y, 'r')) {
		pool.push(grid.grid[current.y][current.x + 1])
	}

	// Scanning
	if (pool.length === 0) {
		for (let j = 0; j < grid.grid.length; j++) {
			for (let i = 0; i < grid.grid[j].length; i++) {
				if (grid.grid[j][i].type === 'path') {grid.grid[j][i].setType('empty')}
			}
		}
		setTimeout(huntAndKillScanStep, map(speed.value, 0, 100, 500, 20))
		return false
	}

	let rand = pool[Math.floor(Math.random()*pool.length)];

	current = rand
	current.setType('path')

	setTimeout(huntAndKillStep, map(speed.value, 0, 100, 500, 20))
}
function huntAndKillScanStep(y = 0, lastCol = null, lastType = '') {

	for (let x = 0; x < grid.cols; x++) {

		if (lastCol) {
			lastCol.setType(lastType)
		}

		let col = grid.grid[y][x]

		lastCol = col
		lastType = col.type

		col.setType('searched')

		if (lastType === 'wall' && backtracker_checkNeighbors(x,y, 'd')) {
			current = col
			current.setType('path')
			setTimeout(huntAndKillStep, map(speed.value, 0, 100, 500, 20))
			return false
		}

	}
	y++;
	if (y >= grid.rows) {
		finished = true
		backtracker_clear()
		return false
	}
	setTimeout(() => {huntAndKillScanStep(y,lastCol,lastType)}, map(speed.value, 0, 100, 200, 10))
}

function generateMaze_recursiveDivision() {
	console.log('Generating Recursive division')
	grid.resetGrid()
	grid.start.setCol(grid.grid[0][0])
	grid.end.setCol(grid.grid[grid.grid.length-1][grid.grid[grid.grid.length-1].length - 1])
	grids = [grid.getGrid()]
	finished = false

	recursiveDivisionStep()
}
function recursiveDivisionStep() {

	if (stopGenerate) {
		stopGenerate = false
		return false
	}

	if (grids.length === 0) {
		finished = true
		return true
	}

	let index = grids.length-1

	if (grids[index].length <= 2 || grids[index][0].length <= 2) {
		grids.splice(index, 1)
		recursiveDivisionStep()
		return false
	}

	splitGrid(index)

	setTimeout(recursiveDivisionStep, map(speed.value, 0, 100, 500, 20))
}
function splitGrid(i) {
	let h = grids[i].length,
	w = grids[i][0].length
	let activeGrid = grids[i]

	if (h > w || (h === w && Math.random() <= 0.5)) { // Split horizontaly
		splitGridHorizontal(activeGrid, h, w)
	}
	else { // Split verticaly
		splitGridVertical(activeGrid, h, w)
	}

	grids.splice(i, 1)

}
function splitGridHorizontal(activeGrid, h, w) {
	let half = Math.floor(h/2)
	let split = half + Math.round(Math.random() * h/3 - h/6) // Get index from 1 to second last index
	if (split % 2 === 0) {
		split++
	}
	let passThrough = Math.round(Math.random() * (w-1)) // Get index where there will be no wall
	if (passThrough % 2 === 1) {
		if (Math.random() <= 0.5) {passThrough++}
		else {passThrough--}
	}
	for (let j = 0; j < w; j++) {
		if (j !== passThrough) {
			activeGrid[split][j].setType('wall')
		}
	}
	// Split grids array
	let splittedGrid = activeGrid.slice(0, split)
	let splittedGrid2 = activeGrid.slice(split+1)
	grids.push(splittedGrid)
	grids.push(splittedGrid2)
}
function splitGridVertical(activeGrid, h, w) {
	let half = Math.floor(w/2)
	let split = half + Math.round(Math.random() * w/3 - w/6) // Get index from 1 to second last index
	if (split % 2 === 0) {
		split++
	}
	let passThrough = Math.round(Math.random() * (h-1)) // Get index where there will be no wall
	if (passThrough % 2 === 1) {
		if (Math.random() <= 0.5) {passThrough++}
		else {passThrough--}
	}
	let splittedGrid = []
	let splittedGrid2 = []
	for (let j = 0; j < h; j++) {
		if (j !== passThrough) {
			activeGrid[j][split].setType('wall')
		}
		splittedGrid.push(activeGrid[j].slice(0, split))
		splittedGrid2.push(activeGrid[j].slice(split+1))
	}
	grids.push(splittedGrid)
	grids.push(splittedGrid2)
}
