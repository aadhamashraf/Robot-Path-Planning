var active, endCord, paths, activePath, step, path, pathStep, heuritics
function solveAStar() {
	console.log('solving A*')

	heuritics = document.getElementById('heuritics').value

	grid.resetSolving();
	solving = true

	active = grid.grid[grid.start.y][grid.start.x]
	endCord = {x: grid.end.x, y: grid.end.y}
	paths = [{path: [active], dist: Math.sqrt(Math.pow((active.x - endCord.x), 2) + Math.pow((active.y - endCord.y), 2))}]

	activePath = paths[0]

	aStarStep()

}
function aStarStep() {
	let newNeighbors = 0

	if (stopSolve) {
		stopSolve = false
		return false
	}

	// Top neighbor
	if (active.y - 1 >= 0) {
		let next = grid.grid[active.y - 1][active.x]
		if ((next.type === 'empty' || next.type === 'end') && !next.visited) {
			steps++
			next.visited = true
			if (next.type !== 'end'){next.setType('activeSearch')}
			let dx = endCord.x - next.x
			let dy = endCord.y - next.y
			let path = {path: [...activePath.path], dist: 0}
			path.path.push(next)
			path.dist = Math.sqrt(dx*dx + dy*dy)
			paths.push(path)
			newNeighbors++
		}
	}

	// Right neighbor
	if (active.x + 1 < grid.cols) {
		let next = grid.grid[active.y][active.x + 1]
		if ((next.type === 'empty' || next.type === 'end') && !next.visited) {
			steps++
			next.visited = true
			if (next.type !== 'end'){next.setType('activeSearch')}
			let dx = endCord.x - next.x
			let dy = endCord.y - next.y
			let path = {path: [...activePath.path], dist: 0}
			path.path.push(next)
			path.dist = Math.sqrt(dx*dx + dy*dy)
			paths.push(path)
			newNeighbors++
		}
	}

	// Bottom neighbor
	if (active.y + 1 < grid.rows) {
		let next = grid.grid[active.y + 1][active.x]
		if ((next.type === 'empty' || next.type === 'end') && !next.visited) {
			steps++
			next.visited = true
			if (next.type !== 'end'){next.setType('activeSearch')}
			let dx = endCord.x - next.x
			let dy = endCord.y - next.y
			let path = {path: [...activePath.path], dist: 0}
			path.path.push(next)
			path.dist = Math.sqrt(dx*dx + dy*dy)
			paths.push(path)
			newNeighbors++
		}
	}

	// Left neighbor
	if (active.x - 1 >= 0) {
		let next = grid.grid[active.y][active.x - 1]
		if ((next.type === 'empty' || next.type === 'end') && !next.visited) {
			steps++
			next.visited = true
			if (next.type !== 'end'){next.setType('activeSearch')}
			let dx = endCord.x - next.x
			let dy = endCord.y - next.y
			let path = {path: [...activePath.path], dist: 0}
			path.path.push(next)
			path.dist = Math.sqrt(dx*dx + dy*dy)
			paths.push(path)
			newNeighbors++
		}
	}

	if (active.type !== 'start'){active.setType('searched')}

	paths.shift()
	if (paths.length === 0) {
		document.getElementById('info').innerHTML = `<span>Steps taken: ${steps}</span>`
		alert('No route')
		solving = false
		solved = true
		return false;
	}
	paths.sort((n1, n2) => {
		if (heuritics === 'distanceAndLength') {return (n1.dist+n1.path.length) - (n2.dist+n2.path.length)}
		return n1.dist - n2.dist
	})

	for (let i = 1; i < activePath.path.length; i++) {
		activePath.path[i].setType('searched')
	}
	activePath = paths[0]
	active = activePath.path[activePath.path.length - 1]
	if (active.type === 'end') {
		found(activePath.path)
		return true;
	}
	for (let i = 1; i < activePath.path.length; i++) {
		activePath.path[i].setType('path')
	}
	setTimeout(aStarStep, map(speed.value, 0, 100, 500, 20))
}
function solveAStarFast() {
	console.log('solving A*')
	grid.resetSolving();
	solving = true
	heuritics = document.getElementById('heuritics').value

	let active = grid.grid[grid.start.y][grid.start.x]
	let endCord = {x: grid.end.x, y: grid.end.y}
	let paths = [{path: [active], dist: Math.sqrt(Math.pow((active.x - endCord.x), 2) + Math.pow((active.y - endCord.y), 2))}]

	let activePath = paths[0]
	let done = false

	while (!done) {

		let newNeighbors = 0

		// Top neighbor
		if (active.y - 1 >= 0) {
			let next = grid.grid[active.y - 1][active.x]
			if ((next.type === 'empty' || next.type === 'end') && !next.visited) {
				steps++
				next.visited = true
				if (next.type !== 'end'){next.setType('activeSearch')}
				let dx = endCord.x - next.x
				let dy = endCord.y - next.y
				let path = {path: [...activePath.path], dist: 0}
				path.path.push(next)
				path.dist = Math.sqrt(dx*dx + dy*dy)
				paths.push(path)
				newNeighbors++
			}
		}

		// Right neighbor
		if (active.x + 1 < grid.cols) {
			let next = grid.grid[active.y][active.x + 1]
			if ((next.type === 'empty' || next.type === 'end') && !next.visited) {
				steps++
				next.visited = true
				if (next.type !== 'end'){next.setType('activeSearch')}
				let dx = endCord.x - next.x
				let dy = endCord.y - next.y
				let path = {path: [...activePath.path], dist: 0}
				path.path.push(next)
				path.dist = Math.sqrt(dx*dx + dy*dy)
				paths.push(path)
				newNeighbors++
			}
		}

		// Bottom neighbor
		if (active.y + 1 < grid.rows) {
			let next = grid.grid[active.y + 1][active.x]
			if ((next.type === 'empty' || next.type === 'end') && !next.visited) {
				steps++
				next.visited = true
				if (next.type !== 'end'){next.setType('activeSearch')}
				let dx = endCord.x - next.x
				let dy = endCord.y - next.y
				let path = {path: [...activePath.path], dist: 0}
				path.path.push(next)
				path.dist = Math.sqrt(dx*dx + dy*dy)
				paths.push(path)
				newNeighbors++
			}
		}

		// Left neighbor
		if (active.x - 1 >= 0) {
			let next = grid.grid[active.y][active.x - 1]
			if ((next.type === 'empty' || next.type === 'end') && !next.visited) {
				steps++
				next.visited = true
				if (next.type !== 'end'){next.setType('activeSearch')}
				let dx = endCord.x - next.x
				let dy = endCord.y - next.y
				let path = {path: [...activePath.path], dist: 0}
				path.path.push(next)
				path.dist = Math.sqrt(dx*dx + dy*dy)
				paths.push(path)
				newNeighbors++
			}
		}

		if (active.type !== 'start'){active.setType('searched')}

		paths.shift()
		if (paths.length === 0) {
			document.getElementById('info').innerHTML = `<span>Steps taken: ${steps}</span>`
			alert('No route')
			solving = false
			solved = true
			done = true
			break
		}
		paths.sort((n1, n2) => {
			if (heuritics === 'distanceAndLength') {return (n1.dist+n1.path.length) - (n2.dist+n2.path.length)}
			return n1.dist - n2.dist
		})

		for (let i = 1; i < activePath.path.length; i++) {
			activePath.path[i].setType('searched')
		}
		activePath = paths[0]
		active = activePath.path[activePath.path.length - 1]
		if (active.type === 'end') {
			found(activePath.path)
			done = true
			break
		}
		for (let i = 1; i < activePath.path.length; i++) {
			activePath.path[i].setType('path')
		}
	}
}

