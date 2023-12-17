"use client";
import React, { useState } from "react";
export function ClickedButton() {
    /**************************************************************************/
    /* State */
    const [clicks, setClicks] = useState(0);
    /**************************************************************************/
    /* Render */
    return (<div className="tw-flex tw-gap-4">
            <button className="tw-btn tw-btn-primary" onClick={() => {
            setClicks(0);
        }}>
                Reset Clicks
            </button>

            <button className="tw-btn tw-btn-primary" onClick={() => {
            setClicks((prevState) => prevState + 1);
        }}>
                Clicked {clicks} time{clicks === 1 ? "" : "s"}
            </button>
        </div>);
}
