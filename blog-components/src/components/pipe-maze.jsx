"use client"

import { useRerender } from "@react-hookz/web"
import classNames from "classnames"
import _ from "lodash"
import React, { useRef, useState } from "react"

import { Divider } from "@components/divider"
import { Grid } from "@components/grid"

const EMPTY = "◦"
const START = "S"
const pipes = [EMPTY, "|", "-", "L", "J", "7", "F", START]
class PipeGrid extends Grid {
    constructor() {
        super()
        this.path = []
        this.position = { x: 0, y: 0 }
        this.addValue(0, 0, START)
    }
    clear() {
        super.clear()
        this.position = { x: 0, y: 0 }
        this.path = []
        this.addValue(0, 0, START)
    }
    pathIndex(x, y) {
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
    const pipeGridRef = useRef(new PipeGrid())
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
function GridControls(props) {
    /**************************************************************************/
    /* State */
    const [pressedKey, setPressedKey] = useState("W")
    /**************************************************************************/
    /* Render */
    return (
        <>
            <div className="tw-relative tw-pb-2 tw-text-primary tw-opacity-80">
                <div>Click for keyboard controls</div>
                <div className="tw-absolute tw-left-[50%] tw-top-2.5 tw-translate-x-[-50%]">⌄</div>
            </div>

            <div
                className="tw-flex tw-flex-col tw-gap-2 tw-rounded tw-border-2 tw-border-primary tw-p-1"
                onKeyDown={(event) => {
                    console.log(event)
                }}
            >
                <div className="tw-flex tw-w-full tw-justify-center">
                    <button
                        className={classNames(
                            "tw-btn tw-btn-primary tw-btn-sm tw-h-8 tw-w-8",
                            pressedKey === "W" ? "tw-bg-primary-hover" : "",
                        )}
                    >
                        W
                    </button>
                </div>

                <div className="tw-flex tw-justify-center tw-gap-2">
                    <button className="tw-btn tw-btn-primary tw-btn-sm tw-w-8">A</button>
                    <button className="tw-btn tw-btn-primary tw-btn-sm tw-w-8">S</button>
                    <button className="tw-btn tw-btn-primary tw-btn-sm tw-w-8">D</button>
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
function ViewableGrid(props) {
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
                                    className="tw-relative tw-flex tw-h-6 tw-w-6 tw-items-center tw-justify-center"
                                >
                                    {pathIndex && <div className="tw-absolute">{pathIndex}</div>}

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
