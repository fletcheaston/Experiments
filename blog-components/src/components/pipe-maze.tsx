"use client"

import { useRerender } from "@react-hookz/web"
import classNames from "classnames"
import _ from "lodash"
import React, { useRef, useState } from "react"

import { Divider } from "@components/divider"
import { Grid } from "@components/grid"

interface Position {
    x: number
    y: number
}

const EMPTY = "◦"
const START = "S"

const pipes = [EMPTY, "|", "-", "L", "J", "7", "F", START] as const
type Pipe = (typeof pipes)[number]

const offsets: Record<`${number}:${number}:${number}:${number}`, Pipe> = {
    "-1:0:-1:0": "-",
    "1:0:1:0": "-",
    "0:-1:0:-1": "|",
    "0:1:0:1": "|",
    "-1:0:0:-1": "L",
    "0:1:1:0": "L",
    "1:0:0:-1": "J",
    "0:1:-1:0": "J",
    "1:0:0:1": "7",
    "0:-1:-1:0": "7",
    "-1:0:0:1": "F",
    "0:-1:1:0": "F",
} as const

class PipeGrid extends Grid<Pipe> {
    protected position: Position
    protected path: Array<Position> = []

    constructor() {
        super()
        this.position = { x: 0, y: 0 }
        this.addValue(0, 0, START)
    }

    isHere(x: number, y: number) {
        return this.position.x === x && this.position.y === y
    }

    clear() {
        super.clear()
        this.position = { x: 0, y: 0 }
        this.path = []
        this.addValue(0, 0, START)
    }

    pathIndex(x: number, y: number) {
        for (let i = 0; i < this.path.length; i++) {
            if (this.path[i].x === x && this.path[i].y === y) {
                return i
            }
        }

        return null
    }

    isCompleted() {
        return (
            this.position !== null &&
            this.getValue(this.position.x, this.position.y) === START &&
            this.path.length > 1
        )
    }

    undo() {
        const poppedPosition = this.path.pop()
        if (poppedPosition !== undefined) {
            this.position = poppedPosition
        }

        // Don't undo the start position
        if (this.getValue(this.position.x, this.position.y) === START) {
            return
        }

        delete this.grid[this.key(this.position.x, this.position.y)]
    }

    move(position: Position) {
        // Add current position to history
        this.path.push(this.position)

        // Update current position
        this.position = {
            x: this.position.x + position.x,
            y: this.position.y + position.y,
        }

        // Set the character we just put in the last position
        // If not enough characters, we must have just started
        if (this.path.length < 2) {
            return
        }

        // Get the position before last
        const formerPosition = this.path[this.path.length - 1]
        const priorPosition = this.path[this.path.length - 2]

        // Calculate offset from the new position
        const xOffset1 = this.position.x - formerPosition.x
        const yOffset1 = this.position.y - formerPosition.y

        const xOffset2 = formerPosition.x - priorPosition.x
        const yOffset2 = formerPosition.y - priorPosition.y

        // Get the character for the last position
        const pipe = offsets[`${xOffset2}:${yOffset2}:${xOffset1}:${yOffset1}`]
        this.addValue(formerPosition.x, formerPosition.y, pipe)

        // Update boundaries
        this.minX = Math.min(this.minX, this.position.x)
        this.maxX = Math.max(this.maxX, this.position.x + 1)

        this.minY = Math.min(this.minY, this.position.y)
        this.maxY = Math.max(this.maxY, this.position.y + 1)
    }

    columns() {
        return _.range(this.minX, this.maxX)
    }

    rows() {
        return _.range(this.minY, this.maxY)
    }
}

export function PipeMaze() {
    /**************************************************************************/
    /* State */
    const forceRerender = useRerender()

    const pipeGridRef = useRef<PipeGrid>(new PipeGrid())

    /**************************************************************************/
    /* Render */
    return (
        <div className="tw-flex tw-gap-4">
            <div className="tw-flex-shrink">
                <GridControls
                    pipeGrid={pipeGridRef.current}
                    forceRerender={forceRerender}
                />
            </div>

            <ViewableGrid
                rows={pipeGridRef.current.rows()}
                columns={pipeGridRef.current.columns()}
                pipeGrid={pipeGridRef.current}
            />
        </div>
    )
}

type PressedKey = "W" | "A" | "S" | "D"
const lowerKeys: Array<PressedKey> = ["A", "S", "D"]
const pressedKeyOffset: Record<PressedKey, Position> = {
    W: { x: 0, y: -1 },
    A: { x: -1, y: 0 },
    S: { x: 0, y: 1 },
    D: { x: 1, y: 0 },
}

