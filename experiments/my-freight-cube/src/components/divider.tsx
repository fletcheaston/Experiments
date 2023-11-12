import classNames from "classnames"

export function Divider(props: { className?: string }) {
    return <hr className={classNames("border-t-[1px] border-t-slate-300", props.className)} />
}
