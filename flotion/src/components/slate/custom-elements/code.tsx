import { RenderElementProps } from "slate-react"

export function Code(props: RenderElementProps) {
    /**************************************************************************/
    /* Render */
    return (
        <pre
            {...props.attributes}
            className="text-rose-500"
        >
            {props.children}
        </pre>
    )
}
