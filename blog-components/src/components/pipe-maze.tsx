"use client"

import { useRerender } from "@react-hookz/web"
import classNames from "classnames"
import _ from "lodash"
import React, { useMemo, useRef, useState } from "react"

import { Grid } from "@components/grid"

interface Position {
    x: number
    y: number
}

const EMPTY = "◦"
const START = "S"

const pipes = [EMPTY, "|", "-", "L", "J", "7", "F", START] as const
type Pipe = (typeof pipes)[number]
type OffsetKey = `${Pipe}:${number}:${number}`

const OFFSET: Record<OffsetKey, Position> = {
    "|:0:1": { x: 0, y: 1 },
    "|:0:-1": { x: 0, y: -1 },
    "-:1:0": { x: 1, y: 0 },
    "-:-1:0": { x: -1, y: 0 },
    "L:0:1": { x: 1, y: 0 },
    "L:-1:0": { x: 0, y: -1 },
    "J:1:0": { x: 0, y: -1 },
    "J:0:1": { x: -1, y: 0 },
    "7:1:0": { x: 0, y: 1 },
    "7:0:-1": { x: -1, y: 0 },
    "F:-1:0": { x: 0, y: 1 },
    "F:0:-1": { x: 1, y: 0 },
}

function isPipe(value: string): value is Pipe {
    // @ts-ignore
    return pipes.includes(value)
}

class PipeGrid extends Grid<Pipe> {
    protected position: Position | null = null
    protected path: Array<Position> = []
    protected nextOffset: Position | null = null

    isHere(x: number, y: number) {
        return this.position && x === this.position.x && y === this.position.y
    }

    start() {
        // Set the start position, clear the path
        for (let x = 0; x < this.maxX; x++) {
            for (let y = 0; y < this.maxY; y++) {
                if (this.getValue(x, y) == "S") {
                    this.position = { x, y }
                    this.path = []
                }
            }
        }
    }

    stepInitial() {
        if (this.nextOffset !== null) {
            throw new Error("Initial step already complete.")
        }

        // Get the first position we'll move to
        ;[
            [0, 1],
            [0, -1],
            [1, 0],
            [-1, 0],
        ].forEach(([xOffset, yOffset]) => {
            if (this.position === null) {
                throw new Error("No starting position.")
            }

            // We've already calculated a valid next offset, skip
            if (this.nextOffset !== null) {
                return
            }

            const nextPipe = this.getValue(this.position.x + xOffset, this.position.y + yOffset)

            if (!nextPipe) {
                return
            }

            const key: OffsetKey = `${nextPipe}:${xOffset}:${yOffset}`

            if (key in OFFSET) {
                this.nextOffset = OFFSET[key]
                this.position = {
                    x: this.position.x + xOffset,
                    y: this.position.y + yOffset,
                }
            }
        })
    }

    step() {
        if (this.position === null) {
            this.start()
            return
        }

        if (this.nextOffset === null) {
            this.stepInitial()
            return
        }

        // Add current position to the path
        this.path.push(this.position)

        // Move to the next position
        this.position = {
            x: this.position.x + this.nextOffset.x,
            y: this.position.y + this.nextOffset.y,
        }

        // Get the pipe at the new position
        const nextPipe = this.getValue(this.position.x, this.position.y)

        if (nextPipe === undefined) {
            throw new Error("Next pipe not found.")
        }

        // Update the next offset
        this.nextOffset = OFFSET[`${nextPipe}:${this.nextOffset.x}:${this.nextOffset.y}`]
    }

    isCompleted() {
        return (
            this.position !== null &&
            this.getValue(this.position.x, this.position.y) === START &&
            this.path.length > 1
        )
    }

    canStep() {
        return !this.isCompleted()
    }

    pathIndex(x: number, y: number) {
        for (let i = 0; i < this.path.length; i++) {
            if (this.path[i].x === x && this.path[i].y === y) {
                return i
            }
        }

        return null
    }

    clear() {
        this.position = null
        this.nextOffset = null
        this.path = []
        super.clear()
    }
}

export function PipeMaze() {
    /**************************************************************************/
    /* State */
    const forceRerender = useRerender()

    const pipeGridRef = useRef<PipeGrid>(new PipeGrid())

    const [height, setHeight] = useState(5)
    const [width, setWidth] = useState(5)

    const rows = useMemo(() => {
        return _.range(0, height)
    }, [height])

    const columns = useMemo(() => {
        return _.range(0, width)
    }, [width])

    /**************************************************************************/
    /* Render */
    return (
        <div className="tw-flex tw-flex-col tw-gap-4">
            <GridControls
                height={height}
                setHeight={setHeight}
                width={width}
                setWidth={setWidth}
                pipeGrid={pipeGridRef.current}
            />

            <ViewableGrid
                rows={rows}
                columns={columns}
                pipeGrid={pipeGridRef.current}
            />

            <div className="tw-flex tw-gap-4">
                <button
                    className="tw-btn tw-btn-primary"
                    disabled={!pipeGridRef.current.canStep()}
                    onClick={() => {
                        pipeGridRef.current.step()
                        forceRerender()
                    }}
                >
                    Step
                </button>
            </div>
        </div>
    )
}

