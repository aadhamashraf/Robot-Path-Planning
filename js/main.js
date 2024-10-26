var grid, headerSize, dragging, activeAlgorithm, solved = false, solving = false, distance = 0, steps = 0, drawing = false, dragging = false, speed, stopSolve = false, stopGenerate = false
const colSize = 35

window.onload = () => {

	grid = new Grid();

	headerSize = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--header-height').replace('px', ''))

	speed = document.getElementById('speed')
	const solveAlgorithm = document.getElementById('solveAlgorithm')
	const mazeAlgorithm = document.getElementById('mazeAlgorithm')
	const heuriticsDom = document.getElementById('heuritics')
	const mazeGeneratorDescription = document.getElementById('mazeGeneratorDescription')
	const solveAlgorithmDescription = document.getElementById('solveAlgorithmDescription')
	const heuriticsDescription = document.getElementById('heuriticsDescription')

	console.log(solveAlgorithm, mazeAlgorithm, heuriticsDom, mazeGeneratorDescription, solveAlgorithmDescription, heuriticsDescription)

	document.onmouseup = () => {
		grid.mouseDown = false
		if (dragging && solved) {
			console.log('solving fast...')
			switch (solveAlgorithm.value) {
				case 'A':
					console.log('A*')
					solveAStarFast()
					break;
				case 'dijkstra':
					console.log('Dijkstra')
					solveDijkstraFast()
					break;
			}
		}
		dragging = false
	}

	mazeAlgorithm.addEventListener('change', (e) => {
		let description = document.querySelector(`option[value="${e.target.value}"]`).dataset.desc
		mazeGeneratorDescription.innerHTML = description
	})

	solveAlgorithm.addEventListener('change', (e) => {
		let option = document.querySelector(`option[value="${e.target.value}"]`)
		let description = option.dataset.desc, heuriticsOn = option.dataset.heuretics
		solveAlgorithmDescription.innerText = description
		if (heuriticsOn === 'true') {
			heuriticsDom.classList.remove('hide')
			heuriticsDescription.classList.remove('hide')
		}
		else {
			heuriticsDom.classList.add('hide')
			heuriticsDescription.classList.add('hide')
		}
	})

	heuriticsDom.addEventListener('change', (e) => {
		let description = document.querySelector(`option[value="${e.target.value}"]`).dataset.desc
		console.log(description)
		heuriticsDescription.innerText = description
	})

	let evt = document.createEvent("HTMLEvents");
		evt.initEvent("change", false, true);
		solveAlgorithm.dispatchEvent(evt);
		heuriticsDom.dispatchEvent(evt);
		mazeAlgorithm.dispatchEvent(evt);


	document.getElementById('reset').onclick = () => {
		grid.resetGrid()
	}

	document.getElementById('stop').onclick = () => {
		if (solving) {stopSolve = true}
		if (!finished) {stopGenerate = true}
	}

	document.getElementById('solve').onclick = () => {
		switch (solveAlgorithm.value) {
			case 'A':
				solveAStar()
				break;
			case 'dijkstra':
				solveDijkstra()
				break;
		}
	}

	document.getElementById('solveFast').onclick = () => {
		switch (solveAlgorithm.value) {
			case 'A':
				solveAStarFast()
				break;
			case 'dijkstra':
				solveDijkstraFast()
				break;
		}
	}

	document.getElementById('generateMaze').onclick = () => {
		switch (mazeAlgorithm.value) {
			case 'backtracker':
				generateMaze_backtracker();
				break;
			case 'backtrackerMulti':
				generateMaze_backtracker_multi();
				break;
			case 'huntAndKill':
				generateMaze_huntAndKill();
				break;
			case 'recursiveDivision':
				generateMaze_recursiveDivision();
				break;
		}
	}

}

window.onresize = () => {
	grid.resetGridSize();
}

class Grid {

