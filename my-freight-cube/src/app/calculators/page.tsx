import { RouteType } from "next/dist/lib/load-custom-routes"
import Image, { StaticImageData } from "next/image"
import Link, { LinkProps } from "next/link"
import React from "react"

import CubeIcon from "@images/icon-density.png"
import PlaneIcon from "@images/icon-plane.png"
import BoxIcon from "@images/icon-shipping-box.png"
import TruckIcon from "@images/icon-truck.png"

function CalculatorCard(props: {
    icon: StaticImageData
    alt: string
    title: string
    description: string
    link: LinkProps<RouteType>["href"]
}) {
    /**************************************************************************/
    /* Render */
    return (
        <div className="flex w-[360px] flex-col items-center gap-3 rounded border-[1px] border-slate-300 px-6 pb-5 pt-6 text-center">
            <Image
                src={props.icon}
                alt={props.alt}
                className="w-[35%]"
            />
            <h3 className="text-4xl font-semibold">{props.title}</h3>
            <p>{props.description}</p>
            <Link
                href={props.link}
                className="btn btn-primary-outline mt-auto"
            >
                Get Started
            </Link>
        </div>
    )
}

export default async function Page() {
    /**************************************************************************/
    /* Render */
    return (
        <>
            <h1 className="mt-8 text-center text-5xl font-semibold">MyFreightCube Calculators</h1>

            <div className="mt-8 flex flex-wrap justify-center gap-8 px-16">
                <CalculatorCard
                    icon={TruckIcon}
                    alt="Track icon"
                    title="Lineal Feet"
                    description="Determine how much space of a trailer your shipment will take."
                    link="/calculators/lineal-foot"
                />

                <CalculatorCard
                    icon={CubeIcon}
                    alt="Gridded-cube icon"
                    title="LTL Density"
                    description="Get your shipments' density and an estimate of the NMFC shipping class."
                    link="/calculators/ltl-density"
                />

                <CalculatorCard
                    icon={PlaneIcon}
                    alt="Airplane icon"
                    title="Air Freight Dim Weight"
                    description="Quickly determine billable weight on your domestic or international shipment."
                    link="/calculators/air-freight-dim-weight"
                />

                <CalculatorCard
                    icon={BoxIcon}
                    alt="Shipping box icon"
                    title="Parcel Dim Weight"
                    description="Quickly determine billable weight on your parcel/small pack shipment."
                    link="/calculators/parcel-dim-weight"
                />
            </div>

            <div className="mt-8" />
        </>
    )
}
