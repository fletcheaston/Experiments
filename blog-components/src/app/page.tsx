import { ClickedButton } from "@components/clicked-button"
import { Divider } from "@components/divider"
import { LoadingButton } from "@components/loading-button"

export default function Page() {
    /**************************************************************************/
    /* Render */
    return (
        <div className="tw-flex tw-flex-col tw-p-4">
            <h1 className="tw-text-4xl">All Components</h1>

            <Divider />

            <LoadingButton />

            <Divider />

            <ClickedButton />

            <Divider />
        </div>
    )
}