	constructor() {
		this.dom = document.getElementById('grid')
		this.grid = []
		this.resetGridSize()

		this.start = new Start(this, Math.floor(this.cols/3), Math.floor(this.rows/2))
		this.end = new End(this, Math.floor(2*this.cols/3), Math.floor(this.rows/2))

		this.mouseDown = false
		this.lastCol = null

		this.top = this.dom.offsetTop

		this.dom.onmousedown = (e) => {
			this.mouseDown = true
			this.lastCol = this.getMouseColHover(e)
			if (this.lastCol) {
				if (this.lastCol.type === 'start' || this.lastCol.type === 'end') {
					dragging = this.lastCol.type
				}
				else {
					this.lastCol.toggleWall()
				}
			}
		}
		this.dom.onmousemove = (e) => {
			if (this.mouseDown) {
				let col = this.getMouseColHover(e)
				if (dragging !== false) {
					if (solving) {
						console.log('solving, can\'t move')
						return false
					}
					let dragCol
					if (dragging === 'start') {
						dragCol = this.start
					}
					else if (dragging === 'end') {
						dragCol = this.end
					}
					if (col !== this.lastCol && col !== false) {
						this.lastCol = col
						dragCol.setCol(col)
					}
				}
				else {
					if (col !== this.lastCol && col !== false && col.type !== 'start' && col.type !== 'end') {
						let type = this.lastCol.type
						this.lastCol = col
						this.lastCol.setType(type)
					}
				}
			}
		}
	}

	getMouseColHover(e) {
		let left = e.x
		let top = e.y - this.top

		let col = Math.floor(left / colSize)
		let row = Math.floor(top / colSize)

		if (this.grid[row] && this.grid[row][col]) {
			if ((dragging === 'start' && this.grid[row][col].type === 'end') || (dragging === 'end' && this.grid[row][col].type === 'start')) {
				return false
			}
			return this.grid[row][col]
		}
		return false
	}

	resetGridSize() {
		// Get size from dom
		this.width = this.dom.offsetWidth
		this.height = this.dom.offsetHeight

		this.top = this.dom.offsetTop

		// Calculate cols and rows from the size
		this.cols = Math.floor(this.width/colSize)
		this.rows = Math.floor(this.height/colSize)

		// Generate a grid - add|remove rows and columns
		// Removing rows
		while (this.grid.length > this.rows) {
			let row = this.grid.pop()
			for (let i = 0; i < row.length; i++) {
				row[i].dom.remove()
			}
		}
		// Looping through all this.rows
		for (let j = 0; j < this.rows; j++) {
			// Create new rows
			if (!this.grid[j]) {
				this.grid[j] = [];
			}
			// Create new columns
			while (this.grid[j].length < this.cols){
				let col = new Col(this.grid[j].length, j)
				this.grid[j].push(col);
				if (j < this.grid.length - 1) {
					this.dom.insertBefore(col.dom, this.grid[j+1][0].dom)
				}
				else {
					this.dom.appendChild(col.dom)
				}
			}
			// Remove spare columns
			while (this.grid[j].length > this.cols) {
				let col = this.grid[j].pop()
				col.dom.remove()
			}
		}
	}

	resetGrid() {
		this.start.setCol(this.grid[Math.floor(this.rows/2)][Math.floor(this.cols/3)])
		this.end.setCol(this.grid[Math.floor(this.rows/2)][Math.floor(2*this.cols/3)])
		this.resetSolving(true)
	}

	resetSolving(full = false) {
		if (solving) {stopSolve = true}
		if (!finished) {stopGenerate = true}
		for (let j = 0; j < this.grid.length; j++) {
			for (let i = 0; i < this.grid[j].length; i++) {
				if (this.grid[j][i].type !== 'wall' || full) {
					this.grid[j][i].setType('empty')
					this.grid[j][i].visited = false
				}
			}
		}
		this.start.setCol(this.grid[this.start.y][this.start.x])
		this.end.setCol(this.grid[this.end.y][this.end.x])
		solving = false
		solved = false
		steps = 0
		distance = 0
		drawing = false
	}

