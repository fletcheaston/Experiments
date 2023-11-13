import Image, { StaticImageData } from "next/image"
import React from "react"

import { Divider } from "@components/divider"

import HeroImage from "@images/hero.jpg"
import CalculatorIcon from "@images/icon-calculator.png"
import GearIcon from "@images/icon-gear.png"
import TruckIcon from "@images/icon-truck.png"
import PatternImage from "@images/pattern.png"

function BackgroundCard(props: { icon: StaticImageData }) {
    return (
        <div
            className="flex items-center justify-center px-12 py-16 text-white"
            style={{
                backgroundImage: `url(${props.icon.src})`,
                backgroundRepeat: "no-repeat",
                backgroundPosition: "center",
                backgroundSize: "cover",
            }}
        >
            <div className="flex w-[500px] flex-col gap-6 text-center">
                <h1 className="text-3xl font-semibold md:text-5xl md:leading-snug">
                    The Single Source for Freight Conversions and Calculations
                </h1>

                <p className="text-xl">Make sure you&apos;re not paying for freight you don&apos;t ship!</p>
            </div>
        </div>
    )
}

function CalculatorCard(props: { title: string; description: string }) {
    /**************************************************************************/
    /* Render */
    return (
        <div className="flex flex-col gap-2 rounded border-[1px] border-slate-300 px-6 pb-6 pt-6 text-center">
            <h3 className="text-4xl">{props.title}</h3>
            <p>{props.description}</p>
        </div>
    )
}

function BenefitCard(props: { icon: StaticImageData; alt: string; title: string; description: string }) {
    return (
        <div className="flex flex-col items-center gap-2 px-6 pb-6 text-center">
            <Image
                src={props.icon}
                alt={props.alt}
                className="px-2 md:px-4 lg:px-10"
            />
            <h3 className="text-4xl">{props.title}</h3>
            <p>{props.description}</p>
        </div>
    )
}

export default async function Page() {
    /**************************************************************************/
    /* Render */
    return (
        <>
            <BackgroundCard icon={HeroImage} />

            <h2 className="mt-8 px-12 text-center text-5xl">MyFreightCube Calculators</h2>

            <div className="mt-8 grid grid-cols-1 gap-x-6 gap-y-4 px-12 md:grid-cols-2 xl:grid-cols-4">
                <CalculatorCard
                    title="Lineal Feet"
                    description="Determine how much space of a trailer your shipment will take."
                />

                <CalculatorCard
                    title="LTL Density"
                    description="Get your shipments' density and an estimate of the NMFC shipping class."
                />

                <CalculatorCard
                    title="Air Freight Dim Weight"
                    description="Quickly determine billable weight on your domestic or international shipment."
                />

                <CalculatorCard
                    title="Parcel Dim Weight"
                    description="Quickly determine billable weight on your parcel/small pack shipment."
                />
            </div>

            <Divider className="mx-12 mt-6" />

            <div className="mt-4 grid grid-cols-1 gap-x-6 gap-y-4 px-12 md:grid-cols-3">
                <BenefitCard
                    icon={CalculatorIcon}
                    alt="Calculator icon"
                    title="Ease of Use"
                    description="All calculators are self-explanatory, no training necessary and easy to use. Just enter your product dimensions and your calculation comes back instantly. You can also easily cycle through different carriers without having to re-enter information."
                />

                <BenefitCard
                    icon={GearIcon}
                    alt="Gear icon"
                    title="User Customization"
                    description="Customize your calculators based on specific carrier contracts you have. You can have as many carriers as you want, each with different numbers, and you can choose your own defaults so you don't have to change every time."
                />

                <BenefitCard
                    icon={TruckIcon}
                    alt="Truck icon"
                    title="Lineal Foot Conversion"
                    description="MFC has the only calculator that will determine how much room on a trailer/container will be required, even if some of the shipping units can double, triple, or multiple stack."
                />
            </div>

            <BackgroundCard icon={PatternImage} />
        </>
    )
}