function GridControls(props: { pipeGrid: PipeGrid; forceRerender: () => void }) {
    /**************************************************************************/
    /* State */
    const [pressedKey, setPressedKey] = useState<PressedKey | "Delete" | null>(null)

    /**************************************************************************/
    /* Render */
    return (
        <>
            <div className="tw-relative tw-pb-2 tw-text-primary tw-opacity-80">
                <div>Click for keyboard controls</div>
                <div className="tw-absolute tw-left-[50%] tw-top-2.5 tw-translate-x-[-50%]">⌄</div>
            </div>

            <div
                className="tw-rounded tw-border-2 tw-border-primary tw-p-1 focus-within:tw-outline-secondary focus:tw-outline-secondary"
                tabIndex={0}
                onKeyDown={(event) => {
                    if (event.key.toUpperCase() === "W") {
                        setPressedKey("W")
                        props.pipeGrid.move(pressedKeyOffset["W"])
                    } else if (event.key.toUpperCase() === "A") {
                        setPressedKey("A")
                        props.pipeGrid.move(pressedKeyOffset["A"])
                    } else if (event.key.toUpperCase() === "S") {
                        setPressedKey("S")
                        props.pipeGrid.move(pressedKeyOffset["S"])
                    } else if (event.key.toUpperCase() === "D") {
                        setPressedKey("D")
                        props.pipeGrid.move(pressedKeyOffset["D"])
                    } else if (event.key.toUpperCase() === "BACKSPACE") {
                        setPressedKey("Delete")
                        props.pipeGrid.undo()
                    } else {
                        setPressedKey(null)
                    }

                    props.forceRerender()
                }}
                onKeyUp={() => {
                    setPressedKey(null)
                }}
            >
                <div className="tw-flex tw-justify-around">
                    <div className="tw-flex tw-flex-col tw-gap-2">
                        <div className="tw-flex tw-w-full tw-justify-center">
                            <button
                                className={classNames(
                                    "tw-btn tw-btn-primary tw-btn-sm tw-h-8 tw-w-8 tw-duration-0",
                                    pressedKey === "W" ? "tw-outline tw-outline-secondary" : "",
                                )}
                                onClick={() => {
                                    setPressedKey("W")
                                    props.pipeGrid.move(pressedKeyOffset["W"])
                                    props.forceRerender()
                                }}
                            >
                                W
                            </button>
                        </div>

                        <div className="tw-flex tw-justify-center tw-gap-2">
                            {lowerKeys.map((letter) => {
                                return (
                                    <button
                                        key={letter}
                                        className={classNames(
                                            "tw-btn tw-btn-primary tw-btn-sm tw-h-8 tw-w-8 tw-duration-0",
                                            pressedKey === letter
                                                ? "tw-outline tw-outline-secondary"
                                                : "",
                                        )}
                                        onClick={() => {
                                            setPressedKey(letter)
                                            props.pipeGrid.move(pressedKeyOffset[letter])
                                            props.forceRerender()
                                        }}
                                    >
                                        {letter}
                                    </button>
                                )
                            })}
                        </div>
                    </div>

                    <button
                        className={classNames(
                            "tw-btn tw-btn-primary tw-btn-sm tw-h-8 tw-w-fit tw-duration-0",
                            pressedKey === "Delete" ? "tw-outline tw-outline-secondary" : "",
                        )}
                        onClick={() => {
                            setPressedKey("Delete")
                            props.pipeGrid.undo()
                            props.forceRerender()
                        }}
                    >
                        ⌫
                    </button>
                </div>
            </div>

            <Divider className="tw-my-1" />

            <button
                className="tw-btn tw-btn-primary-outline tw-w-full"
                onClick={() => {
                    props.pipeGrid.clear()
                    props.forceRerender()
                }}
            >
                Reset
            </button>
        </>
    )
}

function ViewableGrid(props: { rows: Array<number>; columns: Array<number>; pipeGrid: PipeGrid }) {
    /**************************************************************************/
    /* Render */
    return (
        <div className="tw-flex tw-h-fit tw-w-fit tw-flex-col tw-rounded tw-border-2 tw-border-primary">
            {props.rows.map((y) => {
                return (
                    <div
                        key={y}
                        className="tw-flex"
                    >
                        {props.columns.map((x) => {
                            const pathIndex = props.pipeGrid.pathIndex(x, y)

                            return (
                                <div
                                    key={x}
                                    className={classNames(
                                        "tw-relative tw-flex tw-h-6 tw-w-6 tw-items-center tw-justify-center",
                                        props.pipeGrid.isHere(x, y)
                                            ? "tw-bg-primary tw-text-white"
                                            : "",
                                    )}
                                >
                                    {props.pipeGrid.getValue(x, y) || EMPTY}
                                </div>
                            )
                        })}
                    </div>
                )
            })}
        </div>
    )
}