	getGrid() {
		return this.grid.slice(0)
	}

}

class Col {

	constructor(x, y) {
		this.dom = document.createElement('div')
		this.dom.classList.add('col')
		this.dom.style.width = colSize + 'px'
		this.dom.style.height = colSize + 'px'
		this.type = 'empty'
		this.visited = false
		this.setType('empty')

		this.x = x
		this.y = y

		this.dom.ondragover = (e) => {
			e.preventDefault()
		}

		this.dom.ondrop = (e) => {
			dragging.setCol(this)
			if (solving && dragging.dom.id === 'start') {
				clearInterval(search)
				switch (activeAlgorithm) {
					case 'A':
						solveAStar()
						break;
					case 'dijkstra':
						solveDijkstra()
						break;
				}
			}
			if (solved) {
				switch (activeAlgorithm) {
					case 'A':
						solveAStarFast()
						break;
					case 'dijkstra':
						solveDijkstraFast()
						break;
				}
			}
		}
	}

	toggleWall() {
		if (this.type === 'wall') {
			this.setType('empty')
		}
		else {
			this.setType('wall')
		}
	}

	setType(type) {
		this.dom.classList.remove(this.type)
		this.type = type
		this.dom.classList.add(this.type)
	}

}

class Start {

	constructor(grid,x,y) {
		this.dom = document.createElement('span')
		// this.dom.setAttribute('draggable', 'true');
		this.dom.innerHTML = '&Alpha;'
		this.dom.id = 'start'

		this.setCol(grid.grid[y][x])

		// this.dom.ondragstart = (e) => {
		// 	dragging = this
		// 	grid.mouseDown = false
		// 	grid.grid[this.y][this.x].setType('blank')
		// }
		// this.dom.ondragend = (e) => {
		// 	dragging = null
		// }
	}

	getCol() {
		return grid.grid[this.y][this.x]
	}

	setCol(col) {
		if (this.x && this.y) {grid.grid[this.y][this.x].setType('empty')}
		this.x = col.x
		this.y = col.y
		col.dom.appendChild(this.dom)
		col.setType('start')
		col.dom.classList.remove('active')
	}

}

class End {

	constructor(grid,x,y) {
		this.dom = document.createElement('span')
		// this.dom.setAttribute('draggable', 'true');
		this.dom.innerHTML = '&Omega;'
		this.dom.id = 'end'

		this.setCol(grid.grid[y][x])

		// this.dom.ondragstart = (e) => {
		// 	dragging = this
		// 	grid.mouseDown = false
		// 	grid.grid[this.y][this.x].setType('blank')
		// }
		// this.dom.ondragend = (e) => {
		// 	dragging = null
		// }
	}

	getCol() {
		return grid.grid[this.y][this.x]
	}

	setCol(col) {
		if (this.x && this.y) {grid.grid[this.y][this.x].setType('empty')}
		this.x = col.x
		this.y = col.y
		col.dom.appendChild(this.dom)
		col.setType('end')
		col.dom.classList.remove('active')
	}

}

function found(path) {
	distance = path.length
	document.getElementById('info').innerHTML = `<span>Steps taken: ${steps}</span><span>Distance: ${distance}</span>`
	solved = true
	solving = false
	for (let i = 0; i < path.length; i++) {
		path[i].setType('empty')
	}
	setTimeout(() => {
		draw(path, 0)
	}, 400)
}

function draw(path, i) {
	if (i === 0) {
		drawing = true
	}
	if (!path[i] || !drawing) {
		drawing = false
		return false
	}
	path[i].setType('path')
	grid.start.getCol().setType('start')
	grid.end.getCol().setType('end')
	setTimeout(() => {
		draw(path, i+1)
	}, map(speed.value, 0, 100, 6000, 500)/path.length)
}

function map(v, l1, h1, l2, h2) {
	return (((v-l1)/(h1-l1))*(h2-l2))+l2
}
