"use client"

import classNames from "classnames"

export function Divider(props: { className?: string }) {
    /**************************************************************************/
    /* Render */
    return <hr className={classNames("my-4 border-t-[1px] border-t-slate-300", props.className)} />
}
