"use client"

import React from "react"

export function Loading(props) {
    /**************************************************************************/
    /* Render */
    return <div className={props.on ? "tw-animate-pulse" : ""}>{props.children}</div>
}
