import { cn } from "@utils"
import { RenderLeafProps } from "slate-react"

export function Formatted(props: RenderLeafProps) {
    /**************************************************************************/
    /* State */
    if (props.leaf.type !== "formatted") {
        throw new Error("Formatted leaf rendered with unknown leaf type.")
    }

    /**************************************************************************/
    /* Render */
    return (
        <span
            {...props.attributes}
            className={cn(
                props.leaf.bold ? "font-bold" : "",
                props.leaf.italics ? "italic" : "",
                props.leaf.strikethrough ? "line-through" : "",
            )}
        >
            {props.children}
        </span>
    )
}
