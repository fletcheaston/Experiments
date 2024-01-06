import { RenderLeafProps } from "slate-react"

export function Plain(props: RenderLeafProps) {
    /**************************************************************************/
    /* Render */
    return <span {...props.attributes}>{props.children}</span>
}
