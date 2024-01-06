import { RenderLeafProps } from "slate-react"

export function Code(props: RenderLeafProps) {
    /**************************************************************************/
    /* Render */
    return (
        <span
            {...props.attributes}
            className="text-rose-500"
        >
            {props.children}
        </span>
    )
}
