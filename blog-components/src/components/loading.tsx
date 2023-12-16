"use client"

import React from "react"

export function Loading(props: { on: boolean; children: React.JSX.Element }) {
    /**************************************************************************/
    /* Render */
    return <div className={props.on ? "tw-animate-pulse" : ""}>{props.children}</div>
}