function GridControls(props: {
    height: number
    setHeight: React.Dispatch<React.SetStateAction<number>>
    width: number
    setWidth: React.Dispatch<React.SetStateAction<number>>
    pipeGrid: PipeGrid
}) {
    /**************************************************************************/
    /* Render */
    return (
        <div className="tw-flex tw-gap-4">
            <div className="tw-flex tw-items-center">
                <div className="tw-rounded-s tw-border-2 tw-border-r-0 tw-border-primary tw-px-1.5 tw-py-0.5">
                    Height
                </div>

                <button
                    className="tw-btn tw-btn-primary tw-rounded-none"
                    disabled={props.height <= 2}
                    onClick={() => {
                        props.setHeight((prevState) => {
                            return Math.max(prevState - 1, 2)
                        })
                    }}
                >
                    –
                </button>

                <div className="tw-h-full tw-w-[1px] tw-border-y-2 tw-border-primary tw-bg-transparent" />

                <button
                    className="tw-btn tw-btn-primary tw-inline-flex tw-rounded-l-none"
                    onClick={() => {
                        props.setHeight((prevState) => {
                            return prevState + 1
                        })
                    }}
                >
                    +
                </button>
            </div>

            <div className="tw-flex tw-items-center">
                <div className="tw-rounded-s tw-border-2 tw-border-r-0 tw-border-primary tw-px-1.5 tw-py-0.5">
                    Width
                </div>

                <button
                    className="tw-btn tw-btn-primary tw-rounded-none"
                    disabled={props.width <= 2}
                    onClick={() => {
                        props.setWidth((prevState) => {
                            return Math.max(prevState - 1, 2)
                        })
                    }}
                >
                    –
                </button>

                <div className="tw-h-full tw-w-[1px] tw-border-y-2 tw-border-primary tw-bg-transparent" />

                <button
                    className="tw-btn tw-btn-primary tw-inline-flex tw-rounded-l-none"
                    onClick={() => {
                        props.setWidth((prevState) => {
                            return prevState + 1
                        })
                    }}
                >
                    +
                </button>
            </div>

            <button
                className="tw-btn tw-btn-primary"
                onClick={() => {
                    const tempWidth = props.width
                    const tempHeight = props.height

                    // Async callback used to force a re-render between width/height being set to 0, then reset back
                    // Because the inputs are uncontrolled, this resets them
                    async function reset() {
                        props.setWidth(0)
                        props.setHeight(0)

                        props.pipeGrid.clear()
                    }

                    reset().then(() => {
                        props.setWidth(tempWidth)
                        props.setHeight(tempHeight)
                    })
                }}
            >
                Clear
            </button>
        </div>
    )
}

function ViewableGrid(props: { rows: Array<number>; columns: Array<number>; pipeGrid: PipeGrid }) {
    /**************************************************************************/
    /* Render */
    return (
        <div className="tw-flex tw-w-fit tw-flex-col tw-rounded tw-border-2 tw-border-primary">
            {props.rows.map((y) => {
                return (
                    <div
                        key={y}
                        className="tw-flex"
                    >
                        {props.columns.map((x) => {
                            const pathIndex = props.pipeGrid.pathIndex(x, y)

                            console.log(x, y, pathIndex)

                            return (
                                <div
                                    key={x}
                                    className="tw-relative tw-flex tw-h-8 tw-w-8 tw-flex-col"
                                >
                                    {pathIndex && <div className="tw-absolute">{pathIndex}</div>}

                                    <label className="tw-hidden">
                                        {x}, {y}
                                    </label>

                                    <select
                                        defaultValue={props.pipeGrid.getValue(x, y) || EMPTY}
                                        className={classNames(
                                            "focus:outline-none tw-h-full tw-w-full tw-appearance-none tw-border-0 tw-bg-none tw-p-1 tw-text-center tw-outline-none tw-ring-0 hover:tw-bg-primary hover:tw-text-white focus:tw-bg-primary focus:tw-text-white",
                                            props.pipeGrid.isHere(x, y) ? "tw-bg-slate-500" : "",
                                        )}
                                        onChange={(event) => {
                                            const {
                                                target: { value },
                                            } = event

                                            if (isPipe(value)) {
                                                props.pipeGrid.addValue(x, y, value)
                                            } else {
                                                throw new Error("Value is not a valid pipe.")
                                            }
                                        }}
                                    >
                                        {pipes.map((pipe) => {
                                            return (
                                                <option
                                                    key={pipe}
                                                    value={pipe}
                                                >
                                                    {pipe}
                                                </option>
                                            )
                                        })}
                                    </select>
                                </div>
                            )
                        })}
                    </div>
                )
            })}
        </div>
    )
}
