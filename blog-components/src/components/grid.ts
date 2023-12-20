export type Key = `${number}:${number}`

export class Grid<T> {
    protected grid: Record<Key, T> = {}

    protected minX: number = 0
    protected maxX: number = 1

    protected minY: number = 0
    protected maxY: number = 1

    clear() {
        this.grid = {}

        this.minX = 0
        this.maxX = 0

        this.minY = 0
        this.maxY = 0
    }

    key(x: number, y: number) {
        return `${x}:${y}` satisfies Key
    }

    addValue(x: number, y: number, value: T) {
        this.minX = Math.min(this.minX, x)
        this.maxX = Math.max(this.maxX, x + 1)

        this.minY = Math.min(this.minY, y)
        this.maxY = Math.max(this.maxY, y + 1)

        this.grid[this.key(x, y)] = value
    }

    getValue(x: number, y: number): T | undefined {
        return this.grid[this.key(x, y)]
    }
}
