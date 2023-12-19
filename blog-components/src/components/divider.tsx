"use client"

import classNames from "classnames"

export function Divider(props: { className?: string }) {
    /**************************************************************************/
    /* Render */
    return (
        <hr
            className={classNames(
                "tw-my-4 tw-border-t-[1px] tw-border-t-slate-300",
                props.className,
            )}
        />
    )
}