function solveDijkstra() {
	console.log('solving Dijkstra')
	grid.resetSolving();
	solving = true

	active = grid.grid[grid.start.y][grid.start.x]
	active.visited
	paths = [[active]];

	step = 0;
	pathStep = paths.length - 1;
	path = [...paths[pathStep]]

	dijkstraStep();
}
function dijkstraStep() {

	if (stopSolve) {
		stopSolve = false
		return false
	}

	for (let i = 1; i < path.length - 1; i++) {
	path[i].setType('searched')
	}
	if (!paths[pathStep]) {
		document.getElementById('info').innerHTML = `<span>Steps taken: ${steps}</span>`
		alert('No route')
		solving = false
		solved = true
		return false;
	}
	path = [...paths[pathStep]]
	let active = path[path.length - 1]
	active.setType('searched')
	added = false

	// Top neighbor
	if (active.y - 1 >= 0 || step !== 0) {
		if (step === 0) {
			let next = grid.grid[active.y - 1][active.x]
			if (next.type === 'empty' && !next.visited) {
				next.visited = true
				next.setType('activeSearch')
				path.push(next)
				paths.push(path)
				added = true
				steps++
			}
			else if (next.type === 'end') {
				found(path)
				return false;
			}
			else {
				step++
			}
		}
	}
	else {
		step++
	}

	// Right neighbor
	if (active.x + 1 < grid.cols || step !== 1) {
		if (step === 1) {
			let next = grid.grid[active.y][active.x + 1]
			if (next.type === 'empty' && !next.visited) {
				next.visited = true
				next.setType('activeSearch')
				path.push(next)
				paths.push(path)
				added = true
				steps++
			}
			else if (next.type === 'end') {
				found(path)
				return false;
			}
			else {
				step++
			}
		}
	}
	else {
		step++
	}

	// Bottom neighbor
	if (active.y + 1 < grid.rows || step !== 2) {
		if (step === 2) {
			let next = grid.grid[active.y + 1][active.x]
			if (next.type === 'empty' && !next.visited) {
				next.visited = true
				next.setType('activeSearch')
				path.push(next)
				paths.push(path)
				added = true
				steps++
			}
			else if (next.type === 'end') {
				found(path)
				return false;
			}
			else {
				step++
			}
		}
	}
	else {
		step++
	}

	// Left neighbor
	if (active.x - 1 >= 0) {
		if (step === 3) {
			let next = grid.grid[active.y][active.x - 1]
			if (next.type === 'empty' && !next.visited) {
				next.visited = true
				next.setType('activeSearch')
				path.push(next)
				paths.push(path)
				added = true
				steps++
			}
			else if (next.type === 'end') {
				path.push(next)
				found(path)
				return false;
			}
		}
	}
	step++
	if (step > 3) {
		paths.splice(pathStep, 1)
		pathStep--
		step = 0
		if (pathStep < 0) {
			pathStep = paths.length-1;
		}
	}
	for (let i = 1; i < path.length - 1; i++) {
		path[i].setType('path')
	}

	setTimeout(dijkstraStep, map(speed.value, 0, 100, 500, 20))

}
function solveDijkstraFast() {

	solving = false
	grid.resetSolving();

	let active = grid.grid[grid.start.y][grid.start.x]
	active.visited
	let paths = [[active]];

	let step = 0;
	let pathStep = paths.length - 1;

	let done = false

	while (!done) {
		if (!paths[pathStep]) {
			document.getElementById('info').innerHTML = `<span>Steps taken: ${steps}</span>`
			done = true
			alert('No route')
			solving = false
			solved = true
			break
		}
		let path = [...paths[pathStep]]
		let active = path[path.length - 1]
		active.setType('searched')
		added = false

		// Top neighbor
		if (active.y - 1 >= 0) {
			let next = grid.grid[active.y - 1][active.x]
			if (next.type === 'empty' && !next.visited) {
				steps++
				next.visited = true
				next.setType('activeSearch')
				path.push(next)
				paths.push(path)
			}
			else if (next.type === 'end') {
				found(path)
				done = true
				break
			}
		}

		path = [...paths[pathStep]]

		// Right neighbor
		if (active.x + 1 < grid.cols) {
			let next = grid.grid[active.y][active.x + 1]
			if (next.type === 'empty' && !next.visited) {
				steps++
				next.visited = true
				next.setType('activeSearch')
				path.push(next)
				paths.push(path)
			}
			else if (next.type === 'end') {
				path.push(next)
				found(path)
				done = true
				break
			}
		}

		path = [...paths[pathStep]]

		// Bottom neighbor
		if (active.y + 1 < grid.rows) {
			let next = grid.grid[active.y + 1][active.x]
			if (next.type === 'empty' && !next.visited) {
				steps++
				next.visited = true
				next.setType('activeSearch')
				path.push(next)
				paths.push(path)
			}
			else if (next.type === 'end') {
				found(path)
				done = true
				break
			}
		}

		path = [...paths[pathStep]]

		// Left neighbor
		if (active.x - 1 >= 0) {
			let next = grid.grid[active.y][active.x - 1]
			if (next.type === 'empty' && !next.visited) {
				steps++
				next.visited = true
				next.setType('activeSearch')
				path.push(next)
				paths.push(path)
			}
			else if (next.type === 'end') {
				found(path)
				done = true
				break
			}
		}
		paths.splice(pathStep, 1)
		pathStep--
		step = 0
		if (pathStep < 0) {
			pathStep = paths.length-1;
		}
	}
}
