"use client"

import { useRerender } from "@react-hookz/web"
import classNames from "classnames"
import _ from "lodash"
import React, { useRef, useState } from "react"

import { Divider } from "@components/divider"

interface Position {
    x: number
    y: number
}

const EMPTY = "◦"
const START = "★"
const VERTICAL = "|"
const HORIZONTAL = "-"
const TURN_0_90 = "L"
const TURN_90_180 = "F"
const TURN_180_270 = "7"
const TURN_270_0 = "J"

const pipes = [
    EMPTY,
    VERTICAL,
    HORIZONTAL,
    TURN_0_90,
    TURN_90_180,
    TURN_180_270,
    TURN_270_0,
    START,
] as const
type Pipe = (typeof pipes)[number]

const offsets: Record<`${number}:${number}:${number}:${number}`, Pipe> = {
    "-1:0:-1:0": HORIZONTAL,
    "1:0:1:0": HORIZONTAL,
    "0:-1:0:-1": VERTICAL,
    "0:1:0:1": VERTICAL,
    "-1:0:0:-1": TURN_0_90,
    "0:1:1:0": TURN_0_90,
    "1:0:0:-1": TURN_270_0,
    "0:1:-1:0": TURN_270_0,
    "1:0:0:1": TURN_180_270,
    "0:-1:-1:0": TURN_180_270,
    "-1:0:0:1": TURN_90_180,
    "0:-1:1:0": TURN_90_180,
} as const

const pipeClasses: Record<Pipe, React.HTMLAttributes<HTMLDivElement>["className"]> = {
    [EMPTY]: "",
    [VERTICAL]: "tw-border-l-4 tw-border-r-4 tw-border-primary",
    [HORIZONTAL]: "tw-border-t-4 tw-border-b-4 tw-border-primary",
    [TURN_0_90]: "tw-border-b-4 tw-border-l-4 tw-border-primary tw-rounded-bl tw-border-tr",
    [TURN_90_180]: "tw-border-t-4 tw-border-l-4 tw-border-primary tw-rounded-tl tw-border-br",
    [TURN_180_270]: "tw-border-t-4 tw-border-r-4 tw-border-primary tw-rounded-tr tw-border-bl",
    [TURN_270_0]: "tw-border-b-4 tw-border-r-4 tw-border-primary tw-rounded-br tw-border-tl",
    [START]: "tw-bg-primary tw-text-white",
} as const

export type Key = `${number}:${number}`

class PipeGrid {
    protected grid: Record<Key, Pipe> = {
        ["0:0"]: START,
    }

    protected path: Array<Position> = []

    protected position: Position = { x: 0, y: 0 }

    key(x: number, y: number) {
        return `${x}:${y}` satisfies Key
    }

    getValue(x: number, y: number): Pipe | undefined {
        return this.grid[this.key(x, y)]
    }

    minX() {
        return (
            Math.min(
                this.position.x,
                ...this.path.map((position) => {
                    return position.x
                }),
            ) - 1
        )
    }

    maxX() {
        return (
            Math.max(
                this.position.x,
                ...this.path.map((position) => {
                    return position.x
                }),
            ) + 2
        )
    }

    minY() {
        return (
            Math.min(
                this.position.y,
                ...this.path.map((position) => {
                    return position.y
                }),
            ) - 1
        )
    }

    maxY() {
        return (
            Math.max(
                this.position.y,
                ...this.path.map((position) => {
                    return position.y
                }),
            ) + 2
        )
    }

    isHere(x: number, y: number) {
        return this.position.x === x && this.position.y === y
    }

