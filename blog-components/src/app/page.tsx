import { Divider } from "@components/divider"
import { LoadingButton } from "@components/loading-button"

export default function Page() {
    /**************************************************************************/
    /* Render */
    return (
        <div className="flex flex-col p-4">
            <LoadingButton />

            <Divider />
        </div>
    )
}
