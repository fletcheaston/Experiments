"use client"

import React from "react"

export function Loading(props: { on: boolean; children: React.JSX.Element }) {
    /**************************************************************************/
    /* Render */
    return <div className={props.on ? "animate-pulse" : ""}>{props.children}</div>
}
