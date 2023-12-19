export type Key = `${number}:${number}`

export class Grid<T> {
    protected grid: Record<Key, T> = {}

    protected maxX: number = 0
    protected maxY: number = 0

    key(x: number, y: number) {
        return `${x}:${y}` satisfies Key
    }

    addValue(x: number, y: number, value: T) {
        this.maxX = Math.max(this.maxX, x + 1)
        this.maxY = Math.max(this.maxY, y + 1)

        this.grid[this.key(x, y)] = value
    }

    getValue(x: number, y: number): T | undefined {
        return this.grid[`${x}:${y}`]
    }

    clear() {
        this.grid = {}
    }
}
