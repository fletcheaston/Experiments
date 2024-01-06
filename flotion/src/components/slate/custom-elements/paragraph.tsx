import { RenderElementProps } from "slate-react"

export function Paragraph(props: RenderElementProps) {
    /**************************************************************************/
    /* Render */
    return <p {...props.attributes}>{props.children}</p>
}
