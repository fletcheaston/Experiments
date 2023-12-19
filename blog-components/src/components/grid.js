export class Grid {
    constructor() {
        this.grid = {}
        this.maxX = 0
        this.maxY = 0
    }
    key(x, y) {
        return `${x}:${y}`
    }
    addValue(x, y, value) {
        this.maxX = Math.max(this.maxX, x + 1)
        this.maxY = Math.max(this.maxY, y + 1)
        this.grid[this.key(x, y)] = value
    }
    getValue(x, y) {
        return this.grid[`${x}:${y}`]
    }
    clear() {
        this.grid = {}
    }
}