    isCompleted() {
        return this.getValue(this.position.x, this.position.y) === START && this.path.length > 1
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

    move(offset: Position) {
        // If we've completed the loop, prevent movement
        if (this.isCompleted()) {
            return
        }

        // If we already have a pipe here, skip the move
        const nextPipe = this.getValue(this.position.x + offset.x, this.position.y + offset.y)

        if (nextPipe && nextPipe !== START) {
            return
        }

        // Add current position to history
        this.path.push(this.position)

        // Update current position
        this.position = {
            x: this.position.x + offset.x,
            y: this.position.y + offset.y,
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
        // Add the pipe to the grid
        this.grid[this.key(formerPosition.x, formerPosition.y)] =
            offsets[`${xOffset2}:${yOffset2}:${xOffset1}:${yOffset1}`]
    }

    columns() {
        return _.range(this.minX(), this.maxX())
    }

    rows() {
        return _.range(this.minY(), this.maxY())
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
        <>
            <GridControls
                complete={pipeGridRef.current.isCompleted()}
                pipeGrid={pipeGridRef.current}
                forceRerender={forceRerender}
            />

            <Divider />

            <ViewableGrid
                rows={pipeGridRef.current.rows()}
                columns={pipeGridRef.current.columns()}
                complete={pipeGridRef.current.isCompleted()}
                pipeGrid={pipeGridRef.current}
            />
        </>
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

function GridControls(props: { complete: boolean; pipeGrid: PipeGrid; forceRerender: () => void }) {
    /**************************************************************************/
    /* State */
    const [pressedKey, setPressedKey] = useState<PressedKey | "Delete" | null>(null)

    /**************************************************************************/
    /* Render */
    return (
        <div className="tw-flex tw-gap-4">
            <div className="tw-w-fit">
                <div className="tw-relative tw-pb-2 tw-text-primary tw-opacity-80">
                    <div>Click for keyboard controls</div>
                    <div className="tw-absolute tw-left-[50%] tw-top-2.5 tw-translate-x-[-50%]">
                        ⌄
                    </div>
                </div>

                <div
                    className={classNames(
                        "tw-cursor-pointer tw-rounded tw-border-2 tw-border-primary tw-p-1",
                        "focus-within:tw-outline-secondary hover:tw-outline-secondary focus:tw-outline-secondary active:tw-outline-secondary",
                    )}
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
                    <div className="tw-flex tw-justify-evenly">
                        <div className="tw-flex tw-flex-col tw-gap-2">
                            <div className="tw-flex tw-w-full tw-justify-center">
                                <button
                                    className={classNames(
                                        "tw-btn tw-btn-primary tw-btn-sm tw-h-8 tw-w-8 tw-duration-0",
                                        pressedKey === "W" ? "tw-bg-primary-hover" : "",
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
                                                "tw-btn tw-btn-primary tw-btn-sm tw-size-8 tw-duration-0",
                                                pressedKey === letter ? "tw-bg-primary-hover" : "",
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
                                pressedKey === "Delete" ? "tw-bg-primary-hover" : "",
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
            </div>

            <div className="tw-flex tw-gap-4 tw-pt-8">
                <div>
                    <button
                        className="tw-btn tw-btn-primary"
                        onClick={() => {
                            props.forceRerender()
                        }}
                    >
                        Expand
                    </button>
                </div>

                <div>
                    <button
                        className="tw-btn tw-btn-primary"
                        disabled={!props.complete}
                    >
                        Flood Fill | ⏵
                    </button>
                </div>
            </div>
        </div>
    )
}

function ViewableGrid(props: {
    rows: Array<number>
    columns: Array<number>
    complete: boolean
    pipeGrid: PipeGrid
}) {
    /**************************************************************************/
    /* Render */
    return (
        <div className="tw-max-w-[100%] tw-overflow-x-auto tw-pb-4">
            <div className="tw-flex tw-h-fit tw-w-fit tw-flex-col tw-rounded tw-border-2 tw-border-primary">
                {props.rows.map((y) => {
                    return (
                        <div
                            key={y}
                            className="tw-flex tw-flex-shrink-0"
                        >
                            {props.columns.map((x) => {
                                const isCurrentPosition = props.pipeGrid.isHere(x, y)

                                return (
                                    <div
                                        key={x}
                                        className={classNames(
                                            "tw-relative tw-flex tw-size-10 tw-items-center tw-justify-center",
                                            isCurrentPosition ? "tw-bg-primary tw-text-white" : "",
                                            pipeClasses[props.pipeGrid.getValue(x, y) || EMPTY],
                                            props.complete ? "tw-border-secondary" : "",
                                            props.complete &&
                                                props.pipeGrid.getValue(x, y) === START
                                                ? "tw-bg-secondary"
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
        </div>
    )
}
