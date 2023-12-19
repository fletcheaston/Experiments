export class Grid {
    constructor() {
        this.grid = {}
        this.minX = 0
        this.maxX = 1
        this.minY = 0
        this.maxY = 1
    }
    clear() {
        this.grid = {}
    }
    key(x, y) {
        return `${x}:${y}`
    }
    addValue(x, y, value) {
        this.minX = Math.min(this.minX, x)
        this.maxX = Math.max(this.maxX, x + 1)
        this.minY = Math.min(this.minY, y)
        this.maxY = Math.max(this.maxY, y + 1)
        this.grid[this.key(x, y)] = value
    }
    getValue(x, y) {
        return this.grid[`${x}:${y}`]
    }
}
