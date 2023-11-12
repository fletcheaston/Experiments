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
                    link="https://youtu.be/ayWb6uKpx5E"
                />

                <VideoCard
                    title="Partial Truckload Rate Calculator"
                    link="https://youtu.be/JhmINw6Wnlg"
                />

                <VideoCard
                    title="LTL Density Calculator"
                    link="https://youtu.be/PLnxDrKPVuo"
                />

                <VideoCard
                    title="Air Freight Dim Weight Calculator"
                    link="https://youtu.be/wtWKZ8FV6YY"
                />

                <VideoCard
                    title="Parcel Dim Weight Calculator"
                    link="https://youtu.be/ZS3uddwMbpM"
                />
            </div>
        </>
    )
}
