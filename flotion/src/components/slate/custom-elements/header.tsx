import { cn } from "@utils"
import React from "react"
import { RenderElementProps } from "slate-react"

import { HeaderElement } from "@components/slate/types"

const levelToFontSize: Record<HeaderElement["level"], string> = {
    1: "text-3xl",
    2: "text-2xl",
    3: "text-xl",
}

export function Header(props: RenderElementProps) {
    /**************************************************************************/
    /* State */
    if (props.element.type !== "header") {
        throw new Error("Header element rendered with unknown element type.")
    }

    const LeveledTag: keyof React.JSX.IntrinsicElements = `h${props.element.level}`

    /**************************************************************************/
    /* Render */
    return (
        <LeveledTag
            {...props.attributes}
            className={cn(levelToFontSize[props.element.level], "font-bold")}
        >
            {props.children}
        </LeveledTag>
    )
}
