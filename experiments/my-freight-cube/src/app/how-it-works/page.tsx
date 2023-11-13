import React from "react"

import { VideoCard } from "./video-card"

export default async function Page() {
    /**************************************************************************/
    /* Render */
    return (
        <>
            <h1 className="mt-8 text-center text-5xl font-semibold">How It Works</h1>

            <div className="mt-8 flex flex-wrap justify-center gap-x-8 gap-y-12 px-16">
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

            <div className="mt-8" />
        </>
    )
}
