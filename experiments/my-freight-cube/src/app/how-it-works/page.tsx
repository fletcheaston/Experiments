import { Divider } from "@components/divider"
import React from "react"

import { VideoCard } from "./video-card"

export default async function Page() {
    /**************************************************************************/
    /* Render */
    return (
        <>
            <h1 className="mt-12 text-center text-5xl font-semibold">How It Works</h1>

            <div className="mt-8 grid grid-cols-1 gap-x-12 gap-y-16 px-16 lg:grid-cols-2">
                <VideoCard
                    title="Lineal Foot Calculator"
                    link="https://www.youtube.com/embed/ayWb6uKpx5E"
                />

                <VideoCard
                    title="Partial Truckload Rate Calculator"
                    link="https://www.youtube.com/embed/JhmINw6Wnlg"
                />

                <VideoCard
                    title="LTL Density Calculator"
                    link="https://www.youtube.com/embed/PLnxDrKPVuo"
                />

                <VideoCard
                    title="Air Freight Dim Weight Calculator"
                    link="https://www.youtube.com/embed/wtWKZ8FV6YY"
                />

                <VideoCard
                    title="Parcel Dim Weight Calculator"
                    link="https://www.youtube.com/embed/ZS3uddwMbpM"
                />
            </div>

            <Divider className="mt-8" />
        </>
    )
}
